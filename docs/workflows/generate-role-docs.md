# ⚙️ GitHub Action: Generate Ansible Role Docs

## 📖 Purpose
This workflow ensures that documentation for all Ansible roles is **automatically generated and kept up to date**.  
Whenever code is pushed or a pull request is opened, the workflow runs the `generate_role_docs.py` script, which regenerates each role’s `README.md`, and updates the central `roles/README.md` index. If changes are detected, they are committed back to the repository.

---

## 🛠 Workflow File
Located at: `.github/workflows/generate-role-docs.yml`

```yaml
name: Generate Ansible Role Docs

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  generate-role-docs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Generate role docs
        run: |
          python scripts/generate_role_docs.py

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add roles/*/README.md roles/README.md
          if ! git diff --cached --quiet; then
            git commit -m "chore(docs): auto-generate role documentation"
            git push origin HEAD:${{ github.ref }}
          else
            echo "No documentation changes to commit."
          fi
```

---

## 🔑 Key Points

- **Trigger:** Runs on every push to `main` and on pull requests.  
- **Checkout:** Uses `actions/checkout@v4` with `fetch-depth: 0` so commits can be pushed back.  
- **Python Setup:** Uses Python 3.11 (adjustable).  
- **Dependencies:** Installs from `requirements.txt` (currently only `PyYAML`).  
- **Script Execution:** Runs `scripts/generate_role_docs.py` to regenerate docs.  
- **Commit Logic:**  
  - Stages only role READMEs and the central index.  
  - Commits only if changes exist (`git diff --cached --quiet` prevents empty commits).  
  - Pushes back to the branch that triggered the workflow.  
- **Permissions:** Requires repository **Actions → Workflow permissions** set to **Read and write** so the built‑in `GITHUB_TOKEN` can push commits.  
