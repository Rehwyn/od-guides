# Rehwyn’s creator guides

Public Markdown sources and a static reading library. Each guide remains one continuous page. The site configuration targets <https://rehwyn.github.io/od-guides/>; publication uses a manually dispatched GitHub Actions workflow.

## Source ownership

`guides.json` explicitly selects public sources and their SHA-256 hashes. The original beginner guide keeps its filename and `v1.0-DRAFT` label. Its bytes are unchanged by the site builder. Generated presentation copies add author/version metadata; do not edit those copies.

The current guide is the reviewed editorial revision committed September 30, 2026. Its hash and exact source commit are recorded in the manifest. The deployment run separately records the complete production revision, dependency versions, and generated-file hashes.

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
3. Add a file-specific `-text` rule in `.gitattributes` for each maintained guide. This preserves its approved bytes across Windows and Linux. Verify the staged Git blob and a fresh checkout match the approved hash before release.
4. Calculate the source hash with `Get-FileHash -Algorithm SHA256 <source>` (PowerShell) or `sha256sum <source>`. Update a hash only after reviewing the changed bytes.
5. Run validation and build. Check headings, fenced prompts, tables, navigation, search, narrow screens, keyboard/focus, browser zoom, print output, and public metadata before deployment.

Keep existing slugs stable across editions. A versioned source filename need not change its website route. Heading changes can break shared section links; retain an explicit anchor alias where appropriate or record an intentional compatibility change. Record release provenance and reconcile later public edits before replacing a source from elsewhere.

## Dependencies, recovery, and publishing

To upgrade dependencies, review official release notes, change pins explicitly, install into a fresh environment, and rerun affected rendering/navigation/privacy checks. Synthetic fixtures are local development inputs only. Keep environments, local evidence, caches, staging, and generated HTML out of Git.

To rebuild an earlier site, use a separate checkout of the selected public source/configuration commit, install its pinned environment, validate the hashes, and build. For a future public rollback, use a reviewed revert or corrective commit and redeploy; do not rewrite history for routine recovery.

Publishing uses `.github/workflows/pages.yml`: manually run **Guide library Pages** from `main` in GitHub Actions. Record the run revision and review its build summary before sharing the release. Pushes do not publish; pull requests run build checks without deployment. The build uses Ubuntu 24.04, Python 3.12.14 and the full dependency lock. Only generated site contents are uploaded, with build records kept outside the served site.

Pages uses GitHub Actions as its publishing source, with deployment restricted to `main` through the `github-pages` environment. Deployments are serialized. The public address is <https://rehwyn.github.io/od-guides/>. No personal token is stored in the workflow.

For recovery, identify the reviewed release commit from a successful run; revert subsequent changes or make a corrective commit on `main`, validate/build, and manually deploy again. Do not force-push routine recovery. Before the first successful deployment there is no previous site artifact to restore. Disabling **Guide library Pages** in Actions stops new deployments; use **Settings → Pages → Unpublish site** separately to remove the served site, and verify the public URL afterward. No analytics, comments, external fonts, or custom domain are configured.

Written guides, including examples and prompts, are **CC BY 4.0**, with attribution to **Rehwyn**. Original site tooling and maintenance documentation are **MIT** licensed. See `LICENSE.md` for the scope split and `LICENSE-MIT.txt` for the software license. Generator and theme dependencies retain their own software licenses; see `THIRD_PARTY_NOTICES.md`.
