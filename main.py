from coleta.soccer_stats import scrap_soccer_data
from utils.juntar_csvs import juntar_csvs

def main():
  PASTA_DESTINO = "./tmp"
  DIRETORIO_ARQUIVOS = './arquivos/2023/rodada38'
  DIRETORIO_DESTINO = './arquivos/arquivo_junto'
  
  urls = [
    "https://fbref.com/en/comps/24/Serie-A-Stats",
  ]

  scrap_soccer_data(urls, PASTA_DESTINO)
  
  juntar_csvs(DIRETORIO_ARQUIVOS, DIRETORIO_DESTINO)

if __name__ == "__main__":
  main()