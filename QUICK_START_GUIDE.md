# Visa Exhibit Generator - Quick Start Guide

**Two powerful tools for creating professional numbered exhibit packages from Google Drive folders.**

## 📂 What's Included

This folder contains **TWO complete applications** plus a **production example PDF** (32 MB compressed file showing real visa petition structure):

### 1. **Streamlit Version** (Python)
`streamlit-exhibit-generator/`
- Full-featured Python web app
- Local PDF processing (no API costs)
- Unlimited file sizes
- Google Drive integration
- Archive.org preservation

### 2. **Google Apps Script Version** (Native Drive)
`google-apps-script-exhibit-generator/`
- Native Google Workspace integration
- Zero installation required
- No authentication needed
- Free hosting on Google
- Perfect for Drive-only workflows

## 🚀 Which One Should I Use?

| Use Case | Recommended Tool |
|----------|------------------|
| Files already in Google Drive | **Google Apps Script** |
| Need to process 100+ large files | **Streamlit** |
| Want zero infrastructure | **Google Apps Script** |
| Need archive.org preservation | **Streamlit** |
| Team of Google Workspace users | **Google Apps Script** |
| Need advanced PDF manipulation | **Streamlit** |

**Best Approach**: Use **Google Apps Script** for quick daily work, **Streamlit** for complex cases.

---

## Option 1: Google Apps Script (Fastest to Start)

### ⏱️ 5-Minute Setup

**1. Create Apps Script Project**
```
1. Go to script.google.com
2. New Project
3. Name it "Visa Exhibit Generator"
```

**2. Copy Files**
```
Copy contents from google-apps-script-exhibit-generator/:
- Code.gs → Replace default code
- Index.html → Add as HTML file
- appsscript.json → Replace manifest
```

**3. Deploy**
```
1. Deploy → New deployment → Web app
2. Execute as: Me
3. Who has access: Anyone
4. Deploy → Authorize → Allow
5. Copy web app URL
```

**4. Use**
```
1. Open web app URL
2. Paste Drive folder URL
3. Configure options
4. Generate!
```

### ✅ Ready to Use Features

- ✅ Native Drive access (no auth needed)
- ✅ Automatic exhibit numbering
- ✅ Table of Contents generation
- ✅ Recursive folder processing
- ✅ Zero infrastructure cost

### 📖 Full Instructions
See `google-apps-script-exhibit-generator/README.md`

---

## Option 2: Streamlit (More Power)

### ⏱️ 10-Minute Setup

**1. Install Dependencies**
```bash
cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator"
pip install -r requirements.txt
```

**2. Run Application**
```bash
streamlit run app.py
```

**3. Use in Browser**
```
App opens at: http://localhost:8501

Upload Files → Add URLs → Import from Drive → Generate
```

### ✅ Ready to Use Features

- ✅ Direct file uploads
- ✅ ZIP/folder batch processing
- ✅ Google Drive import (with credentials)
- ✅ Archive.org preservation
- ✅ Professional PDF manipulation
- ✅ Multiple numbering styles

### 📖 Full Instructions
See `streamlit-exhibit-generator/README.md`

---

## 🎯 Quick Comparison

| Feature | Google Apps Script | Streamlit |
|---------|-------------------|-----------|
| **Setup Time** | 5 minutes | 10 minutes |
| **Installation** | None | Python + packages |
| **Drive Integration** | Native | Needs credentials |
| **File Size Limit** | 50 MB/file | Unlimited |
| **Execution Time** | 6 minutes max | Unlimited |
| **PDF Merging** | Links document | True PDF merge |
| **Cost per Use** | $0 | $0 |
| **Hosting** | Free (Google) | Local or cloud |
| **Best For** | Quick daily use | Complex cases |

---

## 📋 Common Workflows

### Workflow 1: Simple Drive Folder → Exhibits

**Use: Google Apps Script**

1. Organize PDFs in Drive folder
2. Open web app
3. Paste folder URL
4. Click "Generate"
5. Get numbered exhibits in new folder

**Time**: 2 minutes

---

### Workflow 2: Mixed Sources (PDFs + URLs) → Package

**Use: Streamlit**

1. Upload local PDFs (Tab 1)
2. Add URLs for archiving (Tab 2)
3. Import Drive folder (Tab 3)
4. Generate merged package (Tab 4)
5. Download complete PDF

**Time**: 5 minutes

---

### Workflow 3: Large Batch (200+ Files)

**Use: Streamlit**

1. Export Drive folder as ZIP
2. Upload ZIP to Streamlit
3. Generate with progress tracking
4. Download merged PDF

**Time**: 10-15 minutes

---

## 🔑 API Keys (Optional)

Both tools can work **without API keys**, but these enhance functionality:

### For Archive.org Integration
- **Service**: archive.org Wayback Machine
- **Cost**: FREE (no key needed)
- **Used in**: Streamlit only
- **Purpose**: Preserve URLs long-term

### For URL to PDF Conversion
- **Service**: API2PDF
- **Cost**: $0.001/page
- **Get key**: https://api2pdf.com
- **Used in**: Both (optional)
- **Purpose**: Convert web pages to PDFs

### For Google Drive (Streamlit only)
- **Service**: Google Cloud
- **Cost**: FREE
- **Setup**: Service account JSON
- **Get it**: https://console.cloud.google.com
- **Purpose**: Access Drive folders

