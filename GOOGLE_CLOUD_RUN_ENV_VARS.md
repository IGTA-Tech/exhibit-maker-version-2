# 🔐 Google Cloud Run Environment Variables
## Complete Configuration for Visa Exhibit Maker Deployment

**Repository**: https://github.com/IGTA-Tech/visa-exhibit-maker
**Target Platform**: Google Cloud Run
**Last Updated**: December 3, 2025

---

## 📋 REQUIRED ENVIRONMENT VARIABLES

### **Core Application Settings**

```bash
# Application Environment
APP_ENV=production
PORT=8080
HOST=0.0.0.0

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8080
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

---

## 🔑 API KEYS & CREDENTIALS

### **1. Google Drive API** (Required for Drive Integration)

```bash
# Google Drive Service Account
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# OR as JSON string (recommended for Cloud Run)
GOOGLE_CREDENTIALS_JSON='{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}'

# Google Cloud Project
GOOGLE_CLOUD_PROJECT=your-project-id
```

**How to Get**:
1. Go to https://console.cloud.google.com
2. Create/select project
3. Enable Google Drive API
4. Create Service Account
5. Download JSON credentials

---

### **2. SmallPDF API** (Optional - Premium Compression)

```bash
# SmallPDF API Key
SMALLPDF_API_KEY=your-smallpdf-api-key-here
```

**Cost**: $12/month for 5,000 pages
**Get Key**: https://smallpdf.com/developers
**Required**: No (Free compression with Ghostscript/PyMuPDF works)

---

### **3. Supabase Database** (Optional - For Production Features)

```bash
# Supabase Connection
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Supabase Storage
SUPABASE_STORAGE_BUCKET=exhibit-packages

# Supabase Database (Direct Connection - Optional)
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
```

**Get Credentials**:
1. Go to https://app.supabase.com
2. Create new project
3. Go to Settings → API
4. Copy URL and keys

**Required**: No (App works standalone, but Supabase adds features)

---

## 🛠️ SYSTEM DEPENDENCIES

### **Ghostscript** (PDF Compression - Tier 1)

```bash
# Ghostscript Path (auto-detected if installed)
GHOSTSCRIPT_PATH=/usr/bin/gs

# Ghostscript Version Check
GS_VERSION_CHECK=true
```

**Installation in Dockerfile**:
```dockerfile
RUN apt-get update && apt-get install -y ghostscript
```

**Required**: Highly recommended for 60-90% PDF compression

---

## 🔒 SECURITY & SECRETS

### **Secret Keys**

```bash
# Session Secret (for Streamlit)
SECRET_KEY=your-random-secret-key-min-32-chars

# JWT Secret (if implementing auth)
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Generate Random Secret**:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📦 OPTIONAL INTEGRATIONS

### **Archive.org Integration** (URL Preservation)

```bash
# Archive.org (No API key needed - public service)
ARCHIVE_ORG_ENABLED=true
ARCHIVE_ORG_USER_AGENT=VisaExhibitGenerator/1.0
```

**Required**: No (Free service, no auth needed)

---

### **API2PDF** (URL to PDF Conversion - Optional)

```bash
# API2PDF Configuration
API2PDF_API_KEY=your-api2pdf-key
API2PDF_ENABLED=false
```

**Cost**: $0.001/page
**Get Key**: https://api2pdf.com
**Required**: No (Manual PDF uploads work fine)

---

## 📊 LOGGING & MONITORING

### **Application Logging**

```bash
# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Sentry Error Tracking (Optional)
SENTRY_DSN=your-sentry-dsn-here
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

---

### **Google Cloud Logging**

```bash
# Cloud Run automatically integrates with Cloud Logging
GOOGLE_CLOUD_LOGGING=true
GCP_PROJECT=your-project-id
```

---

## 💾 STORAGE & FILE HANDLING

### **Temporary File Storage**

```bash
# Temp Directory (Cloud Run uses /tmp)
TEMP_DIR=/tmp
MAX_UPLOAD_SIZE_MB=50

# File Cleanup
AUTO_CLEANUP_ENABLED=true
CLEANUP_AFTER_HOURS=1
```

---

### **Cloud Storage** (Optional - For Persistent Storage)

```bash
# Google Cloud Storage
GCS_BUCKET_NAME=visa-exhibit-storage
GCS_PROJECT_ID=your-project-id

