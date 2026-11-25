# Setup and publishing

## 1. ChatGPT (personal prototype)
1. Sign in to ChatGPT on the web. Open Plugins, find **Plugin Creator**, and install it if available.
2. Start a fresh chat, mention `@plugin-creator`, attach `Practice_Room_v1.8_plugin.zip` and paste the following:

> Create and install a personal plugin called Practice Room from this attached v1.8.0 Agent Plugins package. Preserve the two skills, references, and Python music engine. Inspect the manifest and file paths, correct only host-specific compatibility issues, and report any unsupported execution capability. Use a skills-only architecture without remote MCP, external storage or API keys. Test both skills in a new chat. Do not claim successful installation or execution until verified.

3. Follow the creator's install flow and then start a new chat with Practice Room selected. Run the manual tests in `evaluation.md`. If ZIP ingestion isn't available, extract the files and attach `plugin.json`, both `SKILL.md` files (rename copies to practice-tutor-SKILL.md and music-tools-SKILL.md for clarity), references and `music.py`; ask the creator to rebuild the equivalent folder structure. If the creator cannot install it, use the same skills as project instructions/reference files for an interim demo.
4. Direct ZIP upload may be available only to eligible accounts/workspaces. Public directory publishing is separate and requires platform permissions and review. Do not present this as publicly published until approval and actual publication.

Official docs (checked 2026-11-25):
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/deploy/submission

## 2. GitHub (portfolio)
1. Create a new repository at https://github.com/new named `practice-room`. Choose public only if you want the code visible; do not initialize with a README if pushing the complete repo.
2. Extract `Practice_Room_v1.8_repository.zip`. Open its `practice-room` folder in a terminal. Run:

```bash
git init -b main
git add .
git commit -m "Release Practice Room v1.8.0 prototype"
git remote add origin https://github.com/YOUR_USERNAME/practice-room.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username. Authenticate using GitHub's approved sign-in process. Alternatively upload the extracted folder contents via GitHub's web UI (including hidden `.github` directory via a Git client if needed). Do not upload credentials, private learner profiles or the ZIP itself as source.

3. Confirm the README renders and Actions test job passes. Add repository description: `Adaptive AI music tutor for piano, guitar and bass, with deterministic music theory and MIDI tools.`
4. Create a GitHub release tagged `v1.8.0`, attach the plugin ZIP, and include the release notes from CHANGELOG. Add real repository/author metadata to plugin.json when you own the URL; rebuild the archive if you change it. Choose a license before inviting reuse (no license has been assigned on your behalf).

## 3. Before interview
Install and smoke-test the plugin if possible. Open the GitHub README and demonstrate the sample MIDI. If installation is blocked, show the source, local engine and manual demo explicitly as a prototype. Record only actual results. Don't claim you had already built it before the screening.
