from coleta.soccer_stats import scrap_soccer_data
from utils.juntar_csvs import juntar_csvs
from flask import Flask, app, jsonify, request
import os

from utils.csv_para_json import csv_para_json

app = Flask(__name__)

# Rota para buscar os arquivos via api e retornar JSON
@app.route('/arquivos/<ano>/<rodada>/<nome_arquivo>', methods=['GET'])
def obter_arquivo_json(ano, rodada, nome_arquivo):
  diretorio_arquivos = f'./arquivos/{ano}/rodada{rodada}'
  file_path = os.path.join(diretorio_arquivos, f'{nome_arquivo}.csv')

  if not os.path.exists(file_path):
    return jsonify({"error": "Arquivo não encontrado"}), 404

  json_data = csv_para_json(file_path)
  return jsonify(json_data)

# Buscar os arquivos
def busca_arquivos():
  PASTA_DESTINO = "./tmp"
  DIRETORIO_ARQUIVOS = './arquivos/2023/rodada38'
  DIRETORIO_DESTINO = './arquivos/arquivo_junto'
  
  urls = [
    "https://fbref.com/en/comps/24/Serie-A-Stats",
  ]

  scrap_soccer_data(urls, PASTA_DESTINO)
  
  juntar_csvs(DIRETORIO_ARQUIVOS, DIRETORIO_DESTINO)

if __name__ == "__main__":
  busca_arquivos()
  app.run(debug=True)