# 🔑 API KEY SETUP GUIDE
## Compression & Google Drive Integration

This guide shows how to set up API keys for the exhibit generator tools.

---

## 📦 WHAT NEEDS API KEYS?

### **Optional (Compression - Tier 3)**:
- SmallPDF API (for premium PDF compression)
- **Cost**: $12/month for 5,000 pages
- **When to use**: For highest quality compression or when free methods fail

### **Optional (Google Drive)**:
- Google Drive API (for folder access from Streamlit)
- **Cost**: FREE
- **When to use**: If using Streamlit version with Drive integration

### **Not Required**:
- Google Apps Script version (uses your Google account automatically)
- Free compression (Ghostscript + PyMuPDF work without API keys)

---

## 🎯 COMPRESSION: Do You Need It?

### **Most Users: NO API KEY NEEDED!**

The compression system has **3 tiers**:

1. **Ghostscript** (FREE) - 60-90% compression
   - Best compression ratio
   - USCIS-compliant quality
   - Install once, use forever
   - **Recommended for most users**

2. **PyMuPDF** (FREE) - 30-60% compression
   - Automatic fallback
   - Good quality
   - Already in requirements.txt
   - **No setup needed**

3. **SmallPDF API** (PAID) - 40-80% compression
   - Premium quality guarantee
   - $12/month for 5,000 pages
   - **Only if you want guaranteed quality**

### **Decision Tree**:

```
Do you need compression? → Install Ghostscript (FREE, see below)
   ↓
Ghostscript working? → You're done! No API key needed.
   ↓
Want premium guarantee? → Get SmallPDF API key (optional)
```

---

## 🛠️ OPTION 1: FREE COMPRESSION SETUP (Recommended)

### **Install Ghostscript** (takes 2 minutes)

#### **Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install ghostscript
```

#### **macOS**:
```bash
brew install ghostscript
```

#### **Windows**:
1. Download: https://ghostscript.com/releases/gsdnld.html
2. Run installer
3. Add to PATH (installer does this automatically)

#### **Verify Installation**:
```bash
gs --version
```

Should show: `GPL Ghostscript 9.50` (or higher)

### **That's It!**
No API keys, no monthly fees. Just works.

---

## 💳 OPTION 2: SmallPDF API (Premium - Optional)

### **When to Use**:
- You process >100 petitions/month
- You need guaranteed consistent quality
- Ghostscript isn't available on your system
- You want API-based processing

### **Sign Up**:

1. Go to: https://smallpdf.com/developers
2. Click "Get API Access"
3. Choose plan:
   - **Starter**: $12/month (5,000 pages)
   - **Professional**: $49/month (25,000 pages)
4. Get your API key

### **Add to Streamlit**:

#### **Option A: Environment Variable** (Recommended)
```bash
# Linux/Mac
export SMALLPDF_API_KEY="your-api-key-here"

# Windows
set SMALLPDF_API_KEY=your-api-key-here
```

#### **Option B: .env File**
Create `.env` file in `streamlit-exhibit-generator/`:
```
SMALLPDF_API_KEY=your-api-key-here
```

Then in your code:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('SMALLPDF_API_KEY')
```

#### **Option C: Streamlit Secrets** (For Cloud Deployment)
Create `.streamlit/secrets.toml`:
```toml
SMALLPDF_API_KEY = "your-api-key-here"
```

Access in app:
```python
import streamlit as st
api_key = st.secrets["SMALLPDF_API_KEY"]
```

### **Add to Google Apps Script**:

In `Code.gs`, add at the top:
```javascript
// Configuration
const SMALLPDF_API_KEY = 'your-api-key-here';

// Or use Script Properties (more secure):
function setApiKey() {
  PropertiesService.getScriptProperties()
    .setProperty('SMALLPDF_API_KEY', 'your-api-key-here');
}

function getApiKey() {
  return PropertiesService.getScriptProperties()
    .getProperty('SMALLPDF_API_KEY');
}
```

---

## 🔐 GOOGLE DRIVE API SETUP (Streamlit Only)

**Note**: Google Apps Script version doesn't need this (uses your Google account automatically)

### **Step 1: Create Google Cloud Project**

1. Go to: https://console.cloud.google.com
2. Create new project: "Visa Exhibit Generator"
3. Note the Project ID

### **Step 2: Enable Google Drive API**

1. In Cloud Console → "APIs & Services" → "Library"
2. Search "Google Drive API"
3. Click "Enable"

### **Step 3: Create OAuth Credentials**

1. "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Visa Exhibit Generator Desktop"
5. Click "Create"
6. Download JSON file

### **Step 4: Add Credentials to Streamlit**

1. Rename downloaded file to `credentials.json`
2. Move to: `streamlit-exhibit-generator/credentials.json`
3. **Add to .gitignore** (keep private!)

```bash
echo "credentials.json" >> .gitignore
```

### **Step 5: First Run (Authorization)**

When you run the Streamlit app and use Google Drive:

1. Browser will open
2. Sign in with your Google account
3. Click "Allow"
4. Token saved to `token.json`
5. **Done!** No need to re-authorize

---

## 🔒 SECURITY BEST PRACTICES

### **1. Never Commit API Keys to Git**

```bash
# Add to .gitignore
echo "*.env" >> .gitignore
echo "credentials*.json" >> .gitignore
echo "token*.json" >> .gitignore
echo "SMALLPDF_API_KEY" >> .gitignore
```

### **2. Use Environment Variables**

**Good**:
```python
import os
api_key = os.getenv('SMALLPDF_API_KEY')
```

