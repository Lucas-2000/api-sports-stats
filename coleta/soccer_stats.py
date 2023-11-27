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
        xpath_html = html.fromstring(response.content)

        regular_season = soup.find('div', id='switcher_results2023241')
        if regular_season:
          regular_season_overall_table = regular_season.find('table')
        
          if regular_season_overall_table:
            header_regular_overall_season, dados_regular_overall_season = get_header_and_body(regular_season_overall_table)
            
            nome_arquivo = os.path.join(pasta_destino, 'regular_overall_season_serie_a.csv')

            salvar_em_csv(nome_arquivo, header_regular_overall_season, dados_regular_overall_season)
        
        header_xpath_regular_homeaway_table = '//*[@id="div_results2023241_home_away"]//thead/tr/th'
        body_xpath_regular_homeaway_table = '//*[@id="div_results2023241_home_away"]//tbody/tr'
        
        if header_xpath_regular_homeaway_table and body_xpath_regular_homeaway_table:
          header_regular_homeaway_season, body_regular_homeaway_season = get_header_and_body_by_xpath(header_xpath_regular_homeaway_table, body_xpath_regular_homeaway_table, xpath_html, 4)
        
          if header_regular_homeaway_season and body_regular_homeaway_season:
            nome_arquivo = os.path.join(pasta_destino, 'regular_overall_homeaway_serie_a.csv')
            salvar_em_csv(nome_arquivo, header_regular_homeaway_season, body_regular_homeaway_season)
      
        standard_stats = soup.find('div', id='div_stats_squads_standard_for')
        if standard_stats:
          standard_stats_squad_table = standard_stats.find('table')
        
          header_standard_stats_squad, data_standard_stats_squad = get_header_and_body_and_remove_header_options(standard_stats_squad_table, 6)
          
          nome_arquivo = os.path.join(pasta_destino, 'standard_stats_squad_serie_a.csv')

          salvar_em_csv(nome_arquivo, header_standard_stats_squad, data_standard_stats_squad)
          
        header_xpath_squad_standard_stats_opponent_table = '//*[@id="div_stats_squads_standard_against"]//thead/tr/th'
        body_xpath_squad_standard_stats_opponent_table = '//*[@id="div_stats_squads_standard_against"]//tbody/tr'
        
        if header_xpath_squad_standard_stats_opponent_table and body_xpath_squad_standard_stats_opponent_table:
          header_squad_standard_stats_opponent, body_squad_standard_stats_opponent = get_header_and_body_by_xpath_with_more_elements(header_xpath_squad_standard_stats_opponent_table, body_xpath_squad_standard_stats_opponent_table, xpath_html, 6)
          
          if header_squad_standard_stats_opponent and body_squad_standard_stats_opponent:
            nome_arquivo = os.path.join(pasta_destino, 'squad_standard_stats_opponent_serie_a.csv')
            salvar_em_csv(nome_arquivo, header_squad_standard_stats_opponent, body_squad_standard_stats_opponent)
    

def get_header_and_body(table):
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
        colunas = linha.find_all(['th', 'td'])
        linha_dados = [col.get_text(strip=True) for col in colunas]
                
        if len(linha_dados) < len(header):
          linha_dados.append('') 
                
        dados_linhas.append(linha_dados)

  return header, dados_linhas

def get_header_and_body_by_xpath(header_xpath, body_xpath, xpath_html, quantity):
  header = []

  if header_xpath:
    header_elements = xpath_html.xpath(header_xpath)
    header = [elem.text_content().strip() for elem in header_elements][quantity:]

  data = []

  if body_xpath:
    body_elements = xpath_html.xpath(body_xpath)
    data = [[td.text_content().strip() for td in elem.xpath(".//td")] for elem in body_elements]

  return header, data

def get_header_and_body_and_remove_header_options(table, quantity):
  header = []
  dados_linhas = []

  if table:
    cabecalho = table.find('thead')
    dados = table.find('tbody')

    if cabecalho:
      header = [th.get_text(strip=True) for th in cabecalho.find_all('th')]
      if quantity:
        header = header[quantity:]

      if dados:
        linhas = dados.find_all('tr')
        for linha in linhas:
          colunas = linha.find_all(['th', 'td'])
          linha_dados = [col.get_text(strip=True) for col in colunas]
          
          if len(linha_dados) < len(header):
            linha_dados.append('') 

          dados_linhas.append(linha_dados)

  return header, dados_linhas

def get_header_and_body_by_xpath_with_more_elements(header_xpath, body_xpath, xpath_html, quantity):
  header = []

  if header_xpath:
    header_elements = xpath_html.xpath(header_xpath)
    header = [elem.text_content().strip() for elem in header_elements][quantity:]

  data = []

  if body_xpath:
    body_elements = xpath_html.xpath(body_xpath)
    for elem in body_elements:
      row = [elem.xpath(".//th")[0].text_content().strip()] + [td.text_content().strip() for td in elem.xpath(".//td")]
      data.append(row)

  return header, data