# app.py
from flask import Flask, render_template, request, jsonify
import qrcode
import base64
import io
import os
from datetime import datetime

app = Flask(__name__)

# Configurações do PIX da igreja (substituir com as informações reais)
PIX_KEY = "igreja@exemplo.com.br"
PIX_NAME = "Igreja Boas Novas"
PIX_CITY = "São Paulo"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_pix', methods=['POST'])
def generate_pix():
    try:
        data = request.get_json()
        amount = data.get('amount', '0.00')
        name = data.get('name', '')

        # Formatar o valor sem vírgulas para formar o PIX
        amount_formatted = amount.replace(',', '.')

        # Criação do payload PIX (Versão simplificada)
        # Em produção, deve-se usar uma biblioteca específica para PIX
        transaction_id = datetime.now().strftime('%Y%m%d%H%M%S')
        pix_payload = f"00020126330014BR.GOV.BCB.PIX01{len(PIX_KEY)}{PIX_KEY}5204000053039865802BR5913{PIX_NAME}6008{PIX_CITY}62090505{transaction_id}6304"

        # Gerando o QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pix_payload)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convertendo a imagem para base64
        buffered = io.BytesIO()
        img.save(buffered)
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            'status': 'success',
            'qr_code': img_str,
            'pix_key': PIX_KEY,
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)