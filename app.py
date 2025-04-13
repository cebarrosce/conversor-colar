from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def obter_cotacao_dolar():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        cotacao = float(dados['USDBRL']['bid'])
        return cotacao
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Erro ao obter cotação: {e}")
        return None

def converter_reais_para_dolar(valor_reais, cotacao):
    return valor_reais / cotacao

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ""
    if request.method == 'POST':
        try:
            valor_reais = float(request.form['valor_reais'])
            cotacao = obter_cotacao_dolar()
            if cotacao:
                valor_dolares = converter_reais_para_dolar(valor_reais, cotacao)
                resultado = f'Cotação atual do dólar: R$ {cotacao:.2f}<br>Valor convertido: US$ {valor_dolares:.2f}'
            else:
                resultado = "Não foi possível obter a cotação do dólar."
        except ValueError:
            resultado = "Digite um número válido."
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)