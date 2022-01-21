import pandas as pd
import plotly.graph_objects as go

tabela = pd.read_csv(r'C:\Users\jcazarotto\Desktop\projeto-covid-br\cases-brazil-states.csv')
total = tabela['state'] == "TOTAL"
tabela = tabela[total]
tabela['date'] = pd.to_datetime(tabela['date'])
tabela['mes'] = tabela['date'].dt.strftime('%m-%Y')
print(tabela.info())
cases = go.Scatter(x=tabela['date'],
                   y=tabela['newCases'],
                   mode='lines',
                   name='Cases',
                   line=dict(width=1.5))
deaths = go.Scatter(x=tabela['date'],
                    y=tabela['newDeaths'],
                    name='Deaths',
                    mode='lines',
                    line=dict(width=1.5))
frames = [dict(data= [dict(type='scatter',
                           x=tabela['date'][:k+1],
                           y=tabela['newCases'][:k+1]),
                      dict(type='scatter',
                           x=tabela['date'][:k+1],
                           y=tabela['newDeaths'][:k+1]),
                     ],
               traces= [0, 1],
              )for k  in  range(1, len(tabela)-1)]
layout = go.Layout(# width=700,
                   # height=600,
                   showlegend=True,
                   # hovermode='x unified',
                   updatemenus=[
                        dict(
                            type='buttons',
                            showactive=False,
                            y=1.05,
                            x=1.15,
                            xanchor='right',
                            yanchor='top',
                            pad=dict(t=0, r=10),
                            buttons=[dict(label='Play',
                            method='animate',
                            args=[None, 
                                  dict(frame=dict(duration=3, 
                                                  redraw=False),
                                                  transition=dict(duration=0),
                                                  fromcurrent=True,
                                                  mode='immediate')]
                            )]
                        ),
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                dict(
                                    args=[{"yaxis.type": "linear"}],
                                    label="LINEAR",
                                    method="relayout"
                                ),
                                dict(
                                    args=[{"yaxis.type": "log"}],
                                    label="LOG",
                                    method="relayout"
                                )
                            ]),
                        ),
                    ]              
                  )
fig = go.Figure(data=[cases, deaths], frames=frames, layout=layout)
fig.show()
