import pandas as pd
import plotly.express as px
import geopandas as gpd

# Função para carregar os dados de vacinação
def load_vaccination_data():
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
    df = pd.read_csv(url)
    df = df[['date', 'state', 'vaccinated']]  # Atualize as colunas conforme necessário
    return df

# Função para formatar os números em milhões
def format_number(value):
    if value >= 1_000_000:
        return f'+{value / 1_000_000:.1f}M'
    elif value >= 1_000:
        return f'+{value / 1_000:.1f}K'
    else:
        return str(value)

# Função para criar gráfico de barras interativo com Plotly
def plot_bar_chart(df):
    total_vaccinated = df.groupby('state')['vaccinated'].max().reset_index()
    fig = px.bar(total_vaccinated, x='state', y='vaccinated', text='vaccinated')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, xaxis_title='Estado', yaxis_title='Total de Vacinados')
    fig.update_layout(title='Gráfico de Barras - Total de Vacinados por Estado')
    fig.show()

# Função para criar gráfico de linhas
def plot_line_chart(df, state):
    state_data = df[df['state'] == state]
    fig = px.line(state_data, x='date', y='vaccinated')
    fig.update_layout(title=f'Gráfico de Barras - Evolução da Vacinação em {state}', xaxis_title='Data', yaxis_title='Total de Vacinados')
    fig.show()

# Função para criar mapa choropleth
def plot_choropleth_map(df):
    shapefile_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    shapefile = gpd.read_file(shapefile_url)
    total_vaccinated = df.groupby('state')['vaccinated'].max().reset_index()
    merged = shapefile.set_index('sigla').join(total_vaccinated.set_index('state'))
    
    fig = px.choropleth(merged, geojson=merged.geometry, locations=merged.index, color='vaccinated',
                        hover_name=merged.index, hover_data={'vaccinated': True},
                        labels={'vaccinated': 'Total de Vacinados'})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title='Mapa Choropleth - Vacinação por Estado no Brasil')
    fig.show()

# Função principal
def main():
    df = load_vaccination_data()
    plot_bar_chart(df)
    plot_line_chart(df, 'SP')
    plot_choropleth_map(df)

if __name__ == "__main__":
    main()
