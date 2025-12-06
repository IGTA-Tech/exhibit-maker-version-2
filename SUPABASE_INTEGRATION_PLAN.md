# 🔗 SUPABASE INTEGRATION PLAN
## Visa Exhibit Generator - Database-Backed Production System

**Version**: 1.0
**Created**: November 29, 2025
**Purpose**: Integrate Supabase database to make THIS exhibit generator robust, scalable, and production-ready

---

## 🎯 INTEGRATION GOALS

### Primary Objectives:
1. **Persistent Storage** - Save exhibit configurations, templates, and generation history
2. **User Management** - Track users, permissions, and usage analytics
3. **Template Library** - Store and retrieve exhibit templates by visa type
4. **Document Versioning** - Track changes to exhibits and maintain audit trail
5. **Collaboration** - Enable team access and sharing within THIS tool
6. **RAG Knowledge Base** - Store and version the comprehensive instructions and guides

---

## 📊 SUPABASE DATABASE SCHEMA

### **Table 1: `users`**
Manage users and authentication

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  organization TEXT,
  role TEXT DEFAULT 'user', -- 'admin', 'user', 'viewer'
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);
```

### **Table 2: `visa_cases`**
Store visa petition cases

```sql
CREATE TABLE visa_cases (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  case_name TEXT NOT NULL,
  beneficiary_name TEXT,
  visa_type TEXT NOT NULL, -- 'O-1A', 'O-1B', 'P-1A', 'EB-1A'
  status TEXT DEFAULT 'draft', -- 'draft', 'in_progress', 'completed', 'submitted'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  submitted_at TIMESTAMP,
  metadata JSONB -- Store additional case info
);
```

### **Table 3: `exhibit_packages`**
Store generated exhibit packages

```sql
CREATE TABLE exhibit_packages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id UUID REFERENCES visa_cases(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  package_name TEXT NOT NULL,
  visa_type TEXT NOT NULL,
  numbering_style TEXT DEFAULT 'letters', -- 'letters', 'numbers', 'roman'

  -- Configuration
  compression_enabled BOOLEAN DEFAULT TRUE,
  quality_preset TEXT DEFAULT 'high',
  has_toc BOOLEAN DEFAULT TRUE,
  has_archive_urls BOOLEAN DEFAULT FALSE,
  is_merged BOOLEAN DEFAULT TRUE,

  -- Results
  total_exhibits INTEGER,
  total_pages INTEGER,
  original_size_bytes BIGINT,
  compressed_size_bytes BIGINT,
  compression_reduction_percent DECIMAL(5,2),

  -- Storage
  storage_path TEXT, -- Google Drive or Supabase Storage path
  download_url TEXT,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### **Table 4: `exhibits`**
Individual exhibits within packages

```sql
CREATE TABLE exhibits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  package_id UUID REFERENCES exhibit_packages(id) ON DELETE CASCADE,
  exhibit_number TEXT NOT NULL, -- 'A', 'B', '1', '2', etc.
  exhibit_name TEXT NOT NULL,
  file_name TEXT NOT NULL,

  -- Classification
  criterion TEXT, -- 'Criterion A', 'Criterion B', etc.
  evidence_type TEXT, -- 'standard', 'comparable'
  document_type TEXT, -- 'award', 'media', 'expert_letter', etc.

  -- File details
  original_size_bytes BIGINT,
  compressed_size_bytes BIGINT,
  compression_method TEXT, -- 'ghostscript', 'pymupdf', 'smallpdf'
  page_count INTEGER,

  -- Storage
  storage_path TEXT,
  download_url TEXT,

  -- Metadata
  metadata JSONB, -- Store archive URLs, dates, etc.
  created_at TIMESTAMP DEFAULT NOW()
);
```

### **Table 5: `exhibit_templates`**
Reusable templates by visa type

```sql
CREATE TABLE exhibit_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  template_name TEXT NOT NULL,
  visa_type TEXT NOT NULL,
  description TEXT,

  -- Template structure
  exhibit_structure JSONB NOT NULL, -- Array of exhibit definitions

  -- Settings
  numbering_style TEXT DEFAULT 'letters',
  compression_enabled BOOLEAN DEFAULT TRUE,
  quality_preset TEXT DEFAULT 'high',

  -- Sharing
  is_public BOOLEAN DEFAULT FALSE,
  organization TEXT, -- Allow organization-wide templates

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(user_id, template_name)
);
```

**Example Template Structure (JSONB)**:
```json
{
  "exhibits": [
    {
      "number": "A",
      "name": "Table of Contents",
      "type": "administrative",
      "required": true
    },
    {
      "number": "B",
      "name": "Form G-1450",
      "type": "administrative",
      "required": true
    },
    {
      "number": "K",
      "name": "Criterion 1 - Awards",
      "type": "criterion",
      "criterion": "1",
      "evidence_type": "standard",
      "sub_exhibits": ["K-1", "K-2", "K-3"]
    }
  ]
}
```

### **Table 6: `generation_history`**
Audit trail of all generations

```sql
CREATE TABLE generation_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  package_id UUID REFERENCES exhibit_packages(id),
  user_id UUID REFERENCES users(id),
  action TEXT NOT NULL, -- 'created', 'updated', 'downloaded', 'deleted'

  -- Details
  details JSONB, -- Store action-specific details
  ip_address INET,
  user_agent TEXT,

  created_at TIMESTAMP DEFAULT NOW()
);
```

### **Table 7: `rag_documents`**
Store RAG knowledge base documents with versioning

```sql
CREATE TABLE rag_documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_name TEXT NOT NULL,
  document_type TEXT NOT NULL, -- 'comprehensive_instructions', 'visa_specific', 'policy'
  visa_types TEXT[], -- Array of visa types this applies to

  -- Content
  content TEXT NOT NULL,
  version TEXT NOT NULL,

  -- Metadata
  source_file TEXT,
  source_url TEXT,
  regulatory_citations TEXT[],

  -- Status
  is_active BOOLEAN DEFAULT TRUE,
  is_authoritative BOOLEAN DEFAULT FALSE,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(document_name, version)
);
```

### **Table 8: `compression_stats`**
Track compression performance

```sql
CREATE TABLE compression_stats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  package_id UUID REFERENCES exhibit_packages(id),

  -- Compression details
  method TEXT NOT NULL, -- 'ghostscript', 'pymupdf', 'smallpdf'
  quality_preset TEXT NOT NULL,

  -- Performance
  original_size_bytes BIGINT NOT NULL,
  compressed_size_bytes BIGINT NOT NULL,
  reduction_percent DECIMAL(5,2),
  processing_time_ms INTEGER,

  -- Environment
  server_region TEXT,

  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 ROW LEVEL SECURITY (RLS) POLICIES

### Enable RLS on all tables:

```sql
-- Users can only see their own data
ALTER TABLE visa_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE exhibit_packages ENABLE ROW LEVEL SECURITY;
ALTER TABLE exhibits ENABLE ROW LEVEL SECURITY;
ALTER TABLE exhibit_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE generation_history ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view their own cases"
  ON visa_cases FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own cases"
  ON visa_cases FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own cases"
  ON visa_cases FOR UPDATE
  USING (auth.uid() = user_id);

-- Public templates policy
CREATE POLICY "Users can view public templates"
  ON exhibit_templates FOR SELECT
  USING (is_public = TRUE OR auth.uid() = user_id);

-- RAG documents are read-only for all authenticated users
CREATE POLICY "Authenticated users can view RAG documents"
  ON rag_documents FOR SELECT
  TO authenticated
  USING (is_active = TRUE);
```

---

---

## 📦 SUPABASE STORAGE STRUCTURE

### Bucket: `exhibit-packages`

```
exhibit-packages/
├── {user_id}/
│   ├── {case_id}/
│   │   ├── {package_id}/
│   │   │   ├── source/              # Original uploaded files
│   │   │   │   ├── file1.pdf
│   │   │   │   ├── file2.pdf
│   │   │   ├── compressed/          # Compressed files
│   │   │   │   ├── exhibit_a.pdf
│   │   │   │   ├── exhibit_b.pdf
│   │   │   ├── final/               # Final merged package
│   │   │   │   └── Complete_Package.pdf
│   │   │   └── metadata.json        # Package metadata
```

### Bucket: `rag-knowledge-base`

```
rag-knowledge-base/
├── visa-types/
│   ├── o1a/
│   │   ├── comprehensive_instructions.md
│   │   ├── templates/
│   │   └── examples/
│   ├── o1b/
│   ├── p1a/
│   └── eb1a/
└── shared/
    ├── regulations/
    ├── policies/
    └── best-practices/
```

---

## 🔌 API ENDPOINTS (Supabase Edge Functions)

### **1. `generate-exhibit-package`**
**Purpose**: Generate exhibits from uploaded files

**Request**:
```typescript
{
  case_id: string,
  files: File[],
  config: {
    visa_type: 'O-1A' | 'O-1B' | 'P-1A' | 'EB-1A',
    numbering_style: 'letters' | 'numbers' | 'roman',
    compression_enabled: boolean,
    quality_preset: 'high' | 'balanced' | 'maximum',
    has_toc: boolean,
    has_archive_urls: boolean,
    is_merged: boolean
  }
}
```

**Response**:
```typescript
{
  package_id: string,
  exhibits: Exhibit[],
  compression_stats: CompressionStats,
  download_url: string
}
```

### **2. `auto-categorize-document`**
**Purpose**: AI-powered document categorization

**Request**:
```typescript
{
  file: File,
  visa_type: string
}
```

**Response**:
```typescript
{
  suggested_criterion: string,
  evidence_type: 'standard' | 'comparable',
  document_type: string,
  confidence_score: number,
  reasoning: string
}
```

### **3. `get-template-suggestions`**
**Purpose**: Get exhibit template based on visa type and evidence

**Request**:
```typescript
{
  visa_type: string,
  available_documents: string[]
}
```

**Response**:
```typescript
{
  suggested_template: ExhibitTemplate,
  missing_documents: string[],
  quality_score: number
}
```

---

## 🚀 IMPLEMENTATION ROADMAP

### **Phase 1: Database Setup** (Week 1)
- [ ] Create Supabase project
- [ ] Implement database schema
- [ ] Configure RLS policies
- [ ] Create storage buckets
- [ ] Set up authentication

### **Phase 2: Backend Integration** (Week 2)
- [ ] Create Supabase Edge Functions
- [ ] Implement file upload/download
- [ ] Add compression integration
- [ ] Build template system
- [ ] Set up RAG document storage

### **Phase 3: Frontend Updates** (Week 3)
- [ ] Update Streamlit app with Supabase
- [ ] Add user authentication
- [ ] Implement case management UI
- [ ] Add template selection
- [ ] Build generation history view

### **Phase 4: Tool Integrations** (Week 4)
- [ ] Integrate with Visa Glow Tool
- [ ] Connect to AI Platform Whitelabel
- [ ] Link Investigation System
- [ ] Add cross-tool authentication

### **Phase 5: Testing & Deployment** (Week 5)
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security audit
- [ ] Production deployment
- [ ] User documentation

---

## 🔧 TECHNICAL STACK

### **Current Tools**:
- Streamlit (Python web UI)
- Google Apps Script (Drive integration)
- PyPDF2 (PDF manipulation)
- ReportLab (PDF generation)
- Ghostscript (Compression Tier 1)
- PyMuPDF (Compression Tier 2)

### **Adding**:
- ✅ **Supabase** (Database + Auth + Storage)
- ✅ **Supabase Edge Functions** (Serverless API)
- ✅ **Supabase Realtime** (Live updates)
- ✅ **Supabase Auth** (User management)
- ✅ **Supabase Storage** (File storage)

### **Existing Tools to Integrate**:
- ✅ **Visa Glow Tool** (Visa evaluation system)
- ✅ **AI Platform Whitelabel** (White-label AI platform)
- ✅ **Investigation System** (Evidence tracking)

---

## 📊 ENVIRONMENT VARIABLES

### **Streamlit (.env)**:
```bash
# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Storage
SUPABASE_STORAGE_BUCKET=exhibit-packages

# Integration
VISA_GLOW_API_URL=https://your-visa-glow-instance.com
AI_PLATFORM_API_KEY=your-ai-platform-key

# Compression
GHOSTSCRIPT_PATH=/usr/bin/gs
```

### **Google Apps Script (Script Properties)**:
```javascript
PropertiesService.getScriptProperties().setProperty('SUPABASE_URL', 'https://xxxxx.supabase.co');
PropertiesService.getScriptProperties().setProperty('SUPABASE_ANON_KEY', 'your-anon-key');
```

---

## 💡 FEATURE ENHANCEMENTS WITH SUPABASE

### **1. Real-Time Collaboration**
- Multiple team members can work on same case
- Live updates when exhibits are added/modified
- Real-time compression progress updates

### **2. Version Control**
- Track all changes to exhibits
- Restore previous versions
- Compare versions side-by-side

### **3. Analytics Dashboard**
- Track generation metrics
- Monitor compression performance
- Usage statistics by visa type

### **4. Template Marketplace**
- Share templates with community
- Rate and review templates
- Organization-wide template libraries

### **5. AI-Powered Suggestions**
- Auto-categorize uploaded documents
- Suggest missing exhibits
- Predict approval likelihood based on exhibits

---

## 🔒 SECURITY CONSIDERATIONS

### **Authentication**:
- Supabase Auth (email/password, OAuth)
- Row Level Security (RLS) enforced
- API key rotation policy

### **Data Protection**:
- Encryption at rest (Supabase default)
- Encryption in transit (HTTPS)
- Secure file upload/download URLs (signed URLs)

### **Access Control**:
- Role-based permissions (admin, user, viewer)
- Organization-based access
- Audit trail for all actions

---

## 📈 SCALABILITY

### **Database**:
- Supabase scales automatically
- Read replicas for high traffic
- Connection pooling (PgBouncer)

### **Storage**:
- Unlimited file storage (pay-as-you-go)
- CDN for fast file delivery
- Automatic backups

### **Compute**:
- Edge Functions scale automatically
- Serverless architecture
- Global distribution

---

## 🎯 SUCCESS METRICS

### **Performance**:
- Exhibit generation time: <30 seconds
- Compression processing: <5 seconds per file
- API response time: <200ms
- Storage costs: <$50/month for 1,000 cases

### **User Adoption**:
- User signups: 100+ in first month
- Cases created: 500+ in first quarter
- Template usage: 80% of users
- Cross-tool integration: 50% of users

---

## 📚 DOCUMENTATION NEEDED

1. **Supabase Setup Guide** - How to create and configure Supabase project
2. **Migration Guide** - Moving from standalone to Supabase-integrated
3. **API Reference** - Edge Functions documentation
4. **Integration Guide** - Connecting with Visa Glow and other tools
5. **User Guide** - How to use new features

---

## 🔗 NEXT STEPS

1. **Create Supabase project** at https://app.supabase.com
2. **Run database schema** (provided above)
3. **Set up environment variables** in Streamlit and Google Apps Script
4. **Implement Edge Functions** for exhibit generation
5. **Update Streamlit UI** to use Supabase
6. **Test end-to-end workflow**
7. **Deploy to production**

---

**Version**: 1.0
**Status**: Ready for Implementation
**GitHub**: https://github.com/IGTA-Tech/visa-exhibit-maker

**Next Action**: Review this plan and approve to begin Phase 1 implementation.
