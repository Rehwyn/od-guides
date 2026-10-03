"""Validate selected public sources, or explicitly build their presentation."""
import argparse
import hashlib
import html
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / '.build'
CREATOR_LINKS = '<p class="creator-links"><a href="https://ourdream.ai/u/rehwyn">My OurDream profile</a> · <a href="https://ourdream.ai/refer/UNIIYM">Referral link</a> · Referral code: <code>UNIIYM</code></p>'


def validate(manifest):
    entries = manifest['guides']
    if not entries:
        raise ValueError('No selected guides')
    slugs = set()
    for entry in entries:
        slug = entry['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in slugs:
            raise ValueError('Invalid or duplicate guide route: ' + slug)
        slugs.add(slug)
        source = (ROOT / entry['source']).resolve()
        if not source.is_relative_to(ROOT.resolve()):
            raise ValueError('Source escapes public repository')
        relative = source.relative_to(ROOT.resolve())
        if any(p.startswith('.') or p in {'local', 'fixtures', 'tests', 'site'} for p in relative.parts):
            raise ValueError('Source is in a non-public input directory')
        if source.suffix.lower() != '.md' or not source.is_file():
            raise ValueError('Missing selected Markdown source: ' + entry['source'])
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('Source hash mismatch: ' + entry['source'])
        for key in ('title', 'nav_title', 'author', 'version', 'summary'):
            if not isinstance(entry[key], str) or not entry[key].strip():
                raise ValueError('Missing public metadata: ' + key)
        if entry.get('license') != 'CC BY 4.0':
            raise ValueError('Selected guides require the owner-selected CC BY 4.0 license')
        if not source.read_text(encoding='utf-8-sig').startswith('# '):
            raise ValueError('Selected source must start with its H1 title')
    return entries


def check_environment():
    if sys.version_info[:3] != (3, 12, 14):
        raise ValueError('Build requires Python 3.12.14')
    for line in (ROOT / 'requirements.lock.txt').read_text().splitlines():
        if line and not line.startswith('#'):
            name, version = line.split('==')
            if importlib.metadata.version(name) != version:
                raise ValueError('Dependency differs from lock: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Read-only validation (default)')
    mode.add_argument('--build', action='store_true', help='Stage and clean-strict build selected sources')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'guides.json').read_text(encoding='utf-8'))
    entries = validate(manifest)
    if not args.build:
        print('Selected-source validation passed')
        return
    check_environment()
    # Cleanup is confined to this repository's generated build directory.
    if BUILD.is_symlink() or not BUILD.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Build directory escapes repository')
    if BUILD.exists():
        shutil.rmtree(BUILD)
    stage = BUILD / 'docs'
    output = BUILD / 'www' / 'od-guides'
    stage.mkdir(parents=True)
    nav = [{'Guide library': 'index.md'}]
    home = ['# Rehwyn’s creator guides', '',
            'Practical resources for OurDream creators, written by **Rehwyn**. These are unofficial guides; product features and advice may change.', '',
            '## Choose a guide', '']
    for entry in entries:
        relative = f"guides/{entry['slug']}/index.md"
        dest = stage / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        source = (ROOT / entry['source']).read_text(encoding='utf-8-sig')
        lines = source.splitlines(keepends=True)
        meta = html.escape(f"By {entry['author']} · {entry['version']}")
        byline = f'<p class="guide-meta">{meta} · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></p>'
        notice = f'\n\n<p class="guide-license">© 2026 {html.escape(entry["author"])}. This guide, including its examples and prompts, is licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Share or adapt it with credit, a license link, and changes identified. See the <a href="{html.escape("https://rehwyn.github.io/od-guides/guides/" + entry["slug"] + "/")}">source guide</a>.</p>\n'
        presentation = lines[0] + '\n\n' + byline + '\n\n' + CREATOR_LINKS + '\n\n' + ''.join(lines[1:]) + notice
        dest.write_text(presentation, encoding='utf-8', newline='\n')
        nav.append({entry['nav_title']: relative})
        home += [f"- [{entry['title']}]({relative}) — {entry['summary']} ({entry['version']})", '']
    home += [CREATOR_LINKS, '', '## Reading and source', '',
             'Each guide is one continuous page. Use the library to choose a guide, its contents to jump between sections, and search to find a topic. Your browser can print the complete article.', '',
             'The displayed version identifies the selected public copy. A draft label remains a draft label.', '',
             '[View the public Markdown sources on GitHub](https://github.com/Rehwyn/od-guides).', '',
             'Written guides, examples and prompts are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), with credit to Rehwyn. Site tooling is MIT licensed. [Licensing details](licensing.txt).']
    (stage / 'index.md').write_text('\n'.join(home) + '\n', encoding='utf-8')
    for name in ('extra.css', 'extra.js'):
        (stage / name).write_bytes((ROOT / 'site' / name).read_bytes())
    (stage / 'third-party-notices.txt').write_bytes((ROOT / 'THIRD_PARTY_NOTICES.md').read_bytes())
    for name in ('LICENSE.md', 'LICENSE-MIT.txt'):
        (stage / ('licensing.txt' if name == 'LICENSE.md' else 'license-mit.txt')).write_bytes((ROOT / name).read_bytes())
    config = (ROOT / 'zensical.toml').read_text(encoding='utf-8')
    toml_nav = ', '.join('{' + json.dumps(key, ensure_ascii=False) + ' = ' + json.dumps(value) + '}'
                         for item in nav for key, value in item.items())
    config = config.replace('nav = []', 'nav = [' + toml_nav + ']')
    config_path = ROOT / 'zensical.generated.toml'
    config_path.write_text(config, encoding='utf-8')
    env = dict(os.environ)
    env['PYTHONPATH'] = str(ROOT / 'site')
    subprocess.run([sys.executable, '-m', 'zensical', 'build', '-f', str(config_path), '--clean', '--strict'], cwd=ROOT, env=env, check=True)
    versions = {line.split('==')[0]: importlib.metadata.version(line.split('==')[0])
                for line in (ROOT / 'requirements.lock.txt').read_text().splitlines() if line and not line.startswith('#')}
    (BUILD / 'build-record.json').write_text(json.dumps({
        'python': sys.version.split()[0], 'dependencies': versions,
        'source_provenance_commit': manifest['source_commit'],
        'source_revision': manifest.get('source_revision', 'Committed public source baseline'),
        'guides': [{'source': e['source'], 'sha256': e['sha256'], 'slug': e['slug'], 'version': e['version'], 'license': e['license']} for e in entries],
        'canonical_url': 'https://rehwyn.github.io/od-guides/'}, indent=2), encoding='utf-8')
    print('Built production output: .build/www/od-guides/')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, importlib.metadata.PackageNotFoundError) as error:
        raise SystemExit(str(error))
