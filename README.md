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

The portfolio includes a live 100 Days of Python section. Source files live in `projects/python-100-days/`. The current build includes Days 01–04 plus two Day 04 bonus security projects. Challenge progress is 04/100, with 6 total projects shipped. Day 04 (Password Audit Tool) is currently featured.

For each new day, add the new Python file, update the challenge-day counter and project cards in `index.html`, then commit and push. Bonus projects should increase the total-project count without increasing the 100-day challenge counter.
