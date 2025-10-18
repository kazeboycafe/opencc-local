import sys
import opencc
import argparse
from docx import Document

import json

def replace_with_json_dict(text, json_path):
    """
    Replace substrings in `text` based on a JSON dictionary loaded from `json_path`.
    
    Args:
        text (str): Input text
        json_path (str): Path to JSON file containing {"old": "new", ...}
    
    Returns:
        str: Text with replacements applied
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        replacements = json.load(f)
    
    # Apply replacements
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def convert_docx_chinese(input_path, output_path, conversion_type='s2mo', json_path='hk2mo.json'):
    """
    Convert Simplified Chinese to Traditional Chinese in a DOCX file while preserving formatting.
    
    Args:
        input_path (str): Path to input DOCX file
        output_path (str): Path for output DOCX file
        conversion_type (str): OpenCC conversion type (default: 's2mo')
    """
    # Initialize OpenCC converter
    if conversion_type == 's2mo':
        opencc_conversion_type = 's2hk'  # first convert to Traditional (Hong Kong)
    else:
        opencc_conversion_type = conversion_type

    cc = opencc.OpenCC(f'{opencc_conversion_type}.json')
    
    # Load document
    doc = Document(input_path)
    
    def convert_runs_in_paragraphs(paragraphs):
        """Helper to convert text in runs of a list of paragraphs."""
        for para in paragraphs:
            for run in para.runs:
                if run.text.strip():
                    run.text = cc.convert(run.text)

                    #further replace the text in the json path if conversion_type is s2mo
                    if conversion_type == 's2mo':
                        run.text = replace_with_json_dict(run.text, json_path)
                    



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
    
    # Save converted document
    doc.save(output_path)
    print(f"Converted document saved to: {output_path}")




    
def main():
    parser = argparse.ArgumentParser(
        description="Convert Simplified Chinese to Traditional Chinese in a DOCX file while preserving formatting."
    )
    parser.add_argument('input', help="Input file path (.docx or .doc)")
    parser.add_argument(
        'output',
        nargs='?',
        help="Output file path (optional). If not given, '(t)' is inserted before the extension (e.g., file.docx → file(t).docx)."
    )
    parser.add_argument(
        '--type',
        default='s2mo',
        choices=['s2mo', 't2s'],
        help="OpenCC conversion type (default: s2mo). "
             "s2mo (to Macau standard), "
             "t2s (Traditional to Simplified)."
    )

    args = parser.parse_args()

    # Auto-generate output filename if not provided
    if args.output is None:
        import os
        base, ext = os.path.splitext(args.input)

        if args.type == 's2mo':
            # Preserve original extension (case-insensitive)
            args.output = f"{base}(t){ext}"
        elif args.type == 't2s':
            # Preserve original extension (case-insensitive)
            args.output = f"{base}(s){ext}"


    # Optional: Warn if .doc is used (since python-docx doesn't support it)
    input_ext = os.path.splitext(args.input)[1].lower()
    output_ext = os.path.splitext(args.output)[1].lower()
    if input_ext == '.doc' or output_ext == '.doc':
        print(
            "Warning: .doc files are not supported by python-docx. "
            "Only .docx files can be processed. This will likely fail.",
            file=sys.stderr
        )

    try:
        convert_docx_chinese(args.input, args.output, conversion_type=args.type)
        print(f"Conversion completed successfully! Output saved to: {args.output}")
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()