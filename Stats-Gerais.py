import streamlit as st
import pandas as pd
import plotly.express as px

########### BASE DE DADOS ###########

stats = pd.read_excel('Stats.xlsx')
filtro1 = ['Data','Semana','Agentes','Mapas','W-Round','L-Round','W-TR','L-TR','W-CT','L-CT','Pickrate']
filtro2 = ['W-Round','L-Round','W-TR','L-TR','W-CT','L-CT','Pickrate']
filtro3 = ['Data','Semana','Agentes','W-Round','L-Round','W-TR','L-TR','W-CT','L-CT','Players']
filtro4 = ['Data','Semana','Agentes','Mapas','L-Round','W-TR','L-TR','W-CT','L-CT','Pickrate']

stats_f1 = stats.drop(columns= filtro1).round(2)
stats_f2 = stats.drop(columns= filtro2).round(2)
stats_f3 = stats.drop(columns= filtro3).round(2)
stats_f4 = stats.drop(columns= filtro4).round(2)

########### CONFIG ###########

st.set_page_config(page_title='Treinos',
                   page_icon= ':bar_chart:',
                   layout= 'wide',
                   )

########### SIDEBAR ###########

st.sidebar.header('Filtros')

mapa = st.sidebar.multiselect(
    'Selecione um Mapa',
    options= stats_f2['Mapas'].unique(),
    default= stats_f2['Mapas'].unique(),

)
stats_mapa = stats_f2.query(
    'Mapas == @mapa'
)

########### CONVERSÕES ###########

stats_mapa['Data'] = stats_mapa['Data'].dt.strftime('%d/%m/%Y')

########### KPI's ###########

st.header('📊 Stats Gerais')
st.markdown('-Referente ao Mês de Agosto-')
st.markdown('----')

w_round = len(stats_f4[stats_f4['W-Round'] > 12])
l_round = len(stats_f4[stats_f4['W-Round'] < 12])
d_round = len(stats_f4[stats_f4['W-Round'] == 12])


total_round = l_round + d_round + w_round

first_colum, second_colum, third_colum, fourth_colum = st.columns(4)

with first_colum:
    st.subheader('Wins')
    st.subheader(f'{w_round}')

with second_colum:
    st.subheader('Loses')
    st.subheader(f'{l_round}')

with third_colum:
    st.subheader('Draws')
    st.subheader(f'{d_round}')

with fourth_colum:
    st.subheader('Total')
    st.subheader(f'{total_round}')

st.markdown('----')

########### GRÁFICO DE PIZZA ###########

g_mapas = px.pie(stats_f3,
                 values= 'Pickrate',
                 names= 'Mapas',
                 width= 900,
                 height= 470,
                 color_discrete_sequence= ['#6959CD','#FFA07A','#F5DEB3','#87CEEB','#DCDCDC','#6B8E23','#4169E1','#00BFFF'],
                 hover_data=['Mapas'],
                 labels= {'Mapas':'Nome'}
)
g_mapas.update_traces(textposition='inside', textinfo='percent+label')
g_mapas.update_layout(font= dict(size= 18), legend= dict(font=dict(size= 15)))
st.plotly_chart(g_mapas)

########### TABELA ###########

st.markdown('----')
st.table(stats_mapa.style.format(precision=1))

########### CUSTOM CSS ###########

hide_st_style = """
<style>
MainMenu {visibility: show;}
footer {visibility: show;}
header {visibility: show;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


