import plotly.express as px
import json
import pandas as pd

# pd.set_option('display.max_columns', None)

tabela = pd.read_csv(r'C:\Users\jcazarotto\Desktop\projeto-covid-br\cases-brazil-states.csv')
remove_total = tabela['state'] != 'TOTAL'
tabela = tabela[remove_total]
tabela['date'] = pd.to_datetime(tabela['date'])
tabela['mes'] = tabela['date'].dt.strftime('%m-%Y')
print(tabela.info())

mapa_brasil = json.load(open('C:/Users/jcazarotto/Desktop/projeto-covid-br/brasil_estados.json'))

'''fig_total = px.choropleth(tabela,
                          geojson=mapa_brasil,
                          locations="state",
                          color="totalCases",
                          animation_frame="mes",
                          hover_name="state",
                          color_continuous_scale='Reds',
                          labels={"state": 'Estado',
                                  "date": 'Data',
                                  "totalCases": 'Total de Casos'},
                          scope='south america'
                          )

fig_total.show()'''

fig_total_per_100k = px.choropleth(tabela,
                                   geojson=mapa_brasil,
                                   locations="state",
                                   color="totalCases_per_100k_inhabitants",
                                   animation_frame="mes",
                                   hover_name="state",
                                   color_continuous_scale='Reds',
                                   labels={"state": 'Estado',
                                           "date": 'Data',
                                           "totalCases_per_100k_inhabitants": 'Total de Casos por 100 mil Habitantes'},
                                   scope='south america'
                                   )
fig_total_per_100k.update_layout(
    title_text='Cases per 100k Inhabitants Evolution',
    title_font_family='Arial',
    title_font_size=30,
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=True,
    ))
fig_total_per_100k.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
fig_total_per_100k.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 20
fig_total_per_100k.update_geos(resolution=110)
fig_total_per_100k.show()
fig_total_per_100k.write_html("covid_map_cases_per_100k_brazil_evolution.html")