**Bad**:
```python
api_key = "pk_12345abcde"  # NEVER DO THIS!
```

### **3. Rotate Keys Regularly**

- Change SmallPDF API key every 3-6 months
- Revoke old keys after updating

### **4. Use Separate Keys for Dev/Production**

- Development: Test key with low limits
- Production: Full key with higher limits

---

## ✅ VERIFICATION CHECKLIST

### **Free Compression (Ghostscript)**:
- [ ] Ghostscript installed (`gs --version` works)
- [ ] PyMuPDF in requirements.txt
- [ ] No API key needed

### **Premium Compression (SmallPDF)**:
- [ ] Signed up at smallpdf.com/developers
- [ ] API key obtained
- [ ] Key added to environment variable or .env
- [ ] Key NOT committed to git
- [ ] Test compression works

### **Google Drive (Streamlit)**:
- [ ] Google Cloud project created
- [ ] Drive API enabled
- [ ] OAuth credentials downloaded
- [ ] credentials.json in correct location
- [ ] credentials.json in .gitignore
- [ ] First authorization completed
- [ ] token.json generated

---

## 🧪 TESTING YOUR SETUP

### **Test Compression (Free)**:

```bash
cd streamlit-exhibit-generator
python3 << EOF
from compress_handler import USCISPDFCompressor

compressor = USCISPDFCompressor(quality_preset='high')
print("✓ Compression handler loaded")

# Check Ghostscript
if compressor._check_ghostscript():
    print("✓ Ghostscript available")
else:
    print("✗ Ghostscript not found - install it")
EOF
```

### **Test Compression (SmallPDF)**:

```bash
cd streamlit-exhibit-generator
python3 << EOF
import os
from compress_handler import USCISPDFCompressor

api_key = os.getenv('SMALLPDF_API_KEY')
if api_key:
    print(f"✓ SmallPDF API key found: {api_key[:10]}...")
    compressor = USCISPDFCompressor(
        quality_preset='high',
        smallpdf_api_key=api_key
    )
    print("✓ SmallPDF compression available")
else:
    print("✗ SMALLPDF_API_KEY not set")
EOF
```

### **Test Google Drive**:

```bash
cd streamlit-exhibit-generator
python3 << EOF
from google_drive import GoogleDriveHandler

try:
    drive = GoogleDriveHandler()
    print("✓ Google Drive handler initialized")
except FileNotFoundError:
    print("✗ credentials.json not found")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

---

## 💰 COST COMPARISON

### **Monthly Processing: 10 Petitions (2,000 pages)**

| Setup | Cost | Notes |
|-------|------|-------|
| **Ghostscript + PyMuPDF** | $0 | Free forever, requires installation |
| **SmallPDF Starter** | $12 | 5,000 pages/month included |
| **SmallPDF Pro** | $49 | 25,000 pages/month included |
| **Google Drive API** | $0 | Free (no quota limits for this use) |

### **Recommendation**:
- **Start with**: Ghostscript (FREE)
- **Upgrade to**: SmallPDF if you process 50+ petitions/month
- **Google Drive**: Free for all users

---

## 🚨 TROUBLESHOOTING

### **"Ghostscript not found"**

**Solution**:
```bash
# Check installation
which gs

# If not found, install:
# Ubuntu: sudo apt-get install ghostscript
# Mac: brew install ghostscript
# Windows: Download from ghostscript.com
```

### **"SmallPDF API authentication failed"**

**Solution**:
1. Check API key is correct
2. Verify key is active at smallpdf.com/developers
3. Check monthly page limit not exceeded
4. Ensure key has correct permissions

### **"Google Drive credentials invalid"**

**Solution**:
1. Delete `token.json`
2. Re-run authorization flow
3. Check credentials.json is valid
4. Verify Drive API is enabled in Cloud Console

### **"Module not found: compress_handler"**

**Solution**:
```bash
# Make sure you're in correct directory
cd streamlit-exhibit-generator

# Verify file exists
ls compress_handler.py

# Should show: compress_handler.py
```

---

## 📚 ADDITIONAL RESOURCES

### **Ghostscript**:
- Homepage: https://ghostscript.com
- Documentation: https://ghostscript.com/documentation.html
- Installation: https://ghostscript.com/releases/gsdnld.html

### **SmallPDF API**:
- Developer Portal: https://smallpdf.com/developers
- API Docs: https://developers.smallpdf.com
- Pricing: https://smallpdf.com/pricing

### **Google Drive API**:
- Documentation: https://developers.google.com/drive
- Python Quickstart: https://developers.google.com/drive/api/quickstart/python
- OAuth Guide: https://developers.google.com/identity/protocols/oauth2

---

## 🎯 QUICK START (TL;DR)

### **For Most Users**:
```bash
# Install Ghostscript (FREE)
sudo apt-get install ghostscript  # Ubuntu
brew install ghostscript          # Mac

# Install Python dependencies
pip install -r requirements.txt

# Done! Compression works without API keys.
```

### **For Premium Users**:
```bash
# Get SmallPDF API key
# https://smallpdf.com/developers

# Set environment variable
export SMALLPDF_API_KEY="your-key"

# Run Streamlit
streamlit run app.py
```

### **For Google Drive Access**:
```bash
# Enable Drive API in Cloud Console
# Download credentials.json
# Place in streamlit-exhibit-generator/
# First run will prompt for authorization
# Done!
```

---

**Questions?** Check the README files in each tool folder or open an issue on GitHub.

**Security Concern?** Never commit API keys. Use environment variables or .env files listed in .gitignore.

**Cost Concern?** Start with free Ghostscript compression. Only add SmallPDF if you need premium features.
