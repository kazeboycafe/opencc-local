import sys
import opencc
import argparse
from docx import Document
from replace_with_json_dict import replace_with_json_dict


def convert_docx_chinese(input_file, conversion_type, extra_s2t_conversion_json_path='hk2mo.json'):
    """
    Convert Simplified Chinese to Traditional Chinese in a DOCX file while preserving formatting.
    
    Args:
        input_file (file-like object): The input .docx file
        conversion_type (str): OpenCC conversion type (default: 's2hk')
        extra_s2t_conversion_json_path (str): Path to additional JSON mapping for further s2t conversion (default: 'hk2mo.json')
    """
    
    cc = opencc.OpenCC(f'{conversion_type}.json')
    
    # Load document
    doc = Document(input_file)
    
    
    def convert_runs_in_paragraphs(paragraphs):
        """Helper to convert text in runs of a list of paragraphs."""
        for para in paragraphs:
            for run in para.runs:
                if run.text.strip():
                    run.text = cc.convert(run.text)
                    
                    #further replace the text in the json path if extra_s2t_conversion_json_path is provided
                    if conversion_type == 's2hk':
                        run.text = replace_with_json_dict(run.text, extra_s2t_conversion_json_path)
                    

    # Process paragraphs in the main document
    convert_runs_in_paragraphs(doc.paragraphs)
    
    # Process tables (including nested tables)
    def process_table(table):
        for row in table.rows:
            for cell in row.cells:
                # Process paragraphs in the cell
                convert_runs_in_paragraphs(cell.paragraphs)
                # Recursively process nested tables
                for nested_table in cell.tables:
                    process_table(nested_table)

    for table in doc.tables:
        process_table(table)
    
    #return the doc
    return doc
    