from flask import Flask, request, render_template
import requests
import random

app = Flask(__name__)

API_ENDPOINT = 'https://api.disneyapi.dev/character'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    nome = request.form.get('nome', None)

    if not nome:
        return render_template('index.html', erro="Você precisa informar um nome!")

    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        dados = response.json()['data']

        if not dados:
            return render_template('index.html', erro="Oh não! O pato Donald se perdeu na confusão. Tente novamente!")

        # Lógica para determinar o personagem (baseado no comprimento do nome)
        comprimento_nome = len(nome)
        qtdA = nome.lower().count('a')
        indice_personagem = comprimento_nome % len(dados) + qtdA
        personagem_sorteado = dados[indice_personagem]

        return render_template('index.html', nome=nome, personagem=personagem_sorteado)

    except requests.exceptions.RequestException as e:
        return render_template('index.html', erro=f"Oh não! O pato Donald se perdeu na confusão. Tente novamente! (Erro técnico: {e})") # Mantendo o erro original
    except (KeyError, IndexError) as e:
        return render_template('index.html', erro=f"Oh não! O pato Donald se perdeu na confusão. Tente novamente! (Erro técnico: {e})") # Mantendo o erro original


if __name__ == '__main__':
    app.run()