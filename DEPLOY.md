# Deploy harleyhardin.me to GitHub Pages + GoDaddy

## 1. Customize the site

Replace these placeholders in `index.html`:

- `HarleyHardin`
- `HarleyHardin.github.io`
- `YOUR_EMAIL_ADDRESS`
- `YOUR_LINKEDIN`

Add your resume to:

`resume/harley-hardin-resume.pdf`

## 2. Create the GitHub repository

Create a **public, empty** GitHub repository named:

`HarleyHardin.github.io`

Do not initialize it with another README, `.gitignore`, or license; this project already contains the files you need.

## 3. Push the website from Kali

```bash
cd ~/Development/harleyhardin.me

git init
git branch -M main
git add .
git commit -m "Initial portfolio site"
git remote add origin https://github.com/HarleyHardin/HarleyHardin.github.io.git
git push -u origin main
```

## 4. Enable GitHub Pages

Repository > Settings > Pages

- Source: Deploy from a branch
- Branch: `main`
- Folder: `/(root)`
- Save

## 5. Verify harleyhardin.me in GitHub

GitHub profile picture > Settings > Pages > Add a domain

Enter:

`harleyhardin.me`

GitHub will give you a TXT record. Keep that page open.

In GoDaddy:

Domain Portfolio > harleyhardin.me > DNS > Add New Record

Create a TXT record using exactly the **Name** and **Value** GitHub gives you. GoDaddy's Name field is the host/prefix without the domain name. Leave TTL at its default unless you have a reason to change it.

After the TXT record resolves, return to GitHub and click Verify. Leave the TXT record in DNS afterward.

## 6. Attach the domain to the repository

Repository > Settings > Pages > Custom domain

Enter:

`harleyhardin.me`

Save it.

This project already contains a `CNAME` file with `harleyhardin.me`.

## 7. Point the GoDaddy domain to GitHub Pages

In GoDaddy DNS, remove/replace any conflicting website-hosting records for the root `@` or `www` that would point the site elsewhere. Do not remove MX/TXT records used by email or unrelated services.

Add these four A records:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

Then add:

| Type | Name | Value |
| --- | --- | --- |
| CNAME | www | HarleyHardin.github.io |

Do **not** create a wildcard `*` record for GitHub Pages.

## 8. Check DNS from Kali

```bash
dig harleyhardin.me +noall +answer -t A
dig www.harleyhardin.me +noall +answer
```

The first command should eventually show the four GitHub Pages IPv4 addresses. The second should show `www.harleyhardin.me` pointing to your GitHub Pages hostname.

DNS changes may not appear everywhere immediately.

## 9. Enable HTTPS

Once GitHub has issued the certificate:

Repository > Settings > Pages > Enforce HTTPS

Enable it.

## 10. Future updates

Whenever you edit the site locally:

```bash
git add .
git commit -m "Update portfolio"
git push
```

GitHub Pages will publish from `main` automatically.
