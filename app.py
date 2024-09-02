# from dash import Dash, html, dcc, callback, Output, Input
# import plotly.express as px
# import pandas as pd

# df = pd.read_csv('http://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# app = Dash()

# app.layout = [
#     html.H1(children='Title of Dash App', style={'textAlign':'center'}),
#     dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
#     dcc.Graph(id='graph-content')
# ]

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )

# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='8080')

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Função para gerar dados sintéticos baseados na F1
@st.cache_data
def gerar_dados_f1():
    # Dados dos pilotos
    np.random.seed(42)
    pilotos = ['Lewis Hamilton', 'Max Verstappen', 'Charles Leclerc', 'Sebastian Vettel', 'Fernando Alonso']
    temporadas = np.arange(2015, 2024)
    construtores = ['Mercedes', 'Red Bull', 'Ferrari', 'Aston Martin', 'McLaren']

    data_pilotos = {
        'Temporada': np.repeat(temporadas, len(pilotos)),
        'Piloto': pilotos * len(temporadas),
        'Construtor': np.random.choice(construtores, size=len(pilotos) * len(temporadas)),
        'Vitórias': np.random.randint(0, 10, size=len(pilotos) * len(temporadas)),
        'Pontos': np.random.randint(50, 400, size=len(pilotos) * len(temporadas)),
        'Pódios': np.random.randint(0, 15, size=len(pilotos) * len(temporadas))
    }
    df_pilotos = pd.DataFrame(data_pilotos)

    # Dados dos construtores
    data_construtores = df_pilotos.groupby(['Temporada', 'Construtor']).agg({
        'Vitórias': 'sum',
        'Pontos': 'sum',
        'Pódios': 'sum'
    }).reset_index()

    return df_pilotos, data_construtores

df_pilotos, df_construtores = gerar_dados_f1()

# Funções para cada página
def pagina_pilotos():
    st.title('Análise de Pilotos')

    # Filtro por piloto
    piloto_selecionado = st.selectbox('Selecione o Piloto', df_pilotos['Piloto'].unique())
    df_piloto_filtrado = df_pilotos[df_pilotos['Piloto'] == piloto_selecionado]

    # Gráfico de barras de vitórias por temporada
    fig_vitorias = px.bar(df_piloto_filtrado, x='Temporada', y='Vitórias', title=f'Vitórias por Temporada - {piloto_selecionado}')
    st.plotly_chart(fig_vitorias)

    # Gráfico de linha de pontos por temporada
    fig_pontos = px.line(df_piloto_filtrado, x='Temporada', y='Pontos', title=f'Pontos por Temporada - {piloto_selecionado}')
    st.plotly_chart(fig_pontos)

def pagina_construtores():
    st.title('Análise de Construtores')

    # Filtro por construtor
    construtor_selecionado = st.selectbox('Selecione o Construtor', df_construtores['Construtor'].unique())
    df_construtor_filtrado = df_construtores[df_construtores['Construtor'] == construtor_selecionado]

    # Gráfico de barras de vitórias por temporada
    fig_vitorias_construtor = px.bar(df_construtor_filtrado, x='Temporada', y='Vitórias', title=f'Vitórias por Temporada - {construtor_selecionado}')
    st.plotly_chart(fig_vitorias_construtor)

    # Gráfico de linha de pontos por temporada
    fig_pontos_construtor = px.line(df_construtor_filtrado, x='Temporada', y='Pontos', title=f'Pontos por Temporada - {construtor_selecionado}')
    st.plotly_chart(fig_pontos_construtor)

def pagina_comparacao():
    st.title('Comparação de Pilotos')

    # Filtro por pilotos
    pilotos_selecionados = st.multiselect('Selecione os Pilotos', df_pilotos['Piloto'].unique(), default=df_pilotos['Piloto'].unique()[:2])
    df_comparacao = df_pilotos[df_pilotos['Piloto'].isin(pilotos_selecionados)]

    # Gráfico de comparação de pontos entre pilotos
    fig_comparacao = px.line(df_comparacao, x='Temporada', y='Pontos', color='Piloto', title='Comparação de Pontos entre Pilotos')
    st.plotly_chart(fig_comparacao)

# Navegação entre as páginas
st.sidebar.title("Navegação")
pagina_selecionada = st.sidebar.radio("Ir para", ["Pilotos", "Construtores", "Comparação de Pilotos"])

if pagina_selecionada == "Pilotos":
    pagina_pilotos()
elif pagina_selecionada == "Construtores":
    pagina_construtores()
elif pagina_selecionada == "Comparação de Pilotos":
    pagina_comparacao()

st.sidebar.text('Os dados apresentados são gerados aleatoriamente para fins de demonstração.')
