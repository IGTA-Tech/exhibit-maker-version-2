-- Visa Exhibit Generator V2.0 - Initial Database Schema
-- Run this in Supabase SQL Editor to create all tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===========================================
-- USERS TABLE
-- ===========================================
-- User profiles and preferences (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE,
    full_name TEXT,
    organization TEXT,
    preferences JSONB DEFAULT '{}',
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'superadmin')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Users can view/update their own profile
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- ===========================================
-- VISA CASES TABLE
-- ===========================================
-- Case tracking with AI analysis fields
CREATE TABLE IF NOT EXISTS public.visa_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,

    -- Case info (all optional per Feature 1)
    visa_category TEXT,  -- O-1A, O-1B, P-1A, EB-1A, etc.
    beneficiary_name TEXT,
    petitioner_name TEXT,
    petition_structure TEXT,  -- direct_employment, agent_as_employer, etc.
    processing_type TEXT DEFAULT 'regular',  -- regular, premium

    -- Status
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'processing', 'completed', 'archived')),

    -- AI analysis results
    ai_analysis JSONB DEFAULT '{}',
    missing_criteria TEXT[],

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.visa_cases ENABLE ROW LEVEL SECURITY;

-- Users can CRUD their own cases
CREATE POLICY "Users can view own cases" ON public.visa_cases
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create cases" ON public.visa_cases
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own cases" ON public.visa_cases
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own cases" ON public.visa_cases
    FOR DELETE USING (auth.uid() = user_id);

-- Index for user lookup
CREATE INDEX idx_visa_cases_user_id ON public.visa_cases(user_id);
CREATE INDEX idx_visa_cases_status ON public.visa_cases(status);

-- ===========================================
-- EXHIBIT PACKAGES TABLE
-- ===========================================
-- Generated packages with stats
CREATE TABLE IF NOT EXISTS public.exhibit_packages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES public.visa_cases(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,

    -- Package info
    exhibit_count INTEGER DEFAULT 0,
    total_pages INTEGER DEFAULT 0,
    original_size BIGINT DEFAULT 0,  -- bytes
    compressed_size BIGINT DEFAULT 0,  -- bytes
    compression_method TEXT,

    -- File storage
    file_path TEXT,
    storage_url TEXT,

    -- Shareable link
    shareable_link_id TEXT UNIQUE,
    link_password_hash TEXT,
    expires_at TIMESTAMPTZ,
    max_downloads INTEGER,
    download_count INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.exhibit_packages ENABLE ROW LEVEL SECURITY;

-- Users can view their own packages
CREATE POLICY "Users can view own packages" ON public.exhibit_packages
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create packages" ON public.exhibit_packages
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own packages" ON public.exhibit_packages
    FOR UPDATE USING (auth.uid() = user_id);

-- Public can view package by shareable link (for download)
CREATE POLICY "Public can view by shareable link" ON public.exhibit_packages
    FOR SELECT USING (shareable_link_id IS NOT NULL);

-- Indexes
CREATE INDEX idx_exhibit_packages_case_id ON public.exhibit_packages(case_id);
CREATE INDEX idx_exhibit_packages_shareable_link ON public.exhibit_packages(shareable_link_id);

-- ===========================================
-- EXHIBITS TABLE
-- ===========================================
-- Individual exhibit records with AI classification
CREATE TABLE IF NOT EXISTS public.exhibits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_id UUID REFERENCES public.exhibit_packages(id) ON DELETE CASCADE,
    case_id UUID REFERENCES public.visa_cases(id) ON DELETE CASCADE,

    -- Exhibit info
    exhibit_number TEXT NOT NULL,  -- A, B, C or 1, 2, 3
    exhibit_name TEXT NOT NULL,
    filename TEXT NOT NULL,

    -- AI classification
    category TEXT,
    criterion_code TEXT,  -- O1A-1, P1A-7, etc.
    confidence_score DECIMAL(3,2) DEFAULT 0.00,
    evidence_type TEXT,  -- standard, comparable (NOT for P-1A)

    -- File info
    page_count INTEGER DEFAULT 0,
    file_size BIGINT DEFAULT 0,
    compressed_size BIGINT DEFAULT 0,

    -- AI reasoning
    ai_reasoning TEXT,
    user_override BOOLEAN DEFAULT FALSE,

    -- Order in package
    "order" INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.exhibits ENABLE ROW LEVEL SECURITY;

-- Users can view exhibits in their packages
CREATE POLICY "Users can view own exhibits" ON public.exhibits
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.exhibit_packages p
            WHERE p.id = package_id AND p.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can create exhibits" ON public.exhibits
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.exhibit_packages p
            WHERE p.id = package_id AND p.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update own exhibits" ON public.exhibits
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.exhibit_packages p
            WHERE p.id = package_id AND p.user_id = auth.uid()
        )
    );

