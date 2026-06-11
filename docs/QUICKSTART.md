# Quick Start Guide

## Preview Your Website Locally RIGHT NOW

You can preview your website immediately by opening the HTML file in your browser:

### On macOS:
```bash
open index.html
```

### On Linux:
```bash
xdg-open index.html
```

### On Windows:
```bash
start index.html
```

Or simply:
1. Navigate to `/home/user/website/` in your file browser
2. Double-click `index.html`
3. It will open in your default browser

**Note**: The ORCID and Substack integrations require an internet connection to fetch data.

## Deploy to GitHub Pages (5 Minutes)

### Step 1: Create GitHub Account (if needed)
Go to [github.com](https://github.com) and sign up (it's free!)

### Step 2: Create Repository
1. Click the **+** icon (top right) → **New repository**
2. Repository name: `website` (or any name)
3. Make it **Public**
4. Click **Create repository**

### Step 3: Upload Files
1. In your new repository, click **uploading an existing file**
2. Drag and drop these files from `/home/user/website/`:
   - `index.html`
   - `README.md`
   - `GITHUB_PAGES_SETUP.md`
   - `QUICKSTART.md`
3. Click **Commit changes**

### Step 4: Enable GitHub Pages
1. In your repository, click **Settings** (⚙️ icon)
2. Click **Pages** in the left sidebar
3. Under "Source":
   - Branch: Select `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait 2-3 minutes

### Step 5: Visit Your Site!
Your website will be live at:
```
https://YOUR_USERNAME.github.io/website/
```

Replace `YOUR_USERNAME` with your GitHub username.

## Connect Your Custom Domain (Optional)

Once your site is live, you can connect `michaeldgreen.phd`:

1. In GitHub Settings → Pages, enter: `michaeldgreen.phd`
2. In Squarespace, update DNS records (see `GITHUB_PAGES_SETUP.md` for detailed instructions)
3. Wait 24-48 hours for DNS to propagate

## What's Already Working

✅ **Automatic Features** (no setup needed):
- ORCID publications from profile 0000-0002-4982-8154
- Substack posts from notbeinggreen.com
- Responsive mobile design
- Professional medical aesthetic

## What You Need to Add

📝 **Before going live, update**:
1. Your profile photo (line 665 in index.html)
2. Email address (line 1047)
3. Google Scholar link (line 1052)
4. LinkedIn profile (line 1057)
5. Twitter/X handle (line 1062)
6. Education details (lines 824-840)
7. Upload your CV PDF

## Testing the Integrations

### Test ORCID Integration:
1. Open your website
2. Click the **Publications** tab
3. Wait 2-3 seconds
4. Your publications should appear!

### Test Substack Integration:
1. Click the **Media & Outreach** tab
2. Scroll to "Recent Posts"
3. Wait 2-3 seconds
4. Your latest 5 blog posts should appear!

## Updating Your Website

Whenever you want to update:

1. Edit `index.html` locally
2. Go to your GitHub repository
3. Click on `index.html`
4. Click the pencil icon (Edit)
5. Paste your updated content
6. Click **Commit changes**
7. Wait 2-3 minutes for changes to go live

## Need Help?

- **Detailed GitHub Pages Setup**: See `GITHUB_PAGES_SETUP.md`
- **Customization Guide**: See `README.md`
- **GitHub Help**: [docs.github.com/pages](https://docs.github.com/pages)

## Your URLs

Once deployed:
- **GitHub Pages**: `https://YOUR_USERNAME.github.io/website/`
- **Custom Domain** (after DNS setup): `https://michaeldgreen.phd`
- **Substack**: `https://notbeinggreen.com`
- **ORCID**: `https://orcid.org/0000-0002-4982-8154`

---

🎉 **You're all set!** Your website has:
- ✅ Professional medical design
- ✅ Automatic ORCID publications
- ✅ Automatic Substack blog posts
- ✅ Mobile responsive
- ✅ Ready to deploy in 5 minutes
