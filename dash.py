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
import functions as lp # o arquivo com as funções



top_sponsors = lp.top_sponsors() # pega o DF filtrado
graph_sponsors = lp.top_sponsors_graph(top_sponsors) # monta o gŕafico com DF filtrado
st.plotly_chart(graph_sponsors) # plota o gráfico na tela


top_variacao = lp.top_variacao() # pega o DF filtrado
graph_variacao = lp.top_variacao_graph(top_variacao) # monta o gŕafico com DF filtrado
st.plotly_chart(graph_variacao) # plota o gráfico na tela


appeared_box = st.selectbox(
    'Qual métrica deseja selecionar:',
    ('Menu', 'Total')  # Opções
) # box com seleção
if appeared_box == 'Menu':
    top_aparicao = lp.top_aparicao('menus_appeared')  # pega o DF filtrado
    graph_aparicao_menu = lp.top_aparicao_graph_menu(top_aparicao) # monta o gŕafico com DF filtrado
    st.plotly_chart(graph_aparicao_menu) # plota o gráfico na tela
else:
    top_aparicao = lp.top_aparicao('times_appeared') # pega o DF filtrado
    graph_aparicao_total = lp.top_aparicao_graph_total(top_aparicao) # monta o gŕafico com DF filtrado
    st.plotly_chart(graph_aparicao_total) # plota o gráfico na tela


animation_df = lp.animation_df() # pega o DF filtrado
animation_graph = lp.animation_graph(animation_df) # monta o gŕafico com DF filtrado
st.plotly_chart(animation_graph) # plota o gráfico na tela