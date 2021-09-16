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
    top_10_menu = df_final[['name', 'menus_appeared']].sort_values(by='menus_appeared', ascending=False).drop_duplicates(subset=['name'])[0:10]
    df_cp = df_final[['price', 'name', 'year']]
    df_cp['times_appeared_by_year'] = 1
    groupped = df_cp.groupby(['year', 'name']).sum().reset_index()
    group_sort = groupped.sort_values(by=['times_appeared_by_year'], ascending=False)
    df_inter = group_sort[group_sort.name.isin(top_10_menu.name)]
    df_sorted_year = df_inter.sort_values(by=['year'])
    return df_sorted_year[df_sorted_year['year'] >= 1900]

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
                    color='rgb(82,82,82)'),
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
                    color='rgb(82,82,82)'),
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
                    color='rgb(82,82,82)'),
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
                    color='rgb(82,82,82)'),
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
def animation_graph(df):
    fig = px.scatter(df, 
        x='price', 
        y='times_appeared_by_year',           
        color='name',
        size='times_appeared_by_year',
        size_max=55,
        animation_frame='year',
        range_y=[1, 400],
        labels={
        'price': 'Preço',
        'times_appeared_by_year': 'Aparições por Ano',
        },
        range_x=[0.1, 350])
    fig.layout.update(title_text='Preço x Aparições por Ano', xaxis_rangeslider_visible=False,autosize=True)
    fig.layout.update(
    xaxis=dict(
        showgrid=False,
        showticklabels=True,
        ticks='outside',
        tickfont=dict(
            family='Roboto',
            size=12,
            color='rgb(82,82,82)'),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=True,
        showticklabels=True,
        ticks='outside',
    ),
    )
    return fig