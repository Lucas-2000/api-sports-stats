from coleta.soccer_stats import scrap_soccer_data

def main():
  PASTA_DESTINO = "./tmp"
  
  urls = [
    "https://fbref.com/en/comps/24/Serie-A-Stats",
  ]

  scrap_soccer_data(urls, PASTA_DESTINO)

if __name__ == "__main__":
  main()