**Note**: Google Apps Script needs NO keys (native integration)

---

## 📁 Example: End-to-End Process

### Starting with Google Drive Folder

**Your Drive Structure:**
```
Smith_O1_Evidence/
├── CV_Resume.pdf
├── Awards/
│   ├── Award_2021.pdf
│   └── Award_2022.pdf
├── Publications/
│   ├── Paper_Nature_2023.pdf
│   ├── Paper_Science_2022.pdf
│   └── Paper_Cell_2021.pdf
└── Letters/
    ├── Letter_MIT.pdf
    └── Letter_Stanford.pdf
```

**Using Google Apps Script:**

1. Go to web app
2. Paste folder URL
3. Options:
   - Case Name: "Smith_O1A_2024"
   - Numbering: Letters (A, B, C...)
   - Include subfolders: ✅
   - Include TOC: ✅
4. Click "Generate"

**Output:**
```
Smith_O1A_2024/
├── Exhibit_A_CV_Resume.pdf
├── Exhibit_B_Award_2021.pdf
├── Exhibit_C_Award_2022.pdf
├── Exhibit_D_Paper_Nature_2023.pdf
├── Exhibit_E_Paper_Science_2022.pdf
├── Exhibit_F_Paper_Cell_2021.pdf
├── Exhibit_G_Letter_MIT.pdf
├── Exhibit_H_Letter_Stanford.pdf
├── Smith_O1A_2024_Table_of_Contents (Google Doc)
└── Smith_O1A_2024_Complete_Package (Google Doc)
```

**Time**: 2-3 minutes
**Files**: 8 numbered exhibits + 2 docs

---

## 🎓 Tips & Best Practices

### File Organization

**Before generation:**
1. Name files clearly (they appear in TOC)
2. Remove duplicates
3. Organize in logical order (alphabetically)
4. Use subfolders for categories

**Example naming:**
```
✅ Good:
- 01_Resume_John_Smith.pdf
- 02_Award_Nobel_Prize_2023.pdf
- 03_Publication_Nature_Cancer_2023.pdf

❌ Bad:
- resume.pdf
- award.pdf
- pub1.pdf
```

### Numbering Strategies

| Visa Type | Recommended Style | Reason |
|-----------|------------------|--------|
| O-1A/O-1B | Letters (A, B, C...) | Standard USCIS format |
| EB-1A | Letters (A, B, C...) | Matches legal briefs |
| P-1A | Numbers (1, 2, 3...) | Simpler for athletics |

### Batch Processing

**For 50+ exhibits:**
1. Test with 5-10 files first
2. Verify numbering is correct
3. Process full batch
4. Review TOC before submission

---

## 🆘 Troubleshooting

### Google Apps Script Issues

**"Folder not found"**
- Solution: Check folder URL, verify access

**"Script timeout"**
- Solution: Process in smaller batches (< 100 files)

**"No PDFs found"**
- Solution: Enable "Include subfolders" option

### Streamlit Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**Google Drive not working**
- Solution: Upload service account JSON in sidebar

**Large files slow**
- Solution: Normal for 100+ MB files, monitor progress

---

## 📊 Cost Analysis

### Google Apps Script
- Hosting: **$0** (Google infrastructure)
- Execution: **$0** (free tier)
- Storage: Uses your Drive quota
- **Total per generation: $0**

### Streamlit
- Hosting: **$0** (local) or **$0** (Streamlit Cloud free)
- PDF processing: **$0** (local libraries)
- Optional APIs: $0.05-0.15 (if using API2PDF)
- **Total per generation: $0-0.15**

---

## 🚀 Next Steps

### You're Ready!

**Choose your tool:**
- ✅ **Quick start**: Google Apps Script (5 min)
- ✅ **Full features**: Streamlit (10 min)
- ✅ **Both**: Use each for different scenarios

### Getting Started

1. **Pick a tool** from above
2. **Follow setup** in respective README
3. **Test with examples** in `Examples of Single PDFs/`
4. **Generate real cases**

### Example Files

Test with production examples:
```
Examples of Single PDFs/
├── Charles P-1 final PDF.pdf (13 MB)
├── Dhyan Patel P-1S Single PDF.pdf (6.6 MB)
├── Dylan Final Single PDF.pdf (6 MB)
└── [3 more examples]
```

---

## 📚 Documentation

**Full Documentation:**
- Google Apps Script: `google-apps-script-exhibit-generator/README.md`
- Streamlit: `streamlit-exhibit-generator/README.md`

**Code Reference:**
- Existing exhibit logic: `../mega-internal-v1-visa-tool/app/lib/exhibit-generator.ts`
- Archive.org integration: `../mega-internal-v1-visa-tool/app/lib/archive-org.ts`

---

## 💡 Pro Tips

1. **Use Google Apps Script for 90% of cases** (fastest, zero setup)
2. **Use Streamlit when you need**:
   - Archive.org preservation
   - True PDF merging
   - Files > 50 MB
   - Batch 100+ exhibits
3. **Keep files organized in Drive** for both tools
4. **Test with small batch first** before processing 100+ files
5. **Save exhibit configurations** for repeat clients

---

**Built**: November 2025
**Status**: Production Ready
**Support**: Both tools fully documented and tested

**Happy Generating! 📄✨**
