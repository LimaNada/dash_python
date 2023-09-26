# ./venv/Scripts/Activate
# streamlit run piloto1.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px


def formata_numero(valor, prefixo=''):
    for unidade in ['','mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'


st.title('Piloto de Streamlit 🛒')

url = 'https://labdados.com/produtos'
response = requests.get(url).json()

dados = pd.DataFrame(response)

coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric("Receita", formata_numero(dados['Preço'].sum(), "R$"))

with coluna2:
    st.metric("Quantidade de Vendas", formata_numero(dados.shape[0]))

st.dataframe(dados)
