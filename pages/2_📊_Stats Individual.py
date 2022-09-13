import streamlit as st
import pandas as pd
import plotly.express as px

########### BASE DE DADOS ###########

stats = pd.read_excel('Stats.xlsx')
stats_f = stats.drop(columns=['Data','Semana','Agentes','Mapas','W-Round','L-Round','W-TR','L-TR','W-CT','L-CT','Pickrate']).round(2)

stats_r = pd.read_excel('Stats por Round.xlsx')

########### CONVERSÕES ###########

stats['Data'] = stats['Data'].dt.strftime('%d/%m/%Y')
rounds = 518

########### KD e KpR ###########

stats_r_drop1 = stats_r.drop(columns=['Data','Semana','A','FK','FD','Rounds'])
stats_r_geral = stats_r_drop1.groupby(['Players']).sum().reset_index()
stats_r_geral['KD'] = (stats_r_geral['K'] / stats_r_geral['D']).round(2)
stats_r_geral['KpR'] = (stats_r_geral['K'] / rounds).round(2)

########### ApR ###########

stats_r_drop2= stats_r.drop(columns=['Data','Semana','K','FK','FD','D','Rounds'])
stats_r_apr = stats_r_drop2.groupby(['Players']).sum().reset_index()
stats_r_geral['ApR'] = (stats_r_apr['A'] / rounds).round(2)

########### FKpR & FDpR ###########

stats_r_drop3 = stats_r.drop(columns=['Data','Semana','K','D','A','Rounds'])
stats_r_fk = stats_r_drop3.groupby(['Players']).sum().reset_index()
stats_r_geral['FKpR'] = (stats_r_fk['FK']/rounds).round(2)
stats_r_geral['FDpR'] = (stats_r_fk['FD']/rounds).round(2)

########### FK/ratio e OPduels ###########
stats_r_geral['FKratio'] = (stats_r_fk['FK']/stats_r_fk['FD']).round(2)
stats_f['OpenDuels'] = (stats_f['FK']/(stats_f['FD']+stats_f['FK'])).round(2)

########### CONFIG ###########

st.set_page_config(page_title='Treinos',
                   page_icon= ':bar_chart:',
                   #layout= 'wide',
                   )
st.title('📊 Stats Individual - Média')
st.markdown('---')

########## SIDEBAR ##########

st.sidebar.header('Filtros')

var1 = st.sidebar.multiselect(
    'Selecione uma Variável (Gráfico 1)',
    options= stats_f.columns.unique(),
    #default= 'ACS',
)

stats_var_1 = stats_f.query(
    'ACS == @var1'
)

var2 = st.sidebar.multiselect(
    'Selecione uma Variável (Gráfico 2)',
    options= stats_r_geral.columns.unique(),
    #default=(),
)

stats_var_2 = stats_r_geral.query(
    'KD == @var2 & KpR == @var2'
)

########### KPI ###########

stats_individual = stats_f.groupby(['Players']).mean().reset_index().round(2)

st.markdown('##')
st.dataframe(stats_individual.style.format(precision=2))

########### GRÁFICO STATS INDIVIDUAS POR PLAYER ###########

g_stats_indiv = px.bar(
    stats_individual.round(2),
    x= 'Players',
    y= var1,
    barmode= 'group',
    text_auto= True,
    color_discrete_sequence= ['#0d0887','orangered','lightslategray'],
    width= 800,
    height= 500,
    template= 'plotly_white'
)
g_stats_indiv.update_layout(
    plot_bgcolor= 'rgba(0,0,0,0)',
    xaxis = (dict(showgrid= False))
)
st.plotly_chart(g_stats_indiv)
st.markdown('----')

########### GRÁFICO STATS INDIVIDUAS POR ROUND ###########

st.title('Stats Individual - p/ Round')
g_stats_indiv_r = px.bar(
    stats_r_geral.round(2),
    x= 'Players',
    y= var2,
    barmode= 'group',
    text_auto= True,
    #title= '<b> Stats per Player </b>',
    color_discrete_sequence= ['#0d0887','orangered','lightslategray'],
    width= 800,
    height= 500,
    template= 'plotly_white'
)
g_stats_indiv_r.update_layout(
    plot_bgcolor= 'rgba(0,0,0,0)',
    xaxis = (dict(showgrid= False))
)
st.plotly_chart(g_stats_indiv_r)
st.markdown('----')

########### GRÁFICO STATS KpR x ACS ###########

st.title('Stats Individual - KpR X ACS')
g_scatter = px.scatter(stats_individual,
    x= stats_individual['ACS'],
    y= stats_r_geral['KpR'],
    text= stats_individual['Players'],
    color= stats_individual['Players'],
    size= stats_individual['ACS'],
    labels= dict(x = 'ACS', y= 'KpR'),
    width= 730,
    height= 430,
    hover_data= ['ACS']
)

st.plotly_chart(g_scatter)