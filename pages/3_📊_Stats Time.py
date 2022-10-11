import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

########### BASE DE DADOS ###########

stats = pd.read_excel('Stats.xlsx')
stats_ct = pd.read_excel('Stats Time CT.xlsx')
stats_tr = pd.read_excel('Stats Time TR.xlsx')
stats_eco = pd.read_excel('Stats ECO.xlsx')
stats_eco_opp = pd.read_excel('Stats ECO OPP.xlsx')
stats_opening = pd.read_excel('Stats Opening.xlsx')

########### CONVERSÕES ###########

def color(s):
    return np.where(s == "Retake Total (W)", "background-color: green;", "")



filtro1 = ['Data','Semana']
stats_f1 = stats_ct.drop(columns= filtro1).round(2)
stats_ct_f = stats_f1.groupby(['Bomb','Mapas']).sum().round(2).reset_index()

stats_f2 = stats_tr.drop(columns= filtro1).round(2)
stats_tr_f = stats_f2.groupby(['Bomb','Mapas']).sum().round(2).reset_index()


filtro2 = ['Data','Semana','Agentes','W-Round','L-Round','Pickrate']
stats_f3 = stats.drop(columns=filtro2)
stats_f3_gb = stats_f3.groupby(['Mapas']).sum().round(2).reset_index() #

tr_wr = (stats_f3_gb['W-TR']/(stats_f3_gb['W-TR'] + stats_f3_gb['L-TR'])) * 100

ct_wr = (stats_f3_gb['W-CT']/(stats_f3_gb['W-CT'] + stats_f3_gb['L-CT'])) * 100

########## CONFIG ##########

st.set_page_config(page_title='Treinos',
                   page_icon= ':bar_chart:',
                   #layout= 'wide',
                   )
st.title('📊 Stats Time')
st.markdown('---')


tab1, tab2, tab3, tab4 = st.tabs(['▶️ CT','▶️ TR','▶️ ECO/ECO OPP','▶️ Round Win %'])

########### CT ###########

with tab1:
    st.sidebar.header('Filtros')

    mapa = st.sidebar.multiselect(
        'Selecione um Mapa para o lado CT',
        options=stats_ct_f['Mapas'].unique(),
        default='Ascent'
    )
    sb_ct = stats_ct_f.query(
        'Mapas == @mapa'
    ).style.format(precision=1)


    g_pistol_ct = px.histogram(
        stats_ct,
        x= ['Pistol, 2º e 3º Round (CT) W', 'Pistol, 2º e 3º Round (CT) L'],
        barmode= 'group',
        text_auto= True,
        color_discrete_sequence= ['seagreen', 'indianred'],
        width= 800,
        height= 500,
        labels=dict(x= 'Situação', y= 'Quantidade'),
    )
    g_pistol_ct.update_layout(font=dict(size=15))

    g_wr_ct = px.histogram(
        x= stats_f3_gb['Mapas'].unique(),
        y= ct_wr.round(2),
        barmode= 'group',
        text_auto= True,
        width= 800,
        height= 500,
        labels= dict(x= 'Mapas',y= '%')
    )
    g_wr_ct.update_traces(textposition='inside', text='percent+label',overwrite=True)
    g_wr_ct.update_layout(font=dict(size=17))

    st.subheader('Retake')
    st.dataframe(sb_ct)
    st.subheader('##')
    st.subheader('Win Rate p/ Mapa')
    st.plotly_chart(g_wr_ct)
    st.subheader('##')
    st.subheader('Rounds Pistol')
    st.plotly_chart(g_pistol_ct)

########### TR ###########

with tab2:
    st.sidebar.header('Filtros')

    mapa = st.sidebar.multiselect(
        'Selecione um Mapa para o lado TR',
        options=stats_tr_f['Mapas'].unique(),
        default='Ascent'
    )
    sb_tr = stats_tr_f.query(
        'Mapas == @mapa'
    ).style.format(precision=2)


    g_pistol_tr = px.histogram(
        stats_tr,
        x= ['Pistol, 2º e 3º Round (TR) W', 'Pistol, 2º e 3º Round (TR) L'],
        barmode= 'group',
        text_auto= True,
        color_discrete_sequence= ['seagreen', 'indianred'],
        width= 800,
        height= 500,

    )
    g_pistol_tr.update_layout(font=dict(size=15))

    g_wr_tr = px.histogram(
        x= stats_f3_gb['Mapas'].unique(),
        y= tr_wr.round(2),
        barmode= 'group',
        text_auto= True,
        width= 800,
        height= 500,
        labels=dict(x='Mapas', y='%')
    )
    g_wr_tr.update_layout(font=dict(size=17))

    st.subheader('Post Plant')
    st.dataframe(sb_tr)
    st.markdown('##')
    st.subheader('Win Rate p/ Mapa')
    st.plotly_chart(g_wr_tr)
    st.markdown('##')
    st.subheader('Rounds Pistol')
    st.plotly_chart(g_pistol_tr)


########## ECO/ECO OPP ##########

with tab3:
    #st.subheader('Stats ECO e ECO OPP')

    stats_eco_f = stats_eco.groupby(['Time']).sum().round(2).reset_index()
    st.dataframe(stats_eco_f.style.format(precision=2))

    st.markdown('----')

    stats_eco_opp_f = stats_eco_opp.groupby(['Time']).sum().round(2).reset_index()
    st.dataframe(stats_eco_opp_f.style.format(precision=2))

########## ROUND WIN % ##########

with tab4:
    stats_opening_f1 = stats_opening.drop(columns=['Monitorar', 'OpD - W', 'OpD - L', 'Mapas', 'Data'])

    stats_opening_killw = stats_opening_f1.groupby(['Time']).sum().reset_index()
    stats_opening_killw['Topk'] = (stats_opening_killw['OpK - W'] + stats_opening_killw['OpK - L'])
    stats_opening_killw['5v4 Round Win %'] = (
                (stats_opening_killw['OpK - W'] / stats_opening_killw['Topk']) * 100).round(2)

    stats_opening_f2 = stats_opening.drop(columns=['Monitorar', 'OpK - W', 'OpK - L', 'Mapas', 'Data'])
    stats_opening_deathw = stats_opening_f2.groupby(['Time']).sum().reset_index()
    stats_opening_deathw['Topd'] = (stats_opening_deathw['OpD - W'] + stats_opening_deathw['OpD - L'])
    stats_opening_deathw['4v5 Round Win %'] = (
                (stats_opening_deathw['OpD - W'] / stats_opening_deathw['Topd']) * 100).round(2)

    g_opening = px.scatter(stats_opening_deathw,
                           x=stats_opening_deathw['4v5 Round Win %'],
                           y=stats_opening_killw['5v4 Round Win %'],
                           text=stats_opening['Time'].unique(),
                           size=stats_opening_deathw['4v5 Round Win %'],
                           width=700,
                           height=400,
                           hover_data=['4v5 Round Win %'],
                           labels=dict(x='4v5 Round Win %', y='5v4 Round Win %'),
                           )
    g_opening.update_layout(font=dict(size=15))
    st.plotly_chart(g_opening)