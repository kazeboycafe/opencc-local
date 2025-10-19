import os
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import opencc
from replace_with_json_dict import replace_with_json_dict
import opencc_docx

app = Flask(__name__)

# Initialize converters (do this once at startup for efficiency)
CONVERTERS = {
    's2hk': opencc.OpenCC('s2hk.json'),  # Simplified to Traditional (Hong Kong)
    't2s': opencc.OpenCC('t2s.json')   # Traditional to Simplified
}

@app.route('/')
def index():
    return render_template('index.html')

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

        # Perform conversion
        converted = CONVERTERS[conversion].convert(text)
        if conversion == 's2hk':
            # Further replace the text using the hk2mo.json mapping
            converted = replace_with_json_dict(converted, 'hk2mo.json')
            
        return jsonify({'convertedText': converted})

    except Exception as e:
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/convert_docx', methods=['POST'])
def convert_docx():
    #use the opencc_docx.py function to convert docx files
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if not file.filename.lower().endswith('.docx'):
            return jsonify({'error': 'Only .docx files are allowed'}), 400
        
        conversion = request.form.get('conversion', 's2mo')
        
        # Read file into memory
        input_file = file.read()

        # Wrap bytes in BytesIO to make it file-like
        input_file = BytesIO(input_file)
        
        # Convert the DOCX file
        output_file = opencc_docx.convert_docx_chinese(input_file, conversion_type=conversion, extra_s2t_conversion_json_path='hk2mo.json')
        
        output_bytes = BytesIO()
        output_file.save(output_bytes)
        output_bytes.seek(0)
        
        base, ext = os.path.splitext(file.filename)
        if conversion == 's2hk':
            # Preserve original extension (case-insensitive)
            download_name = f"{base}(t){ext}"
        elif conversion == 't2s':
            # Preserve original extension (case-insensitive)
            download_name = f"{base}(s){ext}"

        print(download_name)

        return send_file(
            BytesIO(output_bytes.getvalue()),
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment = True,
            download_name = download_name
        )
    

    except Exception as e:
        return jsonify({'error': f'DOCX conversion failed: {str(e)}'}), 500

if __name__ == '__main__':
    #use port 15733
    app.run(debug=True, host='0.0.0.0', port=15733)