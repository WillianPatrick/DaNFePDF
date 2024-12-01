from flask import Flask, request, send_file, jsonify
from lxml import etree
from pytrustnfe.nfe.danfe import danfe
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Obter o XML do corpo da requisição
        nfe_xml = request.data.decode('utf-8')
        print("XML recebido:", nfe_xml)

        # Verificar se o dado é um caminho de arquivo válido
        if nfe_xml.strip().endswith('.xml') and os.path.exists(nfe_xml.strip()):
            # Ler o conteúdo do arquivo XML
            with open(nfe_xml.strip(), 'r', encoding='utf-8') as file:
                nfe_xml_content = file.read()
        else:
            # Caso contrário, tratar como o próprio conteúdo do XML
            nfe_xml_content = nfe_xml

        print("Conteúdo do XML para DANFE:", nfe_xml_content)

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
    except Exception as e:
        print("Erro ao gerar DANFE:", str(e))  # Log do erro
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
