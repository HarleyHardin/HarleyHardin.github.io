# harleyhardin.me

Static cybersecurity + Python portfolio for Harley Hardin, designed for GitHub Pages.

## Before publishing

Search the project for these placeholders and replace them:

- `HarleyHardin`
- `HarleyHardin.github.io`
- `YOUR_EMAIL_ADDRESS`
- `YOUR_LINKEDIN`

Then add your resume as:

`resume/harley-hardin-resume.pdf`

## Preview locally

From this directory:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## GitHub Pages

Use a public repository named `<your-github-username>.github.io` for the simplest personal-site setup.

Push this folder's contents to the repository's `main` branch, then enable GitHub Pages from `main` / `(root)` in Repository Settings > Pages.

The included `CNAME` file contains:

`harleyhardin.me`

## DNS records for harleyhardin.me

For the root (`@`), point four A records to GitHub Pages:

- 185.199.108.153
- 185.199.109.153
- 185.199.110.153
- 185.199.111.153

For `www`, create a CNAME pointing to:

`<your-github-username>.github.io`

Do not use a wildcard (`*`) record for GitHub Pages.

## 100 Days of Python

The portfolio includes a live 100 Days of Python section. Source files live in `projects/python-100-days/`. The current build includes Days 01–09 plus four bonus projects. Challenge progress is 09/100, with 13 total projects shipped. Day 09, the Access Control Gateway, is now featured because it combines SQLite lookups, parameterized SQL, room-specific access-control lists, authorization decisions, and audit logging. The Day 08 Casino is counted as a bonus build, while the Day 04 VirusTotal URL Analyzer remains available in the project grid.

Day 09 expects two supporting paths relative to the project folder: `databases/employees.db` and `logs/access_logs.txt`. The included update carries the uploaded access log, but does not fabricate the binary SQLite database. Copy your existing Day 09 `employees.db` into `projects/python-100-days/databases/employees.db` before publishing if you want the repository copy to be runnable as-is.

For each new day, add the new Python file, update the challenge-day counter and project cards in `index.html`, then commit and push. Bonus projects should increase the total-project count without increasing the 100-day challenge counter.
