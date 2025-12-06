"""
Streamlit Visa Exhibit Generator
Standalone application for generating numbered exhibit packages from PDFs, folders, and Google Drive
With built-in PDF compression

EXHIBIT ORGANIZATION REFERENCE:
This application follows the authoritative exhibit organization guide:
../VISA_EXHIBIT_RAG_COMPREHENSIVE_INSTRUCTIONS.md

This guide provides:
- Complete exhibit ordering templates for O-1A, O-1B, P-1A, P-1S, EB-1A
- Standard vs Comparable Evidence structures (O-1A, O-1B, EB-1A only)
- Criterion-by-criterion organization
- USCIS regulatory compliance (8 CFR § 214.2, 8 CFR § 204.5)
- Production-tested petition structures
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
import zipfile
from datetime import datetime

# Import our modules
from pdf_handler import PDFHandler
from exhibit_processor import ExhibitProcessor
from google_drive import GoogleDriveHandler
from archive_handler import ArchiveHandler

# Check if compression is available
try:
    from compress_handler import USCISPDFCompressor, compress_pdf_batch
    COMPRESSION_AVAILABLE = True
except ImportError:
    COMPRESSION_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="Visa Exhibit Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .stat-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: white;
        border: 1px solid #ddd;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'exhibits_generated' not in st.session_state:
    st.session_state.exhibits_generated = False
if 'compression_stats' not in st.session_state:
    st.session_state.compression_stats = None
if 'exhibit_list' not in st.session_state:
    st.session_state.exhibit_list = []

def main():
    """Main application"""

    # Header
    st.markdown('<div class="main-header">📄 Visa Exhibit Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional numbered exhibit packages for visa petitions</div>', unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Visa type selection
        visa_type = st.selectbox(
            "Visa Type",
            ["O-1A", "O-1B", "P-1A", "EB-1A"],
            help="Select the visa category for your petition"
        )

        # Exhibit numbering style
        numbering_style = st.selectbox(
            "Exhibit Numbering",
            ["Letters (A, B, C...)", "Numbers (1, 2, 3...)", "Roman (I, II, III...)"],
            help="How to number your exhibits"
        )

        # Convert numbering style to code
        numbering_map = {
            "Letters (A, B, C...)": "letters",
            "Numbers (1, 2, 3...)": "numbers",
            "Roman (I, II, III...)": "roman"
        }
        numbering_code = numbering_map[numbering_style]

        st.divider()

        # ==========================================
        # COMPRESSION SETTINGS
        # ==========================================
        st.header("🗜️ PDF Compression")

        if not COMPRESSION_AVAILABLE:
            st.warning("⚠️ Compression not available. Install PyMuPDF: `pip install PyMuPDF`")
            enable_compression = False
        else:
            enable_compression = st.checkbox(
                "Enable PDF Compression",
                value=True,
                help="Compress PDFs to reduce file size (50-75% reduction)"
            )

            if enable_compression:
                st.markdown('<div class="info-box">✓ Compression enabled - files will be 50-75% smaller</div>', unsafe_allow_html=True)

                # Quality preset
                quality_preset = st.selectbox(
                    "Compression Quality",
                    ["High Quality (USCIS Recommended)", "Balanced", "Maximum Compression"],
                    help="High = 300 DPI text, 200 DPI images (best for legal docs)\n"
                         "Balanced = 150 DPI images (good compression)\n"
                         "Maximum = 100 DPI images (smallest files)"
                )

                # Convert to code
                quality_map = {
                    "High Quality (USCIS Recommended)": "high",
                    "Balanced": "balanced",
                    "Maximum Compression": "maximum"
                }
                quality_code = quality_map[quality_preset]

                # Show quality details
                quality_info = {
                    "high": "📊 Text: 300 DPI | Images: 200 DPI | JPEG: 85%",
                    "balanced": "📊 Text: 300 DPI | Images: 150 DPI | JPEG: 80%",
                    "maximum": "📊 Text: 200 DPI | Images: 100 DPI | JPEG: 75%"
                }
                st.caption(quality_info[quality_code])

                # Compression method display
                with st.expander("ℹ️ Compression Methods"):
                    st.write("**3-Tier Fallback System:**")
                    st.write("1️⃣ **Ghostscript** (FREE) - 60-90% compression")
                    st.write("   Best quality/size ratio")
                    st.write("")
                    st.write("2️⃣ **PyMuPDF** (FREE) - 30-60% compression")
                    st.write("   Automatic fallback")
                    st.write("")
                    st.write("3️⃣ **SmallPDF API** (PAID) - 40-80% compression")
                    st.write("   Premium quality ($12/month)")

                # Optional SmallPDF API key
                with st.expander("🔑 SmallPDF API Key (Optional)"):
                    st.caption("For premium Tier 3 compression backup")
                    smallpdf_key = st.text_input(
                        "SmallPDF API Key",
                        type="password",
                        help="Get key at https://smallpdf.com/developers\n"
                             "Leave empty to use free compression only"
                    )
                    if smallpdf_key:
                        st.success("✓ SmallPDF API key set")
                    else:
                        st.info("Using free compression (Ghostscript + PyMuPDF)")
            else:
                quality_code = "high"
                smallpdf_key = None

        st.divider()

        # Additional options
        st.header("📋 Options")

        add_toc = st.checkbox(
            "Generate Table of Contents",
            value=True,
            help="Create a TOC page listing all exhibits"
        )

        add_archive = st.checkbox(
            "Archive URLs (archive.org)",
            value=False,
            help="Preserve URLs on archive.org (for media articles)"
        )

        merge_pdfs = st.checkbox(
            "Merge into single PDF",
            value=True,
            help="Combine all exhibits into one file"
        )

        st.divider()

        # Documentation reference
        st.header("📚 Documentation")

        with st.expander("ℹ️ Exhibit Organization Guide"):
            st.markdown("""
            **Reference Document:**
            `VISA_EXHIBIT_RAG_COMPREHENSIVE_INSTRUCTIONS.md`

            This application follows USCIS-compliant exhibit structures:

            **Supported Visa Types:**
            - ✅ O-1A (Extraordinary Ability)
            - ✅ O-1B (Arts/Entertainment)
            - ✅ P-1A (Internationally Recognized Athletes)
            - ✅ EB-1A (Permanent Residence)

            **Key Features:**
            - Standard vs Comparable Evidence (O-1A, O-1B, EB-1A only)
            - Criterion-based organization
            - USCIS regulatory compliance
            - Production-tested structures

            ⚠️ **Important:** P-1A has NO comparable evidence provision
            """)

    # Main content area
    tab1, tab2, tab3 = st.tabs(["📁 Upload Files", "☁️ Google Drive", "📊 Results"])

    # ==========================================
    # TAB 1: FILE UPLOAD
    # ==========================================
    with tab1:
        st.header("Upload PDF Files")

        upload_method = st.radio(
            "Upload Method",
            ["Individual PDFs", "ZIP Archive", "Folder"],
            horizontal=True
        )

        uploaded_files = []

        if upload_method == "Individual PDFs":
            uploaded_files = st.file_uploader(
                "Select PDF files",
                type=["pdf"],
                accept_multiple_files=True,
                help="Upload one or more PDF files"
            )

        elif upload_method == "ZIP Archive":
            zip_file = st.file_uploader(
                "Select ZIP file",
                type=["zip"],
                help="Upload a ZIP file containing PDFs"
            )

            if zip_file:
                # Extract ZIP
                with tempfile.TemporaryDirectory() as tmp_dir:
                    zip_path = os.path.join(tmp_dir, "upload.zip")
                    with open(zip_path, 'wb') as f:
                        f.write(zip_file.read())

                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(tmp_dir)

                    # Find PDFs
                    pdf_files = list(Path(tmp_dir).rglob("*.pdf"))
                    st.info(f"Found {len(pdf_files)} PDF files in ZIP")

                    # Store in session state for processing
                    st.session_state.zip_files = [str(p) for p in pdf_files]

        elif upload_method == "Folder":
            st.info("💡 Tip: Use Google Drive tab for folder processing")

        # Show uploaded files
        if uploaded_files:
            st.success(f"✓ {len(uploaded_files)} files uploaded")

            with st.expander("📄 View uploaded files"):
                for i, file in enumerate(uploaded_files, 1):
                    st.write(f"{i}. {file.name} ({file.size / 1024:.1f} KB)")

        # Generate button
        if uploaded_files or (upload_method == "ZIP Archive" and 'zip_files' in st.session_state):
            st.divider()

            if st.button("🚀 Generate Exhibits", type="primary", use_container_width=True):
                generate_exhibits(
                    uploaded_files if uploaded_files else st.session_state.zip_files,
                    visa_type,
                    numbering_code,
                    enable_compression,
                    quality_code,
                    smallpdf_key if enable_compression else None,
                    add_toc,
                    add_archive,
                    merge_pdfs
                )

    # ==========================================
    # TAB 2: GOOGLE DRIVE
    # ==========================================
    with tab2:
        st.header("Google Drive Integration")

        st.info("💡 Connect to Google Drive to process folders directly")

        drive_url = st.text_input(
            "Google Drive Folder URL",
            placeholder="https://drive.google.com/drive/folders/...",
            help="Paste the URL of your Google Drive folder containing PDFs"
        )

        if drive_url:
            if st.button("📥 Load from Drive", type="primary"):
                st.warning("🚧 Google Drive integration coming soon. Use file upload for now.")

    # ==========================================
    # TAB 3: RESULTS
    # ==========================================
    with tab3:
        st.header("Generation Results")

        if st.session_state.exhibits_generated:
            # Success message
            st.markdown('<div class="success-box">✓ Exhibits generated successfully!</div>', unsafe_allow_html=True)

            # Statistics
            st.subheader("📊 Statistics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(st.session_state.exhibit_list)}</div>
                    <div class="stat-label">Exhibits</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                total_pages = sum(ex.get('pages', 0) for ex in st.session_state.exhibit_list)
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{total_pages}</div>
                    <div class="stat-label">Total Pages</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                if st.session_state.compression_stats:
                    reduction = st.session_state.compression_stats.get('avg_reduction', 0)
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{reduction:.1f}%</div>
                        <div class="stat-label">Size Reduction</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">-</div>
                        <div class="stat-label">Compression</div>
                    </div>
                    """, unsafe_allow_html=True)

            with col4:
                if st.session_state.compression_stats:
                    original_mb = st.session_state.compression_stats.get('original_size', 0) / (1024*1024)
                    compressed_mb = st.session_state.compression_stats.get('compressed_size', 0) / (1024*1024)
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{compressed_mb:.1f} MB</div>
                        <div class="stat-label">Final Size</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">-</div>
                        <div class="stat-label">File Size</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Compression details
            if st.session_state.compression_stats:
                st.divider()
                st.subheader("🗜️ Compression Details")

                stats = st.session_state.compression_stats

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Original Size",
                        f"{stats.get('original_size', 0) / (1024*1024):.2f} MB"
                    )
                    st.metric(
                        "Compressed Size",
                        f"{stats.get('compressed_size', 0) / (1024*1024):.2f} MB",
                        delta=f"-{stats.get('avg_reduction', 0):.1f}%",
                        delta_color="inverse"
                    )

                with col2:
                    st.metric(
                        "Compression Method",
                        stats.get('method', 'Unknown').title()
                    )
                    st.metric(
                        "Quality Preset",
                        stats.get('quality', 'Unknown').title()
                    )

            # Exhibit list
            st.divider()
            st.subheader("📋 Exhibit List")

            for exhibit in st.session_state.exhibit_list:
                with st.expander(f"Exhibit {exhibit['number']}: {exhibit['title']}"):
                    st.write(f"**Original File**: {exhibit['filename']}")
                    st.write(f"**Pages**: {exhibit.get('pages', 'Unknown')}")
                    if 'compression' in exhibit and exhibit['compression']:
                        st.write(f"**Compressed**: {exhibit['compression']['reduction']:.1f}% reduction")
                        st.write(f"**Method**: {exhibit['compression']['method']}")

            # Download button
            st.divider()
            if 'output_file' in st.session_state:
                with open(st.session_state.output_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download Exhibit Package",
                        data=f,
                        file_name=f"Exhibit_Package_{visa_type}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
        else:
            st.info("👈 Upload files and click 'Generate Exhibits' to see results here")

def generate_exhibits(
    files,
    visa_type: str,
    numbering_style: str,
    enable_compression: bool,
    quality_preset: str,
    smallpdf_api_key: Optional[str],
    add_toc: bool,
    add_archive: bool,
    merge_pdfs: bool
):
    """Generate exhibit package from uploaded files"""

    with st.spinner("🔄 Processing files..."):
        try:
            # Create PDF handler with compression settings
            pdf_handler = PDFHandler(
                enable_compression=enable_compression,
                quality_preset=quality_preset,
                smallpdf_api_key=smallpdf_api_key
            )

            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Save uploaded files
                file_paths = []

                progress_bar = st.progress(0)
                status_text = st.empty()

                # Handle file upload
                for i, file in enumerate(files):
                    if hasattr(file, 'name'):  # Streamlit uploaded file
                        file_path = os.path.join(tmp_dir, file.name)
                        with open(file_path, 'wb') as f:
                            f.write(file.read())
                    else:  # File path (from ZIP)
                        file_path = file

                    file_paths.append(file_path)
                    progress_bar.progress((i + 1) / len(files))
                    status_text.text(f"Saving file {i+1}/{len(files)}")

                status_text.text("✓ All files saved")

                # Compression phase
                compression_results = []
                total_original_size = 0
                total_compressed_size = 0

                if enable_compression:
                    status_text.text("🗜️ Compressing PDFs...")

                    for i, file_path in enumerate(file_paths):
                        result = pdf_handler.compressor.compress(file_path) if pdf_handler.compressor else {'success': False}

                        if result['success']:
                            compression_results.append(result)
                            total_original_size += result['original_size']
                            total_compressed_size += result['compressed_size']

                            status_text.text(
                                f"🗜️ Compressed {i+1}/{len(file_paths)}: "
                                f"{result['reduction_percent']:.1f}% reduction ({result['method']})"
                            )

                        progress_bar.progress((i + 1) / len(file_paths))

                    # Calculate average compression
                    if compression_results:
                        avg_reduction = (1 - total_compressed_size / total_original_size) * 100 if total_original_size > 0 else 0

                        st.session_state.compression_stats = {
                            'original_size': total_original_size,
                            'compressed_size': total_compressed_size,
                            'avg_reduction': avg_reduction,
                            'method': compression_results[0]['method'] if compression_results else 'none',
                            'quality': quality_preset
                        }

                        status_text.text(f"✓ Compression complete: {avg_reduction:.1f}% average reduction")

                # Number exhibits
                status_text.text("📝 Numbering exhibits...")

                exhibit_list = []
                numbered_files = []

                for i, file_path in enumerate(file_paths):
                    # Get exhibit number
                    if numbering_style == "letters":
                        exhibit_num = chr(65 + i)  # A, B, C...
                    elif numbering_style == "numbers":
                        exhibit_num = str(i + 1)  # 1, 2, 3...
                    else:  # roman
                        exhibit_num = to_roman(i + 1)  # I, II, III...

                    # Add exhibit number to PDF
                    numbered_file = pdf_handler.add_exhibit_number(file_path, exhibit_num)
                    numbered_files.append(numbered_file)

                    # Track exhibit info
                    exhibit_info = {
                        'number': exhibit_num,
                        'title': Path(file_path).stem,
                        'filename': os.path.basename(file_path),
                        'pages': get_pdf_page_count(file_path)
                    }

                    # Add compression info if available
                    if i < len(compression_results) and compression_results[i]['success']:
                        exhibit_info['compression'] = {
                            'reduction': compression_results[i]['reduction_percent'],
                            'method': compression_results[i]['method']
                        }

                    exhibit_list.append(exhibit_info)

                    progress_bar.progress((i + 1) / len(file_paths))
                    status_text.text(f"📝 Numbered exhibit {exhibit_num}")

                st.session_state.exhibit_list = exhibit_list

                # Generate TOC if requested
                if add_toc:
                    status_text.text("📋 Generating Table of Contents...")
                    toc_file = pdf_handler.generate_table_of_contents(
                        exhibit_list,
                        visa_type,
                        os.path.join(tmp_dir, "TOC.pdf")
                    )
                    numbered_files.insert(0, toc_file)

                # Merge PDFs if requested
                if merge_pdfs:
                    status_text.text("📦 Merging PDFs...")
                    output_file = os.path.join(tmp_dir, "final_package.pdf")
                    merged_file = pdf_handler.merge_pdfs(numbered_files, output_file)

                    # Save to session state for download
                    final_output = os.path.join(tempfile.gettempdir(), f"exhibit_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                    import shutil
                    shutil.copy(merged_file, final_output)
                    st.session_state.output_file = final_output

                progress_bar.progress(100)
                status_text.text("✓ Generation complete!")

                st.session_state.exhibits_generated = True
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error generating exhibits: {str(e)}")
            import traceback
            with st.expander("Error Details"):
                st.code(traceback.format_exc())

def get_pdf_page_count(pdf_path: str) -> int:
    """Get number of pages in PDF"""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except:
        return 0

def to_roman(num: int) -> str:
    """Convert number to Roman numeral"""
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num

if __name__ == "__main__":
    main()
