import pandas as pd
from datetime import datetime


def create_highlights(df, lang):
    highlights = ""
    count = 0

    date_format = "%d/%m/%Y" if lang == 'Portuguese' else "%b/%d/%Y"

    # Add each article from dataframe to the HTML
    for _, row in df.iterrows():
        count += 1
        if (count % 2) == 0:
            orient = 'orient-left'
        else:
            orient = 'orient-right'

        date = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")


        highlights += """
        <section class="spotlight style1 {0} content-align-left image-position-center onscroll-image-fade-in">
            <div class="content">
                <h2><a href="{1}" target="_blank">{2}</a></h2>
                    <ul class="alt">
                        <li>{3}</li>
                        <li>{4}</li>
                        <li></li>
                        <p>{5}</p>
                    <ul class="actions stacked">
            </div>
            <div class="image">
                <a href="{1}" target="_blank"><img src="{6}" alt="" /></a>
            </div>
</section>""".format(orient,
                     row['Article URL'], 
                     row['Article title in {}'.format(lang)],
                     date.strftime(date_format),
                     row['Where it was published'],
                     row['Article Description in {}'.format(lang)],
                     row['Photo'])

    return highlights

def create_articles(df, lang):
    articles = ""
    date_format = "%d/%m/%Y" if lang == 'Portuguese' else "%b/%d/%Y"

    # Add each article from dataframe to the HTML
    for _, row in df.iterrows():
        # Parse the date
        date = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
        articles += """
        <section>
            <header>
                <h3><a href="{0}" target="_blank">{1}</a></h3>
                {2}
            </header>
            <div class="content">
                <p><a href="{0}" target="_blank">{3}</a></p>
                <p>{4}</p>
            </div>
        </section>""".format(row['Article URL'],
                             date.strftime(date_format),
                             row['Where it was published'],
                             row['Article title in {}'.format(lang)],
                             row['Article Description in {}'.format(lang)])

    return articles

# Read csv file into a dataframe
df = pd.read_csv('articles.csv')
df.sort_values(by='Date', ascending=False, inplace=True)

df_highlights = df[df['Highlight'] == True].reset_index(drop=True)
df_articles = df[df['Highlight'] == False].reset_index(drop=True)


# Load the template
with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Descriptions in both languages
title_pt = 'Pesquisador em Ética de Inteligência Artificial; Jornalista de tecnologia, dados e IA'
title_en = 'Artificial Intelligence Ethics Researcher; Tech, data and AI journalist'

description_pt = 'Pesquisador em Ética de IA e Jornalista'
description_en = 'AI Ethics Researcher, Journalist'

with open('about_pt.html', 'r', encoding='utf-8') as f:
    about_pt = f.read()
with open('about_en.html', 'r', encoding='utf-8') as f:
    about_en = f.read()

language_selector_pt = 'Português / <a href="./index.html">English</a>'
language_selector_en = '<a href="./pt.html">Português</a> / English'

# Generate webpages in both languages
with open('pt.html', 'w', encoding='utf-8') as f:
    highlights = create_highlights(df_highlights, 'Portuguese')
    articles = create_articles(df_articles, 'Portuguese')
    f.write(template.format(lang='pt', 
                            title=title_pt,
                            description=description_pt,
                            language_selector=language_selector_pt,
                            about=about_pt,
                            work='Trabalhos selecionados',
                            more_work='Mais trabalhos selecionados',
                            highlights=highlights,
                            articles=articles))

# Generate webpages in both languages
with open('index.html', 'w', encoding='utf-8') as f:
    highlights = create_highlights(df_highlights, 'English')
    articles = create_articles(df_articles, 'English')
    f.write(template.format(lang='en', 
                            title=title_en,
                            description=description_en,
                            language_selector=language_selector_en,
                            about=about_en,
                            work='Selected work',
                            more_work='More selected work',
                            highlights=highlights,
                            articles=articles))