-- Indexes
CREATE INDEX idx_exhibits_package_id ON public.exhibits(package_id);
CREATE INDEX idx_exhibits_case_id ON public.exhibits(case_id);
CREATE INDEX idx_exhibits_order ON public.exhibits("order");

-- ===========================================
-- AI CLASSIFICATIONS TABLE
-- ===========================================
-- Audit trail for AI decisions
CREATE TABLE IF NOT EXISTS public.ai_classifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exhibit_id UUID REFERENCES public.exhibits(id) ON DELETE CASCADE,
    case_id UUID REFERENCES public.visa_cases(id) ON DELETE CASCADE,

    -- Classification details
    visa_type TEXT NOT NULL,
    criterion_code TEXT NOT NULL,
    confidence_score DECIMAL(3,2) NOT NULL,
    reasoning TEXT,

    -- AI model info
    model_version TEXT DEFAULT 'claude-3',
    tokens_used INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.ai_classifications ENABLE ROW LEVEL SECURITY;

-- Users can view their own classifications
CREATE POLICY "Users can view own classifications" ON public.ai_classifications
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.visa_cases c
            WHERE c.id = case_id AND c.user_id = auth.uid()
        )
    );

-- Index
CREATE INDEX idx_ai_classifications_exhibit_id ON public.ai_classifications(exhibit_id);
CREATE INDEX idx_ai_classifications_case_id ON public.ai_classifications(case_id);

-- ===========================================
-- GENERATION HISTORY TABLE
-- ===========================================
-- Action logging
CREATE TABLE IF NOT EXISTS public.generation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES public.visa_cases(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,

    -- Action info
    action TEXT NOT NULL,  -- 'upload', 'classify', 'generate', 'download', 'email', 'share'
    details JSONB DEFAULT '{}',

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.generation_history ENABLE ROW LEVEL SECURITY;

-- Users can view their own history
CREATE POLICY "Users can view own history" ON public.generation_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create history" ON public.generation_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Index
CREATE INDEX idx_generation_history_case_id ON public.generation_history(case_id);
CREATE INDEX idx_generation_history_user_id ON public.generation_history(user_id);

-- ===========================================
-- COMPRESSION STATS TABLE
-- ===========================================
-- Performance metrics
CREATE TABLE IF NOT EXISTS public.compression_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_id UUID REFERENCES public.exhibit_packages(id) ON DELETE CASCADE,

    -- Compression info
    original_size BIGINT NOT NULL,
    compressed_size BIGINT NOT NULL,
    reduction_percent DECIMAL(5,2),
    method TEXT NOT NULL,  -- 'ghostscript', 'pymupdf', 'smallpdf', 'none'
    quality_preset TEXT,   -- 'high', 'balanced', 'maximum'
    duration_ms INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.compression_stats ENABLE ROW LEVEL SECURITY;

-- Users can view stats for their packages
CREATE POLICY "Users can view own compression stats" ON public.compression_stats
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.exhibit_packages p
            WHERE p.id = package_id AND p.user_id = auth.uid()
        )
    );

