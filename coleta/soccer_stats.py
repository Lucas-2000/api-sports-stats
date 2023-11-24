# Importação das bibliotecas
import requests
from bs4 import BeautifulSoup
from utils.salvar_em_csv import salvar_em_csv
import os
from lxml import html

def scrap_soccer_data(urls, pasta_destino):
  for url in urls:
    response = requests.get(url)
    if url == "https://fbref.com/en/comps/24/Serie-A-Stats":
      if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        hidden_table_homeaway = html.fromstring(response.content)

        regular_season = soup.find('div', id='switcher_results2023241')
        if regular_season:
          regular_season_overall_table = regular_season.find('table')
        
          if regular_season_overall_table:
            header_regular_overall_season, dados_regular_overall_season = regular_season_overall_data(regular_season_overall_table)
            
            nome_arquivo = os.path.join(pasta_destino, 'regular_overall_season_serie_a.csv')

            salvar_em_csv(nome_arquivo, header_regular_overall_season, dados_regular_overall_season)
        
        header_xpath_regular_homeaway_table = '//*[@id="div_results2023241_home_away"]//thead/tr/th'
        body_xpath_regular_homeaway_table = '//*[@id="div_results2023241_home_away"]//tbody/tr'
        
        if header_xpath_regular_homeaway_table and body_xpath_regular_homeaway_table:
          header_regular_homeaway_season, body_regular_homeaway_season = regular_season_homeaway_data(header_xpath_regular_homeaway_table, body_xpath_regular_homeaway_table, hidden_table_homeaway)
        
          if header_regular_homeaway_season and body_regular_homeaway_season:
            nome_arquivo = os.path.join(pasta_destino, 'regular_overall_homeaway_serie_a.csv')
            salvar_em_csv(nome_arquivo, header_regular_homeaway_season, body_regular_homeaway_season)

def regular_season_overall_data(table):
  header = []
  dados_linhas = []

  if table:
    cabecalho = table.find('thead')
    dados = table.find('tbody')

    if cabecalho:
      header = [th.get_text(strip=True) for th in cabecalho.find_all('th')]

    if dados:
      linhas = dados.find_all('tr')
      for linha in linhas:
        linha_dados = [td.get_text(strip=True) for td in linha.find_all('td')]
                
        if len(linha_dados) < len(header):
          linha_dados.append('') 
                
        dados_linhas.append(linha_dados)

  return header, dados_linhas


def regular_season_homeaway_data(header_xpath, body_xpath, hidden_table_homeaway):
  header = []

  if header_xpath:
    header_elements = hidden_table_homeaway.xpath(header_xpath)
    header = [elem.text_content().strip() for elem in header_elements][4:]

  data = []

  if body_xpath:
    body_elements = hidden_table_homeaway.xpath(body_xpath)
    data = [[td.text_content().strip() for td in elem.xpath(".//td")] for elem in body_elements]

  return header, data