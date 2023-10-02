# ./venv/Scripts/Activate
# streamlit run piloto1.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')


def formata_numero(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'


st.title('Piloto de Streamlit 🛒')

url = 'https://labdados.com/produtos'
response = requests.get(url).json()
dados = pd.DataFrame(response)
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

# Tabelas
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_estados = dados.drop_duplicates(subset=['Local da compra'])[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mês'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False).reset_index()

# Gráficos
fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat='lat',
                                  lon='lon',
                                  scope='south america',
                                  size='Preço',
                                  template='seaborn',
                                  hover_name='Local da compra',
                                  hover_data={'lat': False, 'lon': False},
                                  title='Receita por Estado'
                                  )

fig_receita_mensal = px.line(receita_mensal,
                             x='Mês',
                             y='Preço',
                             markers=True,
                             range_y=[0, receita_mensal.max()],
                             color='Ano',
                             line_dash='Ano',
                             title='Receita Mensal'
                             )

fig_mapa_receita.update_layout(yaxis_title='Receita')

fig_receita_estados = px.bar(receita_estados.head(),
                             x='Local da compra',
                             y='Preço',
                             text_auto=True,
                             title='Top estados (receita)'
                             )

fig_receita_estados.update_layout(yaxis_title='Receita')

receita_categorias['Preço'] = pd.to_numeric(receita_categorias['Preço'])
fig_receita_categorias = px.bar(receita_categorias,
                                x='Categoria do Produto',
                                y='Preço',
                                text_auto=True,
                                title='Receita por categoria'
                                )

fig_receita_categorias.update_layout(yaxis_title='Receita')

# Visualização no streamlit
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric("Receita", formata_numero(dados['Preço'].sum(), "R$"))
    st.plotly_chart(fig_mapa_receita, use_container_width=True)
    st.plotly_chart(fig_receita_estados, use_container_width=True)

with coluna2:
    st.metric("Quantidade de Vendas", formata_numero(dados.shape[0]))
    st.plotly_chart(fig_receita_mensal, use_container_width=True)
    st.plotly_chart(fig_receita_categorias, use_container_width=True)

st.dataframe(dados)