# Storage Options
STORAGE_TYPE=local  # Options: local, gcs, supabase
```

---

## 🗜️ COMPRESSION SETTINGS

### **PDF Compression Configuration**

```bash
# Default Compression Settings
COMPRESSION_ENABLED=true
COMPRESSION_QUALITY=high  # Options: high, balanced, maximum

# Compression Methods Priority
COMPRESSION_TIER_1=ghostscript
COMPRESSION_TIER_2=pymupdf
COMPRESSION_TIER_3=smallpdf

# Quality Presets
HIGH_QUALITY_TEXT_DPI=300
HIGH_QUALITY_IMAGE_DPI=200
HIGH_QUALITY_JPEG_QUALITY=85
```

---

## 🔐 AUTHENTICATION (Future Implementation)

### **User Authentication** (Optional - With Supabase)

```bash
# Auth Configuration
AUTH_ENABLED=false
AUTH_PROVIDER=supabase  # Options: supabase, firebase, custom

# Session Management
SESSION_LIFETIME_DAYS=30
REMEMBER_ME_DAYS=90
```

---

## 🌐 CORS & SECURITY HEADERS

### **CORS Configuration**

```bash
# CORS Settings
CORS_ENABLED=true
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOW_CREDENTIALS=true
```

---

### **Security Headers**

```bash
# Security Configuration
ENABLE_HTTPS_ONLY=true
SECURE_COOKIES=true
CSRF_PROTECTION=true
```

---

## 📝 FEATURE FLAGS

### **Feature Toggles**

```bash
# Feature Flags
FEATURE_GOOGLE_DRIVE=true
FEATURE_COMPRESSION=true
FEATURE_ARCHIVE_ORG=true
FEATURE_TOC_GENERATION=true
FEATURE_BATCH_PROCESSING=true
FEATURE_SUPABASE_INTEGRATION=false
```

---

## 🚀 DEPLOYMENT CONFIGURATION

### **Cloud Run Specific**

```bash
# Cloud Run Settings
CLOUD_RUN_SERVICE_NAME=visa-exhibit-maker
CLOUD_RUN_REGION=us-central1
CLOUD_RUN_MEMORY=2Gi
CLOUD_RUN_CPU=2
CLOUD_RUN_TIMEOUT=300
CLOUD_RUN_MAX_INSTANCES=10
CLOUD_RUN_MIN_INSTANCES=0
```

---

### **Container Configuration**

```bash
# Container Settings
WORKERS=1
THREADS=4
MAX_CONCURRENT_REQUESTS=10

# Resource Limits
MAX_MEMORY_MB=2048
MAX_CPU_CORES=2
```

---

## 📦 COMPLETE ENV FILE TEMPLATE

### **Minimal Setup** (Works out of the box)

```bash
# Required
APP_ENV=production
PORT=8080
STREAMLIT_SERVER_PORT=8080
STREAMLIT_SERVER_HEADLESS=true

# Recommended
COMPRESSION_ENABLED=true
GHOSTSCRIPT_PATH=/usr/bin/gs
LOG_LEVEL=INFO
```

---

### **Full Production Setup** (All features)

```bash
# Application
APP_ENV=production
PORT=8080
HOST=0.0.0.0
SECRET_KEY=your-secret-key-here

# Streamlit
STREAMLIT_SERVER_PORT=8080
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Google Drive
GOOGLE_CREDENTIALS_JSON='{"type":"service_account",...}'
GOOGLE_CLOUD_PROJECT=your-project-id

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key
SUPABASE_STORAGE_BUCKET=exhibit-packages

# Compression
COMPRESSION_ENABLED=true
COMPRESSION_QUALITY=high
GHOSTSCRIPT_PATH=/usr/bin/gs
SMALLPDF_API_KEY=your-key-optional

# Storage
STORAGE_TYPE=supabase
TEMP_DIR=/tmp
AUTO_CLEANUP_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
GOOGLE_CLOUD_LOGGING=true

# Features
FEATURE_GOOGLE_DRIVE=true
FEATURE_COMPRESSION=true
FEATURE_ARCHIVE_ORG=true
FEATURE_SUPABASE_INTEGRATION=true

