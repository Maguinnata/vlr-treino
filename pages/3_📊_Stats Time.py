import streamlit as st
import pandas as pd
import plotly.express as px

########### BASE DE DADOS ###########

stats_ct = pd.read_excel('Stats Time CT.xlsx')
stats_tr = pd.read_excel('Stats Time TR.xlsx')
stats_eco = pd.read_excel('Stats ECO.xlsx')
stats_eco_opp = pd.read_excel('Stats ECO OPP.xlsx')
stats_opening = pd.read_excel('Stats Opening.xlsx')

filtro1 = ['Data','Semana']

stats_f1 = stats_ct.drop(columns= filtro1).round(2)
stats_ct_f = stats_f1.groupby(['Bomb','Mapas']).sum().round(2).reset_index()

stats_f2 = stats_tr.drop(columns= filtro1).round(2)
stats_tr_f = stats_f2.groupby(['Bomb','Mapas']).sum().round(2).reset_index()

########## CONFIG ##########

st.set_page_config(page_title='Treinos',
                   page_icon= ':bar_chart:',
                   #layout= 'wide',
                   )
st.title('📊 Stats Time')
st.markdown('---')

########### SIDEBAR CT ###########

st.sidebar.header('Filtros')

mapa = st.sidebar.multiselect(
    'Selecione um Mapa para o lado CT',
    options= stats_ct_f['Mapas'].unique(),
    default= 'Ascent'
)
sb_ct = stats_ct_f.query(
    'Mapas == @mapa'
).style.format(precision=2)

########## CT ##########

st.subheader('Stats CT')
st.dataframe(sb_ct)

g_pistol_ct = px.histogram(
    stats_ct,
    x= ['Pistol, 2º e 3º Round (CT) W','Pistol, 2º e 3º Round (CT) L'],
    barmode= 'group',
    text_auto= True,
    color_discrete_sequence= ['seagreen','indianred'],
    width= 800,
    height= 500,
    template= 'plotly_white'
)
st.plotly_chart(g_pistol_ct)

st.markdown('##')

########### SIDEBAR TR ###########

st.sidebar.header('Filtros')

mapa = st.sidebar.multiselect(
    'Selecione um Mapa para o lado TR',
    options= stats_tr_f['Mapas'].unique(),
    default= 'Ascent'
)
sb_tr = stats_tr_f.query(
    'Mapas == @mapa'
).style.format(precision=2)

########## TR ##########

st.subheader('Stats TR')
st.dataframe(sb_tr)

g_pistol_tr = px.histogram(
    stats_tr,
    x= ['Pistol, 2º e 3º Round (TR) W','Pistol, 2º e 3º Round (TR) L'],
    barmode= 'group',
    text_auto= True,
    color_discrete_sequence= ['seagreen','indianred'],
    width= 800,
    height= 500,
    template= 'plotly_white'
)
st.plotly_chart(g_pistol_tr)

st.markdown('----')

########## ECO ##########

st.subheader('Stats ECO e ECO OPP')

stats_eco_f = stats_eco.groupby(['Time']).sum().round(2).reset_index()
st.dataframe(stats_eco_f.style.format(precision=2))

########## ECO OPP ##########

stats_eco_opp_f = stats_eco_opp.groupby(['Time']).sum().round(2).reset_index()
st.dataframe(stats_eco_opp_f.style.format(precision=2))

st.markdown('----')

########## GRÁFICO 5V4 X 4V5 ##########
stats_opening_f1 = stats_opening.drop(columns=['Monitorar','OpD - W','OpD - L','Mapas','Data'])

stats_opening_killw = stats_opening_f1.groupby(['Time']).sum().reset_index()
stats_opening_killw['Topk'] = (stats_opening_killw['OpK - W'] + stats_opening_killw['OpK - L'])
stats_opening_killw['5v4 Round Win %'] = ((stats_opening_killw['OpK - W'] / stats_opening_killw['Topk'])*100).round(2)


stats_opening_f2 = stats_opening.drop(columns=['Monitorar','OpK - W','OpK - L','Mapas','Data'])
stats_opening_deathw = stats_opening_f2.groupby(['Time']).sum().reset_index()
stats_opening_deathw['Topd'] = (stats_opening_deathw['OpD - W'] + stats_opening_deathw['OpD - L'])
stats_opening_deathw['4v5 Round Win %'] = ((stats_opening_deathw['OpD - W'] / stats_opening_deathw['Topd'])*100).round(2)


g_opening = px.scatter(stats_opening_deathw,
                       x= stats_opening_deathw['4v5 Round Win %'],
                       y= stats_opening_killw['5v4 Round Win %'],
                       text= stats_opening['Time'].unique(),
                       size= stats_opening_deathw['4v5 Round Win %'],
                       width= 700,
                       height= 400,
                       hover_data= ['4v5 Round Win %'],
                       labels= dict(x= '4v5 Round Win %', y= '5v4 Round Win %'),
                       )
st.markdown('##')
st.subheader('Stats Time - 5v4 X 4v5')
st.plotly_chart(g_opening)