-- Index
CREATE INDEX idx_compression_stats_package_id ON public.compression_stats(package_id);

-- ===========================================
-- EXHIBIT TEMPLATES TABLE
-- ===========================================
-- Reusable exhibit structures
CREATE TABLE IF NOT EXISTS public.exhibit_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,

    -- Template info
    name TEXT NOT NULL,
    description TEXT,
    visa_type TEXT NOT NULL,

    -- Structure
    structure JSONB NOT NULL,  -- Array of {criterion_code, exhibit_letter, name}

    -- Usage
    is_public BOOLEAN DEFAULT FALSE,
    use_count INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.exhibit_templates ENABLE ROW LEVEL SECURITY;

-- Users can view their own templates and public templates
CREATE POLICY "Users can view templates" ON public.exhibit_templates
    FOR SELECT USING (auth.uid() = user_id OR is_public = TRUE);

CREATE POLICY "Users can create templates" ON public.exhibit_templates
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own templates" ON public.exhibit_templates
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own templates" ON public.exhibit_templates
    FOR DELETE USING (auth.uid() = user_id);

-- Index
CREATE INDEX idx_exhibit_templates_user_id ON public.exhibit_templates(user_id);
CREATE INDEX idx_exhibit_templates_visa_type ON public.exhibit_templates(visa_type);

-- ===========================================
-- STORAGE BUCKETS
-- ===========================================
-- Note: Create these in Supabase Dashboard > Storage

-- 1. exhibit-packages (private bucket for generated PDFs)
-- 2. temp-uploads (private bucket for processing)

-- ===========================================
-- FUNCTIONS
-- ===========================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_visa_cases_updated_at
    BEFORE UPDATE ON public.visa_cases
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_exhibit_templates_updated_at
    BEFORE UPDATE ON public.exhibit_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, full_name)
    VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ===========================================
-- INITIAL DATA
-- ===========================================

-- Default O-1A template
INSERT INTO public.exhibit_templates (name, description, visa_type, structure, is_public) VALUES
(
    'O-1A Standard Structure',
    'Standard exhibit structure for O-1A Extraordinary Ability petitions',
    'O-1A',
    '[
        {"criterion_code": "O1A-1", "exhibit_letter": "A", "name": "Awards and Prizes"},
        {"criterion_code": "O1A-2", "exhibit_letter": "B", "name": "Membership in Organizations"},
        {"criterion_code": "O1A-3", "exhibit_letter": "C", "name": "Published Material"},
        {"criterion_code": "O1A-4", "exhibit_letter": "D", "name": "Judging"},
        {"criterion_code": "O1A-5", "exhibit_letter": "E", "name": "Original Contributions"},
        {"criterion_code": "O1A-6", "exhibit_letter": "F", "name": "Scholarly Articles"},
        {"criterion_code": "O1A-7", "exhibit_letter": "G", "name": "Critical Employment"},
        {"criterion_code": "O1A-8", "exhibit_letter": "H", "name": "High Salary"}
    ]'::jsonb,
    TRUE
),
(
    'P-1A Standard Structure',
    'Standard exhibit structure for P-1A Athlete petitions (NO comparable evidence)',
    'P-1A',
    '[
        {"criterion_code": "P1A-1", "exhibit_letter": "A", "name": "Major League Documentation"},
        {"criterion_code": "P1A-2", "exhibit_letter": "B", "name": "National Team Participation"},
        {"criterion_code": "P1A-3", "exhibit_letter": "C", "name": "Intercollegiate Competition"},
        {"criterion_code": "P1A-4", "exhibit_letter": "D", "name": "Federation Statement"},
        {"criterion_code": "P1A-5", "exhibit_letter": "E", "name": "Expert Statements"},
        {"criterion_code": "P1A-6", "exhibit_letter": "F", "name": "Ranking Documentation"},
        {"criterion_code": "P1A-7", "exhibit_letter": "G", "name": "Honors and Awards"}
    ]'::jsonb,
    TRUE
);

-- Grant permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