# Security
CORS_ENABLED=true
CORS_ORIGINS=https://yourdomain.com
SECURE_COOKIES=true
ENABLE_HTTPS_ONLY=true
```

---

## 🔧 HOW TO SET ENV VARS IN CLOUD RUN

### **Method 1: Via gcloud CLI**

```bash
gcloud run deploy visa-exhibit-maker \
  --image gcr.io/your-project/visa-exhibit-maker \
  --platform managed \
  --region us-central1 \
  --set-env-vars="APP_ENV=production,PORT=8080,COMPRESSION_ENABLED=true" \
  --set-secrets="GOOGLE_CREDENTIALS_JSON=google-creds:latest,SUPABASE_SERVICE_ROLE_KEY=supabase-key:latest"
```

---

### **Method 2: Via Cloud Console**

1. Go to Cloud Run in GCP Console
2. Select your service
3. Click "Edit & Deploy New Revision"
4. Go to "Variables & Secrets" tab
5. Add environment variables
6. Deploy

---

### **Method 3: Via YAML Configuration**

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: visa-exhibit-maker
spec:
  template:
    spec:
      containers:
      - image: gcr.io/your-project/visa-exhibit-maker
        env:
        - name: APP_ENV
          value: production
        - name: PORT
          value: "8080"
        - name: COMPRESSION_ENABLED
          value: "true"
        - name: GOOGLE_CREDENTIALS_JSON
          valueFrom:
            secretKeyRef:
              name: google-creds
              key: latest
```

---

## 🔐 SECRET MANAGEMENT

### **Google Secret Manager** (Recommended)

```bash
# Create secrets
echo -n "your-secret-value" | gcloud secrets create SECRET_NAME --data-file=-

# Grant access to Cloud Run service account
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/secretmanager.secretAccessor"

# Reference in Cloud Run
gcloud run deploy visa-exhibit-maker \
  --set-secrets="SMALLPDF_API_KEY=smallpdf-key:latest"
```

---

## ✅ VALIDATION CHECKLIST

### **Before Deployment**

- [ ] All required env vars set
- [ ] Google credentials JSON valid
- [ ] Ghostscript path correct
- [ ] Secrets stored in Secret Manager
- [ ] CORS origins configured
- [ ] Port set to 8080
- [ ] Streamlit headless mode enabled
- [ ] Log level appropriate
- [ ] Resource limits configured

---

### **After Deployment**

- [ ] Service accessible via URL
- [ ] PDF uploads working
- [ ] Compression functioning
- [ ] Google Drive integration (if enabled)
- [ ] Logs appearing in Cloud Logging
- [ ] No secret keys in logs
- [ ] Error handling working

---

## 💰 COST CONSIDERATIONS

### **Free Tier Components**

- ✅ Google Drive API: FREE
- ✅ Ghostscript: FREE
- ✅ PyMuPDF: FREE
- ✅ Archive.org: FREE
- ✅ Cloud Run: 2 million requests/month free

---

### **Paid Components** (Optional)

- SmallPDF: $12/month (5,000 pages)
- Supabase: $25/month (Pro tier)
- API2PDF: $0.001/page
- Cloud Run: After free tier (~$0.00002400/request)
- Cloud Storage: $0.020/GB/month

---

## 📚 REFERENCES

- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Secret Manager**: https://cloud.google.com/secret-manager
- **Streamlit Deployment**: https://docs.streamlit.io/deploy
- **Google Drive API**: https://developers.google.com/drive
- **Supabase Docs**: https://supabase.com/docs

---

## 🆘 TROUBLESHOOTING

### **Common Issues**

**"Port already in use"**
```bash
# Make sure PORT=8080 is set
export PORT=8080
```

**"Ghostscript not found"**
```bash
# Add to Dockerfile
RUN apt-get update && apt-get install -y ghostscript
```

**"Google credentials invalid"**
```bash
# Verify JSON format
echo $GOOGLE_CREDENTIALS_JSON | jq .
```

**"Supabase connection failed"**
```bash
# Check URL and keys
curl -H "apikey: $SUPABASE_ANON_KEY" $SUPABASE_URL/rest/v1/
```

---

## 📞 SUPPORT

- **GitHub**: https://github.com/IGTA-Tech/visa-exhibit-maker
- **Issues**: https://github.com/IGTA-Tech/visa-exhibit-maker/issues
- **Cloud Run Support**: https://cloud.google.com/run/docs/support

---

**Last Updated**: December 3, 2025
**Version**: 1.0
**Deployment Target**: Google Cloud Run
