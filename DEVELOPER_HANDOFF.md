# Developer Handoff: Exhibit Maker Version 2

## Executive Summary

The current system is a **PDF exhibit organizer** - it takes existing PDFs, classifies them, numbers them, and merges them into a package.

**What we NEED is a RAG-powered petition generator** that:
1. Generates professional DOCX templates (cover letters, legal briefs, petition letters)
2. Produces output that looks like a professional law firm filing, NOT AI markdown with weird symbols
3. Works for both attorneys AND self-petitioners (DIY applicants)
4. Properly handles comparable evidence with auto-generated explanation letters

---

## Current State Analysis

### What EXISTS Now

| Component | Status | What It Does |
|-----------|--------|--------------|
| PDF Processing | Working | Adds exhibit numbers (A, B, C) to PDFs |
| PDF Compression | Working | 60-90% file size reduction |
| AI Classification | Working | Uses Claude to classify docs by visa criteria |
| RAG Knowledge Base | Comprehensive | 1,400+ lines of visa criteria documentation |
| Table of Contents | Basic | Generates a simple TOC as first page |
| Exhibit Ordering | Working | Orders exhibits by criterion |

### What's MISSING

| Feature | Priority | Why It's Critical |
|---------|----------|-------------------|
| **DOCX Template Generation** | CRITICAL | Output looks amateur, not professional |
| **Cover Letter Generator** | CRITICAL | Every petition needs a professional cover letter |
| **Legal Brief Generator** | CRITICAL | The most important document in a petition |
| **Comparable Evidence Letters** | HIGH | O-1A/O-1B/EB-1A require explanation letters |
| **DIY Guidance Output** | HIGH | Self-petitioners need step-by-step help |
| **Clean Professional Formatting** | CRITICAL | No markdown artifacts, proper fonts, spacing |

---

## The Problem: AI Markdown vs Professional Filing

### What We're Getting Now (BAD)
```
## Exhibit A: Award Certificate

The beneficiary received **recognition** for their work...

- Award Name: XYZ Championship
- Date: 2024
* Significance: National level
```

### What We NEED (GOOD)
```
EXHIBIT A

AWARD CERTIFICATE

[Clean professional paragraph]

The beneficiary received recognition for their work in the form of the XYZ
Championship award on [date]. This award carries national significance
because...

[Proper legal citation formatting]
See 8 CFR § 214.2(o)(3)(iii)(A).
```

---

## Required Features for Developer

### 1. Professional DOCX Template Engine

Create a template system that generates clean Word documents:

```python
# Example structure needed:
class PetitionTemplateEngine:
    def generate_cover_letter(self, case_data: dict) -> docx.Document:
        """Generate professional cover letter"""

    def generate_legal_brief(self, case_data: dict, exhibits: list) -> docx.Document:
        """Generate legal brief with criterion analysis"""

    def generate_toc(self, exhibits: list) -> docx.Document:
        """Generate formatted table of contents"""

    def generate_comparable_evidence_letter(
        self,
        criterion: str,
        explanation: str
    ) -> docx.Document:
        """Generate CE explanation letter"""
```

**Libraries to use:**
- `python-docx` for Word document generation
- Professional templates with proper:
  - Fonts (Times New Roman 12pt)
  - Margins (1 inch)
  - Line spacing (1.15 or single)
  - Proper paragraph formatting
  - NO markdown symbols (`**`, `##`, `-`, `*`)

### 2. Cover Letter Template

Every petition needs a cover letter. Must include:

```
[Date]

U.S. Citizenship and Immigration Services
[Service Center Address]

Re: [Visa Type] Petition for [Beneficiary Name]

Dear Sir or Madam:

[Petitioner Name] hereby submits this [Visa Type] petition on behalf of
[Beneficiary Name], a [nationality] national with extraordinary ability in
[field].

This petition is supported by the following exhibits:

[Exhibit list]

[Closing]

Respectfully submitted,

[Signature block]
```

### 3. Legal Brief Generator

The brief is the most critical document. Structure needed:

