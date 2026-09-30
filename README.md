# Rehwyn’s creator guides

Public Markdown sources and a prepared static reading library. Each guide remains one continuous page. The site configuration targets <https://rehwyn.github.io/od-guides/>; this preparation does not enable publishing.

## Source ownership

`guides.json` explicitly selects public sources and their SHA-256 hashes. The original beginner guide keeps its filename and `v1.0-DRAFT` label. Its bytes are unchanged by the site builder. Generated presentation copies add author/version metadata; do not edit those copies.

The current working copy includes a reviewed editorial revision prepared September 30, 2026. Its hash is recorded in the manifest; `source_commit` identifies the public base, and `source_revision` identifies the uncommitted revision until a public commit records it.

Only reviewed public sources belong in this repository. Add no private notes, internal drafts, or navigation fixtures to the production manifest. There is no automatic synchronization with another repository. Content release review and website deployment are separate decisions.

## Local setup and build

Use Python **3.12.14**, an isolated environment, and the complete pinned dependency file (including **Zensical 0.0.66**). The 0.0.x generator is developmental; review upgrades deliberately.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe build.py --check
.\.venv\Scripts\python.exe build.py --build
.\.venv\Scripts\python.exe serve.py
```

The selected interpreter must report 3.12.14; `--build` checks it and the dependency pins. On other systems use the corresponding Python 3.12.14 executable and `.venv/bin/python`. Validation is read-only and is also the default when no option is supplied. The build stages only manifest-selected guides and runs a clean strict Zensical build. Use the adapter rather than invoking the template configuration directly.

Generated output is `.build/www/od-guides/`. The loopback preview prefers port 8765 and prints its actual URL if that port is occupied. It serves generated files only, beneath `/od-guides/`, with directory listings disabled. Stop a foreground preview with Ctrl+C. A background preview records its PID and URL in `.build/server.json`; verify that process identity before stopping it. Stop the preview before a fresh build because the build replaces `.build/`.

## Add or update a guide

1. Review the exact public revision, product claims, citations, permissions, author metadata, and intended release label.
2. Maintain one source file. Add or update its `guides.json` entry: source, stable slug, title, navigation title, author, version, summary, SHA-256, and `license` (`CC BY 4.0`). Keep sources inside this repository, outside ignored/test/build directories, beginning with their H1 title.
3. Calculate the source hash with `Get-FileHash -Algorithm SHA256 <source>` (PowerShell) or `sha256sum <source>`. Update a hash only after reviewing the changed bytes.
4. Run validation and build. Check headings, fenced prompts, tables, navigation, search, narrow screens, keyboard/focus, browser zoom, print output, and public metadata before deployment.

Keep existing slugs stable across editions. A versioned source filename need not change its website route. Heading changes can break shared section links; retain an explicit anchor alias where appropriate or record an intentional compatibility change. Record release provenance and reconcile later public edits before replacing a source from elsewhere.

## Dependencies, recovery, and publishing

To upgrade dependencies, review official release notes, change pins explicitly, install into a fresh environment, and rerun affected rendering/navigation/privacy checks. Synthetic fixtures are local development inputs only. Keep environments, local evidence, caches, staging, and generated HTML out of Git.

To rebuild an earlier site, use a separate checkout of the selected public source/configuration commit, install its pinned environment, validate the hashes, and build. For a future public rollback, use a reviewed revert or corrective commit and redeploy; do not rewrite history for routine recovery.

Publishing is not configured here. A later authorized phase will add manual GitHub Actions deployment and review the exact artifact before enabling Pages. Disabling a future workflow stops new deployments; unpublishing Pages is a separate operation that removes the served site. No analytics, comments, external fonts, or custom domain are configured.

Written guides, including examples and prompts, are **CC BY 4.0**, with attribution to **Rehwyn**. Original site tooling and maintenance documentation are **MIT** licensed. See `LICENSE.md` for the scope split and `LICENSE-MIT.txt` for the software license. Generator and theme dependencies retain their own software licenses; see `THIRD_PARTY_NOTICES.md`.
