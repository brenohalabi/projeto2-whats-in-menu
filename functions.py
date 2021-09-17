from plotly import graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st  # versão 0.87
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import cufflinks as cf
import plotly.express as px

# o DF com os joins já feito(ta no notebook)
df_final = pd.read_csv('./df_final.csv')


# filtro do DF da animação
@st.cache
def animation_df():
    top_10_menu = df_final[['name', 'menus_appeared', 'price']].sort_values(by='menus_appeared', ascending=False).drop_duplicates(subset=['name'])[0:10]
    df_cp = df_final[['price', 'name', 'year']]
    df_cp['times_appeared_by_year'] = 1
    df_cp = df_cp[df_cp.name.isin(top_10_menu.name)]

    itere = df_cp.groupby('year')
    final_df = pd.DataFrame(columns=df_cp.columns)

    for i in itere:
        if top_10_menu.name.isin(i[1].name).all() != True:
            not_in = top_10_menu[~top_10_menu.name.isin(i[1].name)].drop(columns='menus_appeared').copy()
            year = i[1].year.values[0]
            not_in['price'] = 0
            not_in['times_appeared_by_year'] = 0
            not_in['year'] = year
            final_df = final_df.append(not_in[df_cp.columns])

    final_df = final_df.append(df_cp)
    final_df = final_df.append(df_cp)
    final_df = final_df[(final_df['year'] >= 1900) & (final_df['year'] <= 2000)].reset_index()

    groupped = pd.DataFrame()
    for i in final_df.groupby(['year', 'name']):
        media = i[1].price.mean()
        soma =  i[1].times_appeared_by_year.sum()
        nome = i[1].name.values[0]
        year = i[1].year.values[0]
        data = dict(year=[year],name=[nome],times_appeared_by_year=[soma],media=[media])
        new_df = pd.DataFrame(data=data)
        groupped = groupped.append(new_df)
    groupped = groupped.sort_values(by=['year'])
    groupped['cumulative_appearing'] = groupped.groupby(['name']).times_appeared_by_year.cumsum()

    return groupped

# filtro dos sponsors
@st.cache
def top_sponsors():
    columns = ['id','sponsor']
    df_menu_filtered = df_final[columns]
    return df_menu_filtered.sponsor.value_counts().head(15)

# filtro variação de preço
@st.cache
def top_variacao():
    df_dish_sorted_price_var = df_final.sort_values(by=['price_var'], ascending=False)
    return df_dish_sorted_price_var.drop_duplicates(subset=['name'])[0:15]

# filtro de aparições(tanto totais quanto apenas menu)
@st.cache
def top_aparicao(modo):
    df_dish_menu_sorted = df_final.sort_values(by=modo, ascending=False)
    return df_dish_menu_sorted.drop_duplicates(subset=['name'])[0:15]

# gráfico dos sponsors
@st.cache
def top_sponsors_graph(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.index, y=df,marker_color='rgb(55, 83, 109)'))
    fig.layout.update(title_text='Top 15 Sponsors', xaxis_rangeslider_visible=False, autosize=True)
    fig.layout.update(
        xaxis=dict(
                showticklabels=True,
                ticks='outside',
                tickfont=dict(
                    family='Roboto',
                    size=12,
                    color='rgb(235,235,235)'),
            ),
        yaxis=dict(
                showgrid=False,
                zeroline=True,
                showticklabels=True,
                ticks='outside',
            ),
    )
    return fig

# gáfico da variação de preço
@st.cache
def top_variacao_graph(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.name, y=df.price_var,marker_color='rgb(55, 83, 109)'))
    fig.layout.update(title_text='Top 15 Variações de Preço', xaxis_rangeslider_visible=False, autosize=True)
    fig.layout.update(
        xaxis=dict(
                showticklabels=True,
                ticks='outside',
                tickfont=dict(
                    family='Roboto',
                    size=12,
                    color='rgb(235,235,235)'),
            ),
        yaxis=dict(
                showgrid=False,
                zeroline=True,
                showticklabels=True,
                ticks='outside',
            ),
    )
    return fig

# gráfico das aparições(menu)
@st.cache
def top_aparicao_graph_menu(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.name, y=df.menus_appeared,marker_color='rgb(55, 83, 109)'))
    fig.layout.update(title_text='Top 15 Aparições em Menus', xaxis_rangeslider_visible=False, autosize=True)
    fig.layout.update(
        xaxis=dict(
                showticklabels=True,
                ticks='outside',
                tickfont=dict(
                    family='Roboto',
                    size=12,
                    color='rgb(235,235,235)'),
            ),
        yaxis=dict(
                showgrid=False,
                zeroline=True,
                showticklabels=True,
                ticks='outside',
            ),
    )
    return fig

# gráfico das aparições(total)
@st.cache
def top_aparicao_graph_total(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.name, y=df.times_appeared,marker_color='rgb(55, 83, 109)'))
    fig.layout.update(title_text='Top 15 Aparições Totais', xaxis_rangeslider_visible=False, autosize=True)
    fig.layout.update(
        xaxis=dict(
                showticklabels=True,
                ticks='outside',
                tickfont=dict(
                    family='Roboto',
                    size=12,
                    color='rgb(235,235,235)'),
            ),
        yaxis=dict(
                showgrid=False,
                zeroline=True,
                showticklabels=True,
                ticks='outside',
            ),
    )
    return fig

# animação
@st.cache
def animation_graph(df, modo):
    if modo[0] == 'times_appeared_by_year':
        range_y=[0,600]
    else:
        range_y=[0,7000]
    fig = px.scatter(df, 
        x='media', 
        y=modo[0],           
        color='name',
        size=modo[1],
        size_max=55,
        animation_frame='year',
        range_y=range_y,
        log_x=True,
        labels={
        'media': 'Preço',
        'times_appeared_by_year': 'Aparições por Ano',
        'cumulative_appearing': 'Aparições Acumuladas'
        },
        range_x=[0.1, 300])
    fig.layout.update(title_text='Preço x Aparições por Ano x Aparições Acumuladas', xaxis_rangeslider_visible=False,autosize=True)
    fig.layout.update(
    xaxis=dict(
        showgrid=False,
        showticklabels=True,
        ticks='outside',
        tickfont=dict(
            family='Roboto',
            size=12,
            color='rgb(235,235,235)'),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=True,
        showticklabels=True,
        ticks='outside',
    ),
    )
    return fig
