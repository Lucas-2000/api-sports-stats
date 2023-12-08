import pandas as pd
import os

def juntar_csvs(diretorio_arquivos, diretorio_destino):
  lista_dataframes = []
  nomes_abas = []  # Lista para armazenar os nomes das abas
    
  for filename in os.listdir(diretorio_arquivos):
    if filename.endswith('.csv'):
      filepath = os.path.join(diretorio_arquivos, filename)
      df = pd.read_csv(filepath)
      lista_dataframes.append(df)
            
            # Obtém o nome base do arquivo sem a extensão .csv
      nome_aba = os.path.splitext(filename)[0][:31]
      nomes_abas.append(nome_aba)

  nome_arquivo_final = os.path.join(diretorio_destino, 'todos_arquivos.xlsx')
  with pd.ExcelWriter(nome_arquivo_final) as writer:
    for idx, (nome_aba, df) in enumerate(zip(nomes_abas, lista_dataframes), start=1):
            # Use o nome da aba correspondente a cada DataFrame
      df.to_excel(writer, sheet_name=nome_aba, index=False)
    