import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

tabela = pd.read_csv(r'C:\Users\jcazarotto\Desktop\projeto-covid-br\cases-brazil-states.csv')
total = tabela['state'] == "TOTAL"
tabela = tabela[total]
tabela['date'] = pd.to_datetime(tabela['date'])
tabela['mes'] = tabela['date'].dt.strftime('%m-%Y')
tabela['mes'] = pd.to_datetime(tabela['mes'])
tabela_resumo = tabela.groupby(by=['mes'], as_index=False, sort=True).sum()
tabela_vacinados = tabela.groupby(by=['mes'], as_index=False, sort=True).max()
tabela_resumo.reindex(tabela.columns, axis=1)
tabela_vacinados.reindex(tabela.columns, axis=1)
tabela_resumo['mes'] = tabela_resumo['mes'].dt.strftime('%m-%Y')
tabela_vacinados['mes'] = tabela_vacinados['mes'].dt.strftime('%m-%Y')
tabela_resumo = tabela_resumo[['mes','newCases', 'newDeaths']]
tabela_vacinados['vaccinated_single'] = tabela_vacinados['vaccinated_single'].fillna(0)
tabela_vacinados['vaccinated_total'] = tabela_vacinados['vaccinated'] + tabela_vacinados['vaccinated_single']
tabela_vacinados = tabela_vacinados[['mes','vaccinated_total','vaccinated', 'vaccinated_single',
                                     'vaccinated_second','vaccinated_third']]
tabela_tratada = tabela_resumo.merge(tabela_vacinados, on='mes')

pd.set_option('display.max_columns', None)
#print(tabela_tratada.info())
#print(tabela_tratada)


def plottar_grafico():

    fig = make_subplots(rows=3, cols=1, subplot_titles=('Cases', 'Deaths', 'Vaccinated'),
                        shared_xaxes=True)

    fig.add_trace(
        go.Scatter(x=tabela_tratada['mes'],
            y=tabela_tratada['newCases'],
            showlegend=False,
            text=tabela_tratada['newCases'],
            textposition='top center',
            textfont_size=12,
            texttemplate='%{text:.3s}',
            mode='lines+markers+text',
            name='Cases',
            line_shape='spline',
            line=dict(width=1.5)
            ),
        row=1,
        col=1
        )

    fig.add_trace(
        go.Scatter(x=tabela_tratada['mes'],
            y=tabela_tratada['newDeaths'],
            showlegend=False,
            text=tabela_tratada['newDeaths'],
            textposition='top center',
            textfont_size=12,
            texttemplate='%{text:.3s}',
            name='Deaths',
            mode='lines+markers+text',
            line_shape='spline',
            line=dict(width=1.5),
            ),
        row=2,
        col=1
        )

    fig.add_trace(
        go.Scatter(x=tabela_tratada['mes'],
            y=tabela_tratada['vaccinated_total'],
            showlegend=True,
            text=tabela_tratada['vaccinated_total'],
            textposition='top center',
            textfont_size=12,
            texttemplate='%{text:.3s}',
            mode='lines+markers+text',
            name='Vaccinated',
            line_shape='spline',
            line=dict(width=1.5)
            ),
        row=3,
        col=1
        )

    fig.add_trace(
        go.Scatter(x=tabela_tratada['mes'],
            y=tabela_tratada['vaccinated_second'],
            showlegend=True,
            text=tabela_tratada['vaccinated_second'],
            mode='lines+markers',
            name='Vaccinated Second Dose',
            line_shape='spline',
            line=dict(width=1.5)
            ),
        row=3,
        col=1
        )

    fig.add_trace(
        go.Scatter(x=tabela_tratada['mes'],
            y=tabela_tratada['vaccinated_third'],
            showlegend=True,
            text=tabela_tratada['vaccinated_third'],
            mode='lines+markers',
            name='Vaccinated Third Dose',
            line_shape='spline',
            line=dict(width=1.5)
            ),
        row=3,
        col=1
        )

    frames = [dict(name=i,
        data=[go.Scatter(
            x=tabela_tratada['mes'][:k+1],
            y=tabela_tratada['newCases'][:k+1]),
            go.Scatter(
            x=tabela_tratada['mes'][:k+1],
            y=tabela_tratada['newDeaths'][:k+1]),
            go.Scatter(
            x=tabela_tratada['mes'][:k+1],
            y=tabela_tratada['vaccinated_total'][:k+1]),
            go.Scatter(
            x = tabela_tratada['mes'][:k + 1],
            y = tabela_tratada['vaccinated_second'][:k + 1]),
            go.Scatter(
            x=tabela_tratada['mes'][:k + 1],
            y=tabela_tratada['vaccinated_third'][:k + 1])
            ],
        traces= [0, 1, 2, 3, 4],
        )
        for k, i in enumerate(tabela_tratada['mes'])]

    layout = go.Layout(
        showlegend=True,
        legend=dict(
            y=0.12
        ),
        title={'text': "Brazil's Covid-19 Evolution",
               'x': 0.5,
               'y': 1,
               'pad':dict(t=20),
               'font':dict(
                   size=30,
               )},
        updatemenus=[
            dict(
            type='buttons',
            xanchor='right',
            yanchor='top',
            buttons=[dict(label='Play',
            method='animate',
            args=[None,
                dict(frame=dict(duration=750,
                    redraw=True),
                    transition=dict(duration=0),
                    fromcurrent=True,
                    mode='immediate')]),
            dict(label='Pause',
                method='animate',
                args=[[None],
                    dict(frame=dict(duration=0, redraw=True),
                    transition=dict(duration=0),
                    mode='immediate')])
                ],
                direction='left',
                pad=dict(r=25, t=75),
                showactive=True,
                x=0.1,
                y=0
                )],
        sliders=[{'yanchor': 'top',
                'xanchor': 'left',
                'currentvalue': {'font': {'size': 14}, 'prefix': 'Período: ', 'visible': True, 'xanchor': 'right'},
                'transition': {'duration': 0, 'easing': 'linear'},
                'pad': {'b': 20, 't': 50},
                'len': 0.9, 'x': 0.1, 'y': 0,
                'steps': [{'args': [[i], {'frame': {'duration': 0, 'easing': 'linear', 'redraw': True},
                                          'transition': {'duration': 0, 'easing': 'linear'}}],
                           'label': i, 'method': 'animate'} for i in tabela_tratada['mes']
                          ]
                }]
    )

    for title in fig['layout']['annotations']:
        title['yshift']= 10
        title['font']['size']= 20

    fig.update_yaxes(range=[-100000,3750000], showticklabels=False, row=1, col=1)
    fig.update_yaxes(range=[-5000,100000], showticklabels=False, row=2, col=1)
    fig.update_yaxes(range=[-10000000,200000000], showticklabels=False, row=3, col=1)

    fig.update(frames=frames)
    fig.update(layout=layout)
    fig.show()


plottar_grafico()
