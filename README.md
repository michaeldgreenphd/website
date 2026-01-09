# Michael D. Green, PhD - Personal Website

A clean, professional website with a medical/health sciences aesthetic built with HTML, CSS, and vanilla JavaScript.

## Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Medical Aesthetic**: Clean, professional design with your signature green color (#2E7D32)
- **Tab Navigation**: Six main sections (Home, Research, Publications, CV, Media & Outreach, Contact)
- **ORCID Integration**: Automatic publication fetching from your ORCID profile (0000-0002-4982-8154)
- **Substack Integration**: Automatic blog post fetching from Not Being Green (notbeinggreen.com)
- **Smooth Animations**: Subtle transitions and hover effects
- **Accessibility**: Semantic HTML and ARIA labels for better accessibility

## Customization Checklist

### Immediate Updates Needed

1. **Profile Photo** (Line 261)
   - Replace the placeholder with your actual photo
   - Add your photo file to the website directory
   - Update line 261: Replace `<span>MDG</span>` with:
     ```html
     <img src="your-photo.jpg" alt="Michael D. Green, PhD" class="profile-image">
     ```

2. **Education Section** (Lines 635-652)
   - Add your actual Master's and Bachelor's degree details
   - Include institution names, years, and any relevant details

3. **Contact Information** (Lines 744-763)
   - Update email address (replace `your.email@jhu.edu`)
   - Add your actual Google Scholar profile URL
   - Add your LinkedIn profile URL
   - Add your Twitter/X handle if applicable

4. **Publications** - ✅ **Already Integrated!**
   - Your publications are automatically fetched from your ORCID profile
   - The Publications tab uses the ORCID API to display all your works
   - Sorted by year (newest first) with journal names, DOI links, and publication types
   - No manual updates needed - it syncs with your ORCID profile!

5. **Substack Blog** - ✅ **Already Integrated!**
   - Your recent blog posts are automatically fetched from Not Being Green (notbeinggreen.com)
   - Shows the 5 most recent posts with titles, dates, and excerpts
   - Links directly to your Substack for full posts
   - No manual updates needed!

6. **Media Appearances** (Lines 702-710)
   - Add your actual media appearances and interviews
   - Remove placeholder text when you add real content

7. **CV PDF** (Line 584)
   - Upload your CV PDF to the website directory
   - Ensure the filename matches or update the link

### Optional Enhancements

- Add more specific awards and honors in the CV section
- Expand the research publications list
- Add conference presentations
- Include additional institutional details

## Color Scheme

The website uses your signature green color:
- **Primary Green**: #2E7D32
- **Light Green**: #4CAF50 (accents)
- **Accent Blue**: #1976D2 (links in media section)

To change colors, update the CSS variables in the `:root` section (lines 10-18).

## ORCID Integration

The website automatically fetches and displays your publications from your ORCID profile.

### How It Works

- **ORCID ID**: 0000-0002-4982-8154
- **API**: Uses the public ORCID API (https://pub.orcid.org/v3.0)
- **Display**: Publications are shown with title, year, journal, type, and DOI links
- **Sorting**: Automatically sorted by publication year (newest first)
- **No Maintenance**: Whenever you update your ORCID profile, the website reflects those changes automatically

### Features

- Official ORCID badge with direct link to your profile
- Loading animation while fetching data
- Error handling with fallback to direct ORCID profile link
- Clean, medical-themed styling matching the rest of the site
- Mobile-responsive design
- Direct DOI links to each publication

### Changing ORCID ID

If you need to update the ORCID ID (though your current ID is already set):
1. Find the JavaScript section at the bottom of `index.html`
2. Locate the line: `const ORCID_ID = '0000-0002-4982-8154';`
3. Replace with your ORCID ID

## Substack Integration

The website automatically fetches and displays your recent blog posts from your Substack publication.

### How It Works

- **Substack URL**: notbeinggreen.com
- **Feed**: Uses the Substack RSS feed
- **Display**: Shows the 5 most recent posts with title, date, excerpt, and link
- **API**: Uses RSS2JSON API to convert RSS to JSON format
- **No Maintenance**: Automatically updates when you publish new posts on Substack

### Features

- Displays post title with clickable link
- Publication date formatted nicely
- 200-character excerpt of each post
- "Read full post" links to your Substack
- Loading animation while fetching
- Error handling with direct Substack link fallback
- Prominent Substack badge linking to your blog

### Changing Substack URL

If you need to update the Substack URL:
1. Find the JavaScript section at the bottom of `index.html`
2. Locate the line: `const SUBSTACK_URL = 'notbeinggreen.com';`
3. Replace with your Substack domain

## File Structure

```
website/
├── index.html          # Main website file (single-page application)
├── cv.pdf             # Your CV (add this file)
├── your-photo.jpg     # Your profile photo (add this file)
└── README.md          # This file
```

## Deployment to Squarespace

Since you own your domain through Squarespace, you have a few options:

### Option 1: Code Injection (Easiest)
1. In Squarespace, go to Settings → Advanced → Code Injection
2. Paste the entire HTML into the Header section
3. Note: This method has limitations with Squarespace

### Option 2: Code Block
1. Create a new blank page in Squarespace
2. Add a Code Block
3. Paste the HTML content
4. Set this as your homepage

### Option 3: External Hosting + Domain Pointing
1. Host this HTML file on GitHub Pages, Netlify, or Vercel (free options)
2. Point your michaeldgreen.phd domain to the hosted site
3. This gives you full control

### Recommended: Option 3 with GitHub Pages

1. Create a GitHub account if you don't have one
2. Create a new repository called `michaeldgreen.github.io`
3. Upload your `index.html` and other files
4. Enable GitHub Pages in repository settings
5. Point your domain to GitHub Pages

## Future Enhancements

The following features can be added in future updates:

1. **Google Scholar Integration**: Display citation metrics and additional publication details ✨
2. **Comment System**: Add a commenting system for blog engagement ✨

### ✅ Already Implemented

- **ORCID Publication Integration**: Automatically fetches and displays all publications from your ORCID profile with DOI links, journal names, and publication years
- **Substack Blog Integration**: Automatically displays your 5 most recent posts from Not Being Green with titles, dates, excerpts, and links

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Questions?

This website is built with standard HTML/CSS/JavaScript, so any web developer can help you customize it further if needed.

## License

Personal website - All rights reserved.
