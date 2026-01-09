# Michael D. Green, PhD - Personal Website

A clean, professional website with a medical/health sciences aesthetic built with HTML, CSS, and vanilla JavaScript.

## Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Medical Aesthetic**: Clean, professional design with your signature green color (#2E7D32)
- **Tab Navigation**: Five main sections (Home, Research, CV, Media & Outreach, Contact)
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

4. **Publications** (Lines 614-627)
   - Add your actual publications
   - Use the example format provided
   - This section is marked for future automatic updates

5. **Media Appearances** (Lines 702-710)
   - Add your actual media appearances and interviews
   - Remove placeholder text when you add real content

6. **CV PDF** (Line 584)
   - Upload your CV PDF to the website directory
   - Ensure the filename matches or update the link

7. **Substack Link** (Line 689)
   - Add your actual Substack URL

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

## Future Enhancements (Mentioned)

The following features are planned for future implementation:

1. **Automatic Substack Integration**: Pull latest blog posts automatically
2. **Research Article Auto-Update**: Connect to PubMed or similar API
3. **Google Scholar Integration**: Display publications directly from Google Scholar

These will require JavaScript APIs and/or backend services.

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Questions?

This website is built with standard HTML/CSS/JavaScript, so any web developer can help you customize it further if needed.

## License

Personal website - All rights reserved.
