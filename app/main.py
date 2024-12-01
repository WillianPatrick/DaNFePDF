from flask import Flask, request, send_file, jsonify
from lxml import etree
from pytrustnfe.nfe.danfe import danfe
from io import BytesIO
import traceback



app = Flask(__name__)
@app.route('/', methods=['GET'])
def health():
    try:
        # Verificação básica de saúde do serviço
        return jsonify({'status': 'healthy', 'message': 'Service is running'}), 200
    except Exception as e:
        print("Erro no health check:", str(e))
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
    
@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Verificar se um arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        if file:
            # Ler o conteúdo do arquivo
            nfe_xml_content = file.read()
            # Analisar o conteúdo XML
            xml_element = etree.fromstring(nfe_xml_content)
            oDanfe = danfe(list_xml=[xml_element])

            # Gerar a DANFE
            pdf_io = BytesIO()
            oDanfe.writeto_pdf(pdf_io)
            pdf_io.seek(0)

            # Retornar o PDF como resposta
            return send_file(
                pdf_io,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='danfe.pdf'
            )
        else:
            return jsonify({'error': 'Arquivo não permitido'}), 400
    except Exception as e:
        print("Erro ao gerar DANFE:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
