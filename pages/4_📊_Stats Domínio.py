import streamlit as st
import pandas as pd
import plotly.express as px

########### BASE DE DADOS ###########

stats_dom = pd.read_excel('Stats Domínio.xlsx')

Ascent = 'https://i.imgur.com/qq3aVrB.png'
Bind = 'https://i.imgur.com/Fv5bpc7.png'
Breeze = 'https://i.imgur.com/jfzQMnw.png'
Fracture = 'https://i.imgur.com/224BMCP.png'
Haven = 'https://i.imgur.com/NpeYtOi.png'
Icebox = 'https://i.imgur.com/SMCmzBH.png'
#Pearl =

########### FILTROS ###########

filtro_ascent = stats_dom.drop(columns= ['Data','Semana','Bind','Breeze','Fracture','Haven','Icebox','Pearl'])
ascent_filtrado = filtro_ascent.groupby(['Ascent']).sum().reset_index()

filtro_bind = stats_dom.drop(columns= ['Data','Semana','Ascent','Breeze','Fracture','Haven','Icebox','Pearl'])
bind_filtrado = filtro_bind.groupby(['Bind']).sum().reset_index()

filtro_breeze = stats_dom.drop(columns= ['Data','Semana','Ascent','Bind','Fracture','Haven','Icebox','Pearl'])
breeze_filtrado = filtro_breeze.groupby(['Breeze']).sum().reset_index()

filtro_fracture = stats_dom.drop(columns= ['Data','Semana','Ascent','Bind','Breeze','Haven','Icebox','Pearl'])
fracture_filtrado = filtro_fracture.groupby(['Fracture']).sum().reset_index()

filtro_haven = stats_dom.drop(columns= ['Data','Semana','Ascent','Bind','Breeze','Fracture','Icebox','Pearl'])
haven_filtrado = filtro_haven.groupby(['Haven']).sum().reset_index()

filtro_icebox = stats_dom.drop(columns= ['Data','Semana','Ascent','Bind','Breeze','Fracture','Haven','Pearl'])
icebox_filtrado = filtro_icebox.groupby(['Icebox']).sum().reset_index()


########## CONFIG ##########
st.set_page_config(page_title='Treinos',
                   page_icon= ':bar_chart:',
                   #layout= 'wide',
                   )

st.title('📊 Stats Domínio')
st.markdown('---')

########## PÁGINA PRINCIPAL ##########

st.subheader('Ascent')
st.image(
    image=[Ascent],
    #height = '60px',
    width= 470
)
st.dataframe(ascent_filtrado.style.format(precision=2))

st.markdown('---')

st.subheader('Bind')
st.image(
    image= [Bind],
    width= 409
)
st.dataframe(bind_filtrado.style.format(precision=2))

st.markdown('---')

st.subheader('Breeze')
st.image(
    image= [Breeze],
    width= 400
)
st.dataframe(breeze_filtrado.style.format(precision=2))

st.markdown('---')

st.subheader('Fracture')
st.image(
    image=[Fracture],
    width= 336
)
st.dataframe(fracture_filtrado.style.format(precision=2))

st.markdown('---')

st.subheader('Haven')
st.image(
    image=[Haven],
    width=400
)
st.dataframe(haven_filtrado.style.format(precision=2))

st.markdown('---')

st.subheader('Icebox')
st.image(
    image=[Icebox],
    width=400
)
st.dataframe(icebox_filtrado.style.format(precision=2))

st.markdown('---')

st.subheader('Pearl')
#st.image(
 #   image=[Icebox],
  #  width=400
#)