```
I. INTRODUCTION
   - Case overview
   - Visa category

II. STATEMENT OF FACTS
   - Beneficiary biography
   - Career chronology

III. LEGAL STANDARD
   - Regulatory framework
   - CFR citations
   - Applicable AAO decisions

IV. CRITERION-BY-CRITERION ANALYSIS
   [FOR EACH CRITERION BEING CLAIMED:]

   A. [Criterion Name] - [Standard/Comparable Evidence]

      1. Regulatory Requirement
         "..." See 8 CFR § X.X.X

      2. Evidence Submitted
         - Exhibit [X]: [Description]
         - Exhibit [Y]: [Description]

      3. Analysis
         [Professional legal analysis connecting evidence to criterion]

V. FINAL MERITS DETERMINATION (for EB-1A)
   [Required two-step Kazarian analysis]

VI. CONCLUSION
```

### 4. Comparable Evidence Letter Generator

For O-1A, O-1B, and EB-1A when using comparable evidence:

```
COMPARABLE EVIDENCE EXPLANATION
Criterion [X]: [Name]

Pursuant to 8 CFR § [citation], the petitioner submits comparable evidence
to establish the beneficiary's eligibility under this criterion.

WHY THE STANDARD CRITERION DOES NOT READILY APPLY:
[Specific explanation for this field/occupation]

COMPARABLE EVIDENCE SUBMITTED:
[Description of what's being submitted instead]

HOW THIS EVIDENCE IS OF COMPARABLE SIGNIFICANCE:
[Analysis showing it meets the regulatory intent]
```

### 5. DIY Self-Petitioner Mode

When someone is doing their own visa (no attorney):

**Additional outputs needed:**
- Step-by-step filing instructions
- Checklist of required documents
- Common mistakes to avoid
- Fee calculation
- Service center determination
- Estimated processing times
- What to expect after filing

**Embedded guidance in documents:**
- [INSTRUCTION: Sign here before filing]
- [NOTE: Make a copy for your records]
- [IMPORTANT: This exhibit proves Criterion A - Awards]

---

## RAG Integration Requirements

### Current RAG Knowledge Base

The `VISA_EXHIBIT_RAG_COMPREHENSIVE_INSTRUCTIONS.md` file contains:
- All visa criteria definitions
- Exhibit ordering templates
- Comparable evidence alternatives
- Regulatory citations
- Quality checklists

### How to Use RAG for Generation

```python
class RAGPetitionGenerator:
    def __init__(self, knowledge_base_path: str):
        self.kb = self.load_knowledge_base(knowledge_base_path)

    def generate_criterion_analysis(
        self,
        criterion: str,
        visa_type: str,
        evidence: list,
        use_comparable: bool = False
    ) -> str:
        """
        Use RAG to generate professional legal analysis.

        CRITICAL: Output must be clean prose, NOT markdown.
        - No ** for bold
        - No ## for headers
        - No - or * for bullets
        - Use proper legal citation format
        """

    def get_criterion_requirements(self, visa_type: str, criterion: str) -> dict:
        """Pull regulatory requirements from knowledge base"""

    def suggest_comparable_evidence(self, visa_type: str, criterion: str) -> list:
        """Get comparable evidence alternatives from RAG"""
```

### RAG Prompt Engineering

When calling Claude/LLM for content generation:

```
SYSTEM: You are a professional immigration attorney drafting a visa petition.

CRITICAL FORMATTING RULES:
1. Output CLEAN PROSE only - no markdown syntax
2. Use proper legal document formatting
3. Citations: "See 8 CFR § X.X.X" - never markdown links
4. For emphasis, use CAPS or underline, not **bold**
5. Lists should be:
   (a) Lettered like this
   (b) Or numbered like this: 1. 2. 3.
   NEVER: - bullet, * bullet, ## header

BAD OUTPUT:
"The beneficiary has **extraordinary ability** as shown by:
- Award 1
- Award 2
## Analysis..."

GOOD OUTPUT:
"The beneficiary has demonstrated extraordinary ability as evidenced
by the following: (1) the XYZ Championship award; (2) the ABC Medal;
and (3) recognition from the National Federation.

ANALYSIS

The evidence establishes that..."
```

---

## Technical Implementation Roadmap

### Phase 1: Template Foundation (Week 1)

