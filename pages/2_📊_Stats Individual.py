import streamlit as st
import pandas as pd
import plotly.express as px

########### BASE DE DADOS ###########

stats = pd.read_excel('Stats.xlsx')
stats_f = stats.drop(columns=['Data','Semana','Agentes','Mapas','W-Round','L-Round','W-TR','L-TR','W-CT','L-CT','Pickrate']).round(2)

stats_r = pd.read_excel('Stats por Round.xlsx')

########### CONVERSÕES ###########

stats['Data'] = stats['Data'].dt.strftime('%d/%m/%Y')
rounds = 1128

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
st.title('📊 Stats Individual')
st.markdown('---')

########## SIDEBAR ##########

st.sidebar.header('Filtros')

var1 = st.sidebar.multiselect(
    'Selecione uma Variável (Média)',
    options= stats_f.columns.unique(),
    #default= 'ACS',
)

stats_var_1 = stats_f.query(
    'ACS == @var1'
)

box1 = st.sidebar.selectbox(
    'Selecione uma Variável (Quartil)',
    options= stats_f.columns.unique(),
)

stats_box_1 = stats_f.query(
    'ACS == @box1'
)

var2 = st.sidebar.multiselect(
    'Selecione uma Variável (p/Round)',
    options= stats_r_geral.columns.unique(),
    #default=(),
)

stats_var_2 = stats_r_geral.query(
    'KD == @var2 & KpR == @var2'
)

########### KPI's ###########
stats_individual = stats_f.groupby(['Players']).mean().reset_index().round(2)

tab1, tab2, tab3 = st.tabs(['▶️ Média','▶️ p/ Round','▶️ KpR x ACS'])

##########STATS INDIVIDUAIS MÉDIA E GRÁFICO##########

with tab1:
    st.dataframe(stats_individual.style.format(precision=2))

    g_stats_indiv = px.bar(
    stats_individual.round(2),
    x= 'Players',
    y= var1,
    barmode= 'group',
    text_auto= True,
    color_discrete_sequence= ['#0d0887','orangered','lightslategray'],
    width= 800,
    height= 500,
    title= '<b> Média </b>'
    )

    g_stats_indiv.update_layout(
    plot_bgcolor= 'rgba(0,0,0,0)',
    xaxis = (dict(showgrid= False))
    )
    g_stats_indiv.update_layout(font=dict(size=15))

    st.plotly_chart(g_stats_indiv)

    g_stats_indiv2 = px.box(
        stats_f.round(2),
        x= 'Players',
        y= box1,
        points= 'suspectedoutliers',
        width= 800,
        height= 500,
        title= '<b> Quartil </b>'
    )

    g_stats_indiv2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
    )
    g_stats_indiv2.update_layout(font=dict(size=15))

    st.plotly_chart(g_stats_indiv2)

##########STATS INDIVIDUAIS p/ROUND E GRÁFICO##########

with tab2:
    g_stats_indiv_r = px.bar(
        stats_r_geral.round(2),
        x='Players',
        y=var2,
        barmode='group',
        text_auto=True,
        #title= '<b> Stats p/ Round </b>',
        color_discrete_sequence=['#0d0887', 'orangered', 'lightslategray'],
        width=800,
        height=500,
        template='plotly_white'
    )
    g_stats_indiv_r.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
    )
    g_stats_indiv_r.update_layout(font=dict(size=15))
    st.plotly_chart(g_stats_indiv_r)

##########STATS INDIVIDUAIS KpR x ACS E GRÁFICO##########

with tab3:
    g_scatter_acs_kpr = px.scatter(stats_individual,
                                   x=stats_individual['ACS'],
                                   y=stats_r_geral['KpR'],
                                   text=stats_individual['Players'],
                                   color=stats_individual['Players'],
                                   size=stats_individual['ACS'],
                                   labels=dict(x='ACS', y='KpR'),
                                   width=730,
                                   height=430,
                                   hover_data=['ACS'],
                                   )
    g_scatter_acs_kpr.update_layout(font=dict(size=15))
    st.plotly_chart(g_scatter_acs_kpr)

    st.markdown('##')

    g_scatter_acs_fk= px.scatter(stats_individual,
                                 x= stats_individual['ACS'],
                                 y= stats_r_geral['ApR'],
                                 text=stats_individual['Players'],
                                 color=stats_individual['Players'],
                                 size=stats_individual['ACS'],
                                 labels=dict(x='ACS', y='ApR', size= 'ACS'),
                                 width=730,
                                 height=430,
                                 hover_data=['ACS'],
                                 )
    g_scatter_acs_fk.update_layout(font=dict(size=15))
    st.plotly_chart(g_scatter_acs_fk)
