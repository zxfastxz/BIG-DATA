import pandas as pd
import requests
from time import sleep

def acessar_api(url, tentativas=3, espera=2):
   
    for i in range(tentativas):
        try:
            resposta = requests.get(url, timeout=10)
            if resposta.status_code == 200:
                return resposta.json()
            else:
                print(f"Erro {resposta.status_code} na URL: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na conexão: {e}")
        sleep(espera)
    return None


urls = []
for ano in range(2023, 2026):
    for mes in range(1, 13):
        dia = "01"  
        data = f"{ano}-{mes:02d}-{dia}"  
        url = f"https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/ChavesPix(Data=@Data)?@Data='{data}'&$top=200&$format=json"
        urls.append(url)


todos_dados = []

print("Coletando dados de Chaves Pix 2023-2025...")

for idx, url in enumerate(urls, start=1):
    dados = acessar_api(url)
    if dados and 'value' in dados:
        todos_dados.extend(dados['value'])
    print(f"[{idx}/{len(urls)}] Mes coletado. Total de registros: {len(todos_dados)}")

print("Coleta finalizada!")


df = pd.json_normalize(todos_dados) 

df.to_csv("chaves_pix_2023_2025.csv", index=False, encoding="utf-8-sig")
print("CSV salvo com sucesso: chaves_pix_2023_2025.csv")