1. Create `templates/` directory structure:
   ```
   templates/
   ├── cover_letter/
   │   ├── o1a_cover.docx
   │   ├── p1a_cover.docx
   │   └── eb1a_cover.docx
   ├── brief/
   │   ├── o1a_brief.docx
   │   ├── p1a_brief.docx
   │   └── eb1a_brief.docx
   ├── comparable_evidence/
   │   └── ce_explanation.docx
   └── toc/
       └── table_of_contents.docx
   ```

2. Build template engine with `python-docx`
3. Create placeholder system for dynamic content

### Phase 2: RAG-Powered Generation (Week 2)

1. Build prompt templates for each document type
2. Implement clean prose output validation
3. Add regulatory citation lookup
4. Create criterion analysis generator

### Phase 3: DIY Mode (Week 3)

1. Add self-petitioner detection/selection
2. Build instruction document generator
3. Create checklist generator
4. Add fee calculator
5. Embed guidance notes in documents

### Phase 4: Integration & Testing (Week 4)

1. Integrate with existing Streamlit app
2. Add DOCX download alongside PDF
3. Test with real petition examples
4. Validate against actual filed petitions

---

## Quality Criteria for Output

### The output must look like it came from a law firm, NOT an AI tool.

**Checklist for every generated document:**

- [ ] No markdown symbols (`**`, `##`, `-`, `*`, `>`)
- [ ] Proper fonts (Times New Roman or Arial)
- [ ] 1-inch margins
- [ ] Proper paragraph indentation
- [ ] Legal citation format
- [ ] Professional header/footer
- [ ] Page numbers
- [ ] Proper signature blocks
- [ ] Clean tables (no ASCII art)
- [ ] Exhibits properly referenced by letter

### Example Comparison

| Aspect | AI/Markdown (BAD) | Professional (GOOD) |
|--------|-------------------|---------------------|
| Headers | `## Criterion A` | **CRITERION A** (styled) |
| Bold | `**important**` | IMPORTANT or _underline_ |
| Lists | `- item` | (a) item, or 1. item |
| Citations | `[8 CFR](link)` | See 8 CFR § 214.2(o) |
| Emphasis | `*italics*` | Underlined or CAPS |

---

## Files to Review

| File | Purpose | Priority |
|------|---------|----------|
| `VISA_EXHIBIT_RAG_COMPREHENSIVE_INSTRUCTIONS.md` | Primary RAG knowledge | READ FIRST |
| `EXHIBIT_GENERATION_KNOWLEDGE_BASE.txt` | Additional context | Secondary |
| `streamlit-exhibit-generator/app.py` | Current app code | Review |
| `Examples of Single PDFs/` | Real petition examples | Study these |

---

## Key Regulatory References

Ensure the system correctly handles these CFR citations:

| Visa | Standard Criteria | Comparable Evidence |
|------|-------------------|---------------------|
| O-1A | 8 CFR § 214.2(o)(3)(iii) | 8 CFR § 214.2(o)(3)(v) |
| O-1B | 8 CFR § 214.2(o)(3)(iv) | 8 CFR § 214.2(o)(3)(v) |
| P-1A | 8 CFR § 214.2(p)(4)(ii)(B) | **NONE** - No CE allowed |
| EB-1A | 8 CFR § 204.5(h)(3) | 8 CFR § 204.5(h)(4) |

**CRITICAL: P-1A has NO comparable evidence provision. The system must NEVER generate CE letters for P-1A.**

---

## Success Metrics

The rebuild is successful when:

1. **Output looks professional** - Indistinguishable from a law firm filing
2. **No AI artifacts** - Zero markdown symbols in final documents
3. **DIY-friendly** - Self-petitioners can use output directly
4. **Comparable evidence works** - Auto-generates required explanation letters
5. **RAG-accurate** - Uses correct regulatory citations and criteria

---

## Contact & Questions

This handoff document prepared: December 2025
Repository: `/home/sherrod/exhibit-maker-version-2/`

Questions about:
- Visa criteria → See `VISA_EXHIBIT_RAG_COMPREHENSIVE_INSTRUCTIONS.md`
- Current code → See `streamlit-exhibit-generator/app.py`
- Example outputs → See `Examples of Single PDFs/`
