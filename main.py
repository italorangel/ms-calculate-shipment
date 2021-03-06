from flask import Flask, request, jsonify

app = Flask(__name__)

shipping_companies = {
    'transportadoras': [
        {
            'nome': 'Ninja',
            'altura_minima': 10,
            'altura_maxima': 200,
            'largura_minima': 6,
            'largura_maxima': 140,
            'prazo_entrega': 6,
            'valor_frete': 0.3
        }, {
            'nome': 'KaBuM',
            'altura_minima': 5,
            'altura_maxima': 140,
            'largura_minima': 13,
            'largura_maxima': 125,
            'prazo_entrega': 4,
            'valor_frete': 0.2
        }
    ]
}


@app.route('/')
def root():
    return 'Microsserviço para calculo do frete'


@app.route('/shipping-companies', methods=['GET'])
def get_all_shipping_company():
    if request.method == 'GET':
        names = []
        for shipping_company in shipping_companies['transportadoras']:
            names.append(shipping_company['nome'])
        return jsonify(names)


@app.route('/shipping-company/<company>', methods=['GET'])
def get_shipping_company(company=None):
    if request.method == 'GET':
        for shipping_company in shipping_companies['transportadoras']:
            if shipping_company['nome'] == company:
                return shipping_company


@app.route('/calculate-shipping', methods=['POST'])
def calculate_shipping():
    if request.method == 'POST':
        json_data = request.get_json()
        shipment_values = []
        # Zen Of Python - Beautiful is better than ugly.
        if json_data:
            for shipping_company in shipping_companies['transportadoras']:
                if json_data['dimensao']['altura'] < shipping_company['altura_maxima']:
                    if json_data['dimensao']['altura'] > shipping_company['altura_minima']:
                        # Verifica a largura
                        if json_data['dimensao']['largura'] < shipping_company['largura_maxima']:
                            if json_data['dimensao']['largura'] > shipping_company['largura_minima']:
                                # Calcula o valor do frete
                                valor = _calculate_value_shipment(json_data['peso'], shipping_company['valor_frete'])
                                shipment_values.append(
                                    {'nome': 'Entrega ' + shipping_company['nome'], 'valor_frete': valor,
                                     'prazo_dias': shipping_company['prazo_entrega']})
        return jsonify(shipment_values)


def _calculate_value_shipment(peso, valor_frete):
    return (peso * valor_frete) / 10


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
