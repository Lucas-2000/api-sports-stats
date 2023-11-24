import pandas as pd

def salvar_em_csv(nome_arquivo, header, dados):
    df = pd.DataFrame(dados, columns=header)
    df.to_csv(nome_arquivo, index=False)