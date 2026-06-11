# GitHub Pages Setup Guide

This guide will help you deploy your website to GitHub Pages and connect it to your custom domain `michaeldgreen.phd`.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in (or create an account)
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository: `website` (or any name you prefer)
5. Make it **Public**
6. Click "Create repository"

## Step 2: Upload Your Website Files

### Option A: Using GitHub Web Interface (Easiest)

1. In your new repository, click "uploading an existing file"
2. Drag and drop these files:
   - `index.html`
   - `README.md`
   - (Add your `cv.pdf` and profile photo when ready)
3. Click "Commit changes"

### Option B: Using Git Command Line

If you already have the files locally:

```bash
git remote add origin https://github.com/YOUR_USERNAME/website.git
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. In your repository, click **Settings** (gear icon)
2. Scroll down to **Pages** in the left sidebar
3. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait a few minutes for deployment

Your site will be available at: `https://YOUR_USERNAME.github.io/website/`

## Step 4: Connect Your Custom Domain

### In GitHub:

1. Still in Settings → Pages
2. Under "Custom domain", enter: `michaeldgreen.phd`
3. Click **Save**
4. Check "Enforce HTTPS" (after DNS propagates)

### In Squarespace:

1. Log in to your Squarespace account
2. Go to **Settings** → **Domains**
3. Click on `michaeldgreen.phd`
4. Click **DNS Settings**
5. Add these DNS records:

#### A Records (point to GitHub Pages):
```
Type: A
Name: @
Value: 185.199.108.153

Type: A
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153
```

#### CNAME Record (for www subdomain):
```
Type: CNAME
Name: www
Value: YOUR_USERNAME.github.io
```

6. Save the DNS settings

### Important Notes:

- DNS changes can take 24-48 hours to fully propagate
- You might see a "DNS check unsuccessful" message initially - this is normal
- After DNS propagates, enable "Enforce HTTPS" in GitHub Pages settings

## Step 5: Verify Your Website

1. Wait about 10-20 minutes after setting up
2. Visit `https://michaeldgreen.phd`
3. Your website should load!

## Alternative: Simpler GitHub Pages Setup

If you want an even simpler URL without connecting your custom domain yet:

1. Name your repository: `YOUR_USERNAME.github.io`
2. Upload `index.html` to the root
3. Your site will automatically be at: `https://YOUR_USERNAME.github.io`

Then you can add the custom domain later following Step 4.

## Updating Your Website

Whenever you want to update your website:

### Via Web Interface:
1. Go to your repository on GitHub
2. Click on the file you want to edit (e.g., `index.html`)
3. Click the pencil icon (Edit)
4. Make your changes
5. Commit changes

### Via Git Command Line:
```bash
# Make changes to your files
git add .
git commit -m "Update website content"
git push origin main
```

Changes will appear on your live site within a few minutes!

## Troubleshooting

### Site not loading?
- Check that GitHub Pages is enabled in Settings → Pages
- Verify DNS settings are correct (use a DNS checker online)
- Wait 24-48 hours for DNS propagation

### HTTPS not working?
- Make sure "Enforce HTTPS" is checked in GitHub Pages settings
- DNS must be fully propagated first
- Try clearing your browser cache

### Publications not showing?
- The ORCID API requires an internet connection
- Check browser console (F12) for any errors
- Verify your ORCID profile is public

## Need Help?

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Community Forum](https://github.community/)
- Your repository Issues tab for tracking problems

## Your Current Setup

- **Website files**: Ready in `/home/user/website/`
- **ORCID integration**: Already configured with ID 0000-0002-4982-8154
- **Custom domain**: michaeldgreen.phd (owned via Squarespace)
- **Hosting**: Free via GitHub Pages

Once deployed, your website will automatically fetch publications from ORCID whenever visitors load the Publications page!
