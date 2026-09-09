# harleyhardin.me

Static cybersecurity + Python portfolio for Harley Hardin, designed for GitHub Pages.

## Before publishing

Search the project for these placeholders and replace them:

- `YOUR_EMAIL_ADDRESS`
- `YOUR_LINKEDIN`

Then add your resume as:

`resume/harley-hardin-resume.pdf`

## Preview locally

From the portfolio root:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## 100 Days of Python

The current portfolio build includes challenge Days 01–10 plus four bonus projects. Challenge progress is **10/100**, with **14 total projects shipped**.

Day 10 — **Secure Password Storage** — is featured. It revisits the account-registration idea from Day 8 and replaces plaintext password storage with bcrypt hashing and verification backed by SQLite. It also includes password-strength validation, duplicate-account checks, parameterized SQL queries, and login audit logging.

### Day 10 folder structure

The Day 10 ZIP supplied for the project is preserved intact under:

```text
projects/python-100-days/Day_10_Secure_Password_Storage/
├── Day_10_Secure_Password_Storage.py
├── databases/
│   └── users.db
└── logs/
    └── login_logs.txt
```

The Python source currently opens paths beginning with `Day_10_Secure_Password_Storage/...`. To run it **without changing the script**, start it from the parent folder `projects/python-100-days/`:

```bash
python Day_10_Secure_Password_Storage/Day_10_Secure_Password_Storage.py
```

That working directory preserves the script's existing relative paths to `databases/users.db` and `logs/login_logs.txt`.

For each new challenge day, add the new project source and supporting assets, update the challenge-day counter and project cards in `index.html`, then commit and push. Bonus projects increase the total-project count without increasing the 100-day challenge counter.
