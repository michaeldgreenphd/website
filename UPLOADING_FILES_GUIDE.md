# Guide: Uploading PDFs and Images to GitHub

This guide explains how to upload your manuscript PDFs and images to your GitHub repository so they appear on your website.

## File Structure

Your website expects files to be organized like this:

```
website/
├── index.html
├── published-manuscripts.html
├── manuscripts/
│   └── pdf/
│       ├── 01-cardiac-biomarkers-pediatric.pdf
│       ├── 02-black-participation-clinical-trials.pdf
│       ├── 03-discrimination-hypertension-education.pdf
│       ├── 04-discrimination-blood-pressure.pdf
│       ├── 05-ses-disadvantage-hf-admissions.pdf
│       ├── 06-hlhs-family-qualitative.pdf
│       ├── 07-cvd-risk-factor-disparities.pdf
│       ├── 08-hf-hospitalization-disparities.pdf
│       ├── 09-perceived-discrimination-factors.pdf
│       ├── 10-inclusive-pedagogy-mixed-methods.pdf
│       ├── 11-parental-discrimination-measure.pdf
│       ├── 12-trump-diversity-opinion.pdf
│       └── 13-cardiovascular-multimorbidity.pdf
├── images/
│   ├── profile-photo.jpg
│   └── [other images]
└── cv.pdf
```

## Method 1: Upload via GitHub Web Interface (Easiest)

### Step 1: Create the manuscripts/pdf folder

1. Go to your repository: `https://github.com/michaeldgreenphd/website`
2. Click **Add file** → **Create new file**
3. In the filename box, type: `manuscripts/pdf/placeholder.txt`
   - This creates both folders at once
4. Add some text like "PDF files go here"
5. Click **Commit changes**

### Step 2: Upload your PDFs

1. Navigate to the `manuscripts/pdf/` folder in your repository
2. Click **Add file** → **Upload files**
3. Drag and drop your PDF files (or click to browse)
4. **IMPORTANT**: Rename your PDFs to match these exact names:
   - `01-cardiac-biomarkers-pediatric.pdf`
   - `02-black-participation-clinical-trials.pdf`
   - `03-discrimination-hypertension-education.pdf`
   - `04-discrimination-blood-pressure.pdf`
   - `05-ses-disadvantage-hf-admissions.pdf`
   - `06-hlhs-family-qualitative.pdf`
   - `07-cvd-risk-factor-disparities.pdf`
   - `08-hf-hospitalization-disparities.pdf`
   - `09-perceived-discrimination-factors.pdf`
   - `10-inclusive-pedagogy-mixed-methods.pdf`
   - `11-parental-discrimination-measure.pdf`
   - `12-trump-diversity-opinion.pdf`
   - `13-cardiovascular-multimorbidity.pdf`
5. Click **Commit changes**

### Step 3: Upload your profile photo

1. Go to the root of your repository
2. Click **Add file** → **Upload files**
3. Upload your profile photo (name it `profile-photo.jpg` or similar)
4. Click **Commit changes**

### Step 4: Update index.html to use your photo

1. In your repository, click on `index.html`
2. Click the pencil icon (Edit)
3. Find line 800 (or search for "MDG")
4. Replace:
   ```html
   <span>MDG</span>
   ```
   with:
   ```html
   <img src="profile-photo.jpg" alt="Michael D. Green, PhD" class="profile-image">
   ```
5. Click **Commit changes**

## Method 2: Upload via Git Command Line

If you're comfortable with Git:

```bash
# Navigate to your website directory
cd /home/user/website

# Create the folders
mkdir -p manuscripts/pdf
mkdir -p images

# Copy your PDFs to the manuscripts/pdf folder
# (Make sure they're named correctly as listed above)
cp /path/to/your/pdfs/*.pdf manuscripts/pdf/

# Copy your images
cp /path/to/your/profile-photo.jpg images/profile-photo.jpg

# Add all files
git add manuscripts/ images/

# Commit
git commit -m "Add manuscript PDFs and profile photo"

# Push to GitHub
git push origin claude/redesign-website-aesthetic-hHmN9
```

## Important Notes on File Naming

### PDF Files
- **Use lowercase letters and dashes** (not spaces or underscores)
- **Start with the number** (01, 02, 03, etc.) for proper ordering
- **Be descriptive but concise** in the name
- The filenames are already set in `published-manuscripts.html`, so match them exactly

### Image Files
- **Accepted formats**: JPG, JPEG, PNG, GIF
- **Recommended size**:
  - Profile photo: 300x300px to 800x800px
  - Keep file size under 500KB for faster loading
- **Naming**: Use descriptive names like:
  - `profile-photo.jpg`
  - `research-project-1.jpg`
  - `conference-photo.jpg`

## How Links Work

When you upload a file to GitHub, it becomes accessible at:
```
https://michaeldgreenphd.github.io/website/manuscripts/pdf/01-cardiac-biomarkers-pediatric.pdf
```

The website automatically:
1. Looks in the `manuscripts/pdf/` folder
2. Finds the file with the exact name specified
3. Opens it in a new tab when clicked

## Testing Your Uploads

After uploading:

1. Wait 2-3 minutes for GitHub Pages to rebuild
2. Visit your published manuscripts page:
   ```
   https://michaeldgreenphd.github.io/website/published-manuscripts.html
   ```
3. Click on a manuscript title
4. The PDF should open in a new tab

If a PDF doesn't open:
- Check the filename matches exactly (including number prefix)
- Make sure it's in the `manuscripts/pdf/` folder
- Check the file isn't corrupted
- Clear your browser cache and try again

## Adding More PDFs Later

To add more manuscripts:

1. Upload the PDF to `manuscripts/pdf/`
2. Edit `published-manuscripts.html`
3. Add a new manuscript item following the existing format
4. Update the manuscript number
5. Commit your changes

## File Size Limits

- **GitHub**: Individual files up to 100MB
- **Recommended**: Keep PDFs under 10MB for faster loading
- If a PDF is very large, consider compressing it

## Need Help?

If you have trouble uploading files:
1. Check the GitHub documentation: https://docs.github.com/en/repositories/working-with-files
2. Make sure you're in the correct repository
3. Verify you have write access to the repository
4. Check that filenames don't have special characters

## Current Status

✅ Website structure created
✅ Published manuscripts page created
✅ All 13 manuscripts listed with proper formatting
⏳ PDFs need to be uploaded to `manuscripts/pdf/`
⏳ Profile photo needs to be uploaded and linked

Once you upload your PDFs, they'll be immediately accessible on your live website!
