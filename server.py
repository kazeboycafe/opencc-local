import os
import logging
from flask import Flask, request, jsonify, send_file, render_template
from io import BytesIO
import opencc
from replace_with_json_dict import load_replacements
import opencc_docx

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Preload converters
CONVERTERS = {
    's2hk': opencc.OpenCC('s2hk.json'),
    't2s': opencc.OpenCC('t2s.json')
}

# Preload extra replacements for s2hk (optional)
EXTRA_REPLACEMENTS = load_replacements('hk2mo.json')

@app.route('/')
def index():
    return render_template('index.html')  # ensure the templates folder had index.html

@app.route('/convert', methods=['POST'])
def convert_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        conversion = data.get('conversion', '')

        if not text:
            return jsonify({'error': 'Text is empty'}), 400
        if conversion not in CONVERTERS:
            return jsonify({'error': 'Invalid conversion type'}), 400

        converted = CONVERTERS[conversion].convert(text)
        if conversion == 's2hk' and EXTRA_REPLACEMENTS:
            for old, new in EXTRA_REPLACEMENTS.items():
                converted = converted.replace(old, new)

        return jsonify({'convertedText': converted})
    except Exception as e:
        logging.exception("Text conversion error")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/convert_docx', methods=['POST'])
def convert_docx():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if not file.filename.lower().endswith('.docx'):
            return jsonify({'error': 'Only .docx files are allowed'}), 400
        
        conversion = request.form.get('conversion', 's2hk')
        if conversion not in ['s2hk', 't2s']:
            return jsonify({'error': 'Invalid conversion type'}), 400

        # Read file into memory
        input_bytes = BytesIO(file.read())
        
        # Convert the DOCX file (table-aware version)
        output_doc = opencc_docx.convert_docx_chinese(
            input_bytes,
            conversion_type=conversion,
            extra_s2t_conversion_json_path='hk2mo.json'
        )
        
        output_bytes = BytesIO()
        output_doc.save(output_bytes)
        output_bytes.seek(0)
        
        # Generate output filename
        base, ext = os.path.splitext(file.filename)
        suffix = '(t)' if conversion == 's2hk' else '(s)'
        download_name = f"{base}{suffix}{ext}"
        
        return send_file(
            output_bytes,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        logging.exception("DOCX conversion error")
        return jsonify({'error': f'DOCX conversion failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Server running at http://127.0.0.1:15733")
    app.run(debug=True, port=15733)