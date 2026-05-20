import opencc
from docx import Document
from replace_with_json_dict import load_replacements

def convert_docx_chinese(input_file, conversion_type, extra_s2t_conversion_json_path='hk2mo.json'):
    """
    Convert Simplified Chinese to Traditional Chinese (or vice versa) in a DOCX file,
    including all tables, headers, footers, and textboxes.
    
    Args:
        input_file (file-like object): The input .docx file
        conversion_type (str): OpenCC conversion type (e.g., 's2hk', 't2s')
        extra_s2t_conversion_json_path (str): Path to additional JSON mapping (only used when conversion_type == 's2hk')
    
    Returns:
        Document: Modified python-docx Document object
    """
    # Initialize OpenCC converter
    cc = opencc.OpenCC(f'{conversion_type}.json')
    
    # Preload extra replacements if needed (only once)
    extra_replacements = None
    if conversion_type == 's2hk':
        extra_replacements = load_replacements(extra_s2t_conversion_json_path)
    
    # Load document
    doc = Document(input_file)
    
    def convert_text(text):
        """Apply OpenCC conversion and optional extra replacements."""
        if not text:
            return text
        converted = cc.convert(text)
        if extra_replacements:
            for old, new in extra_replacements.items():
                converted = converted.replace(old, new)
        return converted
    
    def convert_runs_in_paragraphs(paragraphs):
        """Convert text in all runs of given paragraphs."""
        for para in paragraphs:
            for run in para.runs:
                if run.text:  # process even if only spaces, but skip None/empty
                    run.text = convert_text(run.text)
    
    def process_table(table):
        """Recursively process all cells in a table and nested tables."""
        for row in table.rows:
            for cell in row.cells:
                convert_runs_in_paragraphs(cell.paragraphs)
                for nested_table in cell.tables:
                    process_table(nested_table)
    
    # 1. Main document paragraphs
    convert_runs_in_paragraphs(doc.paragraphs)
    
    # 2. Tables (top-level)
    for table in doc.tables:
        process_table(table)
    
    # 3. Headers and Footers (often contain tables too)
    for section in doc.sections:
        # Header
        convert_runs_in_paragraphs(section.header.paragraphs)
        for table in section.header.tables:
            process_table(table)
        # Footer
        convert_runs_in_paragraphs(section.footer.paragraphs)
        for table in section.footer.tables:
            process_table(table)
    
    return doc