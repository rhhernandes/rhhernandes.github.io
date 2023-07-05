
import csv
import requests
from bs4 import BeautifulSoup

# List of URLs
# List of URLs
urls = [
    'https://www1.folha.uol.com.br/tec/2021/02/hackers-miram-empresas-de-vacinas-e-saude-na-pandemia.shtml',
    'https://temas.folha.uol.com.br/artificial-intelligence/',
    'https://www1.folha.uol.com.br/poder/2021/02/custo-de-voto-em-mulheres-chega-a-ser-quase-70-vezes-mais-caro-que-em-homens.shtml',
    'https://www1.folha.uol.com.br/ilustrada/2019/09/tecnologia-pode-tirar-ciencias-humanas-da-idade-media-diz-pierre-levy.shtml',
    'https://www1.folha.uol.com.br/ambiente/2019/04/papagaio-que-levou-tiro-mordida-de-cobra-e-foi-roubado-volta-sozinho-para-zoologico.shtml',
    'https://www1.folha.uol.com.br/poder/2018/10/urna-eletronica-chega-a-12a-eleicao-no-pais-sob-ataque-inedito.shtml',
    'https://www1.folha.uol.com.br/tec/2023/07/inteligencias-artificiais-envenenadas-sao-problema-sem-solucao.shtml',
    'https://www1.folha.uol.com.br/tec/2023/07/clones-digitais-com-inteligencia-artificial-baguncam-entendimento-de-realidade.shtml',
    'https://www1.folha.uol.com.br/tec/2023/05/problema-com-chatgpt-e-dar-ideia-de-competencia-onde-nao-ha-diz-pesquisador.shtml',
    'https://www1.folha.uol.com.br/cotidiano/2023/05/discord-vira-terra-sem-lei-com-grupos-que-encorajam-crimes-sexuais-e-violencia.shtml',
    'https://www1.folha.uol.com.br/educacao/2023/05/enem-mostra-que-chatgpt-domina-decoreba-e-interpretacao-de-texto.shtml',
    'https://www1.folha.uol.com.br/educacao/2023/04/chatgpt-e-melhor-que-80-dos-alunos-no-enem-mas-derrapa-em-matematica.shtml',
    'https://www1.folha.uol.com.br/ambiente/2023/03/5g-e-esperanca-ambiental-de-quem-vende-internet.shtml',
    'https://www1.folha.uol.com.br/tec/2023/03/gpt-evolui-muito-problemas-permanecem-e-perigos-aumentam.shtml',
    'https://www1.folha.uol.com.br/tec/2023/03/metaverso-e-mercado-trilionario-mas-nao-se-sabe-qual-cara-tera.shtml',
    'https://www1.folha.uol.com.br/tec/2023/02/o-que-voce-precisa-saber-sobre-chatgpt-openai-e-inteligencia-artificial-na-linguagem.shtml',
    'https://www1.folha.uol.com.br/tec/2023/01/cibercriminosos-do-brasil-buscam-protagonismo-em-fraudes-bancarias.shtml',
    'https://www1.folha.uol.com.br/esporte/2022/11/campeonato-mundial-de-excel-programa-de-tabelas-vira-esporte-com-transmissao-na-tv.shtml',
    'https://www1.folha.uol.com.br/poder/2022/10/eleicao-chega-ao-2o-turno-com-expectativa-de-reducao-nas-filas-de-votacao.shtml',
    'https://www1.folha.uol.com.br/poder/2022/09/lula-e-bolsonaro-focam-economia-e-ignoram-corrupcao-no-youtube.shtml',
    'https://www1.folha.uol.com.br/tec/2022/04/grupo-hacker-lapsus-exporta-malandragem-brasileira.shtml',
    'https://www1.folha.uol.com.br/tec/2021/11/facebook-e-parte-do-problema-mas-ha-manipulacao-em-outras-empresas-diz-especialista.shtml',
    'https://www1.folha.uol.com.br/tec/2021/02/hackers-miram-empresas-de-vacinas-e-saude-na-pandemia.shtml',
    'https://www1.folha.uol.com.br/poder/2021/02/custo-de-voto-em-mulheres-chega-a-ser-quase-70-vezes-mais-caro-que-em-homens.shtml',
    'https://www1.folha.uol.com.br/poder/2020/11/grupo-hacker-que-atacou-o-tse-e-conhecido-por-iniciativas-semelhantes.shtml',
    'https://www1.folha.uol.com.br/tec/2017/12/1945132-leitura-de-termos-e-condicoes-de-servicos-na-internet-exige-45-horas.shtml',
    'https://www1.folha.uol.com.br/tec/2017/12/1945134-brasil-deve-ter-lei-de-protecao-de-dados-so-no-fim-de-2018-dizem-especialistas.shtml',
    'https://www1.folha.uol.com.br/tec/2022/03/internet-capenga-nao-aguentara-o-metaverso.shtml',
    'https://www1.folha.uol.com.br/educacao/2022/05/cotista-tem-nota-de-corte-maior-que-nao-cotista-em-25-dos-cursos-do-sisu.shtml',
    'https://www1.folha.uol.com.br/tec/2022/04/grupos-de-cibercrime-se-profissionalizam-e-lucro-dispara.shtml',
    'https://www1.folha.uol.com.br/poder/2018/09/em-meio-a-debate-sobre-seguranca-tse-planeja-colocar-codigo-da-urna-na-internet.shtml',
    'https://www1.folha.uol.com.br/poder/2018/02/fake-news-ganha-espaco-no-facebook-e-jornalismo-profissional-perde.shtml',
    'https://www1.folha.uol.com.br/tec/2017/10/1928985-rastro-deixado-na-internet-inclui-de-nome-da-mae-a-preferencias-amorosas.shtml'
]

# Function to extract information from a URL
def extract_info(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request was not successful

    # Create a BeautifulSoup object with the response text
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the required information
    title_pt = soup.find("h1", class_="c-content-head__title").get_text().strip() if soup.find("h1", class_="c-content-head__title") else ""
    #title_en = soup.find("h1", class_="c-content-head__subtitle").get_text() if soup.find("h1", class_="c-content-head__subtitle") else ""
    publish_date_element = soup.find("time", class_="c-more-options__published-date")
    publish_date = publish_date_element.get("datetime").strip() if publish_date_element else ""
    section_element = soup.find("li", class_="c-site-nav__item--section")
    section = section_element.find("a").get_text().strip() if section_element else ""
    section = f"Folha de S.Paulo - {section.capitalize()}" if section else ""
    article_url = url
    og_image_element = soup.find("meta", property="og:image")
    og_image_url = og_image_element.get("content").strip() if og_image_element else ""



    # Return the extracted information as a dictionary
    return {
        "Photo" : og_image_url,
        "Article title in Portuguese": title_pt,
        "Date": publish_date,
        "Where it was published": section,
        "Article URL": article_url,
    }

# Extract information from each URL and store the results in a list of dictionaries
results = []
for url in urls:
    info = extract_info(url)
    results.append(info)

# Export the results to a CSV file
filename = "scraped_articles.csv"
encoding = "iso-8859-1"

with open(filename, "w", encoding=encoding, newline="") as csvfile:
    fieldnames = ["Photo",
        "Article title in Portuguese",
        "Date",
        "Where it was published",
        "Article URL"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)

print(f"Data exported to '{filename}' successfully.")