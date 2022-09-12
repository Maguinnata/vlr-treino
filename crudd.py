import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

stats_individual_média = pd.read_excel('Stats.xlsx')
stats_individual_média_f = stats_individual_média.drop(columns=['Data','Semana', 'Agentes','Mapas',])
stats_individual_média_fd = stats_individual_média_f.to_dict('records')

st.markdown("<h1 style='text-align: center; color: white;'>Dashboard Treino</h1>", unsafe_allow_html=True) # se der merda volta pro st.tittle e fé
st.sidebar.title('Menu')

páginas = st.sidebar.selectbox('Selecione a página',['Stats Individual Média','Stats Individual Round', 'Stats Time'])

col1 = stats_individual_média_f.columns.tolist()
select1= st.sidebar.selectbox('Selecione a métrica', col1)

if páginas == 'Stats Individual Média':
    st.subheader('Stats Individual Média')
    stats_individual_média_player = stats_individual_média.groupby(['Players']).mean()
    st.table(stats_individual_média_player.reset_index().round(2))

    x1 = stats_individual_média_f['Players']
    y1 = stats_individual_média_f[select1].mean()
    plt.bar(x1,y1,data= stats_individual_média_f[select1] ,width= 0.4, align= 'center')
    st.pyplot(plt)

    #graph1 = stats_individual_média[select1].mean().plot(kind = 'barh')
    #st.pyplot(graph1.figure)

if páginas == 'Stats Individual Round':
    st.title('Bem vindo a Página 2')
    marital_true = bf.Age.loc[bf.Marital_Status == 1].value_counts()
    marital_false = bf.Age.loc[bf.Marital_Status == 0].value_counts()

    #x1 = marital_true.index
    #y1 = marital_true.values

    x2 = marital_false.index
    y2 = marital_false.values

    #plt.bar(x1,y1, label = 'Casados', width= 0.4, align= 'edge')
    plt.bar(x2, y2, label='Não-Casados', width= -0.4, align='edge',text_auto = True)
    plt.legend()
    plt.title('Casados e não casados por idade')
    st.pyplot(plt)

    plt.clf() #caso precise por dois gráficos no msm lugar isso auqi faz limpar