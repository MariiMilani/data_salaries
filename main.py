import pandas as pd
import streamlit as st
import plotly.express as px

#  ___Initial config___
st.set_page_config(
    page_title="Análise de salários na área de dados",
    layout="wide",
)

st.title("📊 Dashboard interativo de análises de salários na área de dados")
st.markdown("Sinta-se livre para explorar nesta base de dados de salários na área de dados")

df = pd.read_csv("df_final.csv")

#__Side bar config__
st.sidebar.subheader("🔍 Filtros")

st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: #20B2AA !important;
  color: white;
  font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)

#_Set filters_
all_years = sorted(df['ano'].unique())
selected_years = st.sidebar.multiselect("Ano", all_years, default=all_years)

all_expecience = sorted(df['senioridade'].unique())
selected_experience = st.sidebar.multiselect("Experiência", all_expecience, default=all_expecience)

all_employment_type = sorted(df['contrato'].unique())
selected_employment_type = st.sidebar.multiselect("Contrato de trabalho", all_employment_type, default=all_employment_type)

all_type_of_work = sorted(df['modalidade'].unique())
selected_type_of_work = st.sidebar.multiselect("Tipo de trabalho", all_type_of_work, default=all_type_of_work)

#_Apllying filters_
df_filtered = df[
    df['ano'].isin(selected_years) &
    df['senioridade'].isin(selected_experience) &
    df['contrato'].isin(selected_employment_type) &
    df['modalidade'].isin(selected_type_of_work)
]

#__KPIs__
st.space('large')
st.subheader("📈 Principais métricas (Salário anual em USD)")

if not df_filtered.empty:
    mean_salary = df_filtered['salario_usd'].mean()
    max_salary = df_filtered['salario_usd'].max()
    registers = df_filtered.shape[0]
    top_job = df_filtered['cargo'].mode()[0]

else:
    mean_salary, max_salary, registers, top_job = 0, 0, 0, "Sem informações"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Média salarial anual", f"${mean_salary:,.0f}")
col2.metric("Salário máximo anual", f"${max_salary:,.0f}")
col3.metric("Quantidade de registros", f"{registers:,}")
col4.metric("Cargo mais frequente", top_job)

#__Distribution__
st.space('large')
st.subheader("👁️‍🗨️ Distribuição dos dados")
st.markdown("Com os dados distribuídos entre as principais colunas, fica mais fácil a leitura e interpretação dos gráficos")

col1_dist1, col1_dist2 = st.columns(2)

with col1_dist1:
    if not df_filtered.empty:
        exp_counts = df_filtered['senioridade'].value_counts().reset_index()
        exp_counts.columns = ['experiencia', 'quantidade']

        dist_exp = px.bar(
            exp_counts,
            x='experiencia',
            y='quantidade',
            category_orders= {
                'experiencia': ['junior', 'pleno', 'senior', 'executivo']
            },
            title='Distribuição dos dados por experiência',
            labels={'experiencia': 'Experiências'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        dist_exp.update_layout(title_x=0.1)
        st.plotly_chart(dist_exp, width="stretch")

    else:
        st.warning("Sem informações suficientes para gerar gráfico")

with col1_dist2:
    if not df_filtered.empty:
        year_counts = df_filtered['ano'].value_counts().reset_index()
        year_counts.columns = ['ano', 'quantidade']

        dist_year = px.bar(
            year_counts,
            x='ano',
            y='quantidade',
            title='Distribuição dos dados por ano',
            labels={'ano': 'Ano'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        dist_year.update_layout(title_x=0.1)
        st.plotly_chart(dist_year, width="stretch")

    else:
        st.warning("Sem informações suficientes para gerar gráfico")


col2_dist1, col2_dist2 = st.columns(2)

with col2_dist1:
    if not df_filtered.empty:
        country_counts = df_filtered['residencia_iso3'].value_counts().nlargest(10).reset_index()
        country_counts.columns = ['residencia', 'quantidade']

        dist_country = px.bar(
            country_counts,
            x='residencia',
            y='quantidade',
            title='Distribuição dos dados por país',
            labels={'residencia': 'Países'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        dist_country.update_layout(title_x=0.1)
        st.plotly_chart(dist_country, width="stretch")

    else:
        st.warning("Sem informações suficientes para gerar gráfico")

with col2_dist2:
    if not df_filtered.empty:
        size_counts = df_filtered['porte_empresa'].value_counts().reset_index()
        size_counts.columns = ['porte_empresa', 'quantidade']

        dist_size = px.bar(
            size_counts,
            x='porte_empresa',
            y='quantidade',
            category_orders= {
                'porte_empresa': ['pequena', 'média', 'grande']
            },
            title='Distribuição dos dados por porte de empresa',
            labels={'porte_empresa': 'Porte'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        dist_size.update_layout(title_x=0.1)
        st.plotly_chart(dist_size, width="stretch")

    else:
        st.warning("Sem informações suficientes para gerar gráfico")

# ___Grafics___
st.space('large')
st.subheader("✔️ Gráficos")

col1_graf1, col1_graf2 = st.columns(2)

with col1_graf1:
    if not df_filtered.empty:
        top_jobs_mean = df_filtered.groupby('cargo')['salario_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()

        top_jobs_mean_graf = px.bar(
            top_jobs_mean,
            x= 'salario_usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário anual médio",
            labels={'salario_usd': 'Média salarial anual em USD', 'cargo': 'Cargo'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        top_jobs_mean_graf.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(top_jobs_mean_graf, width="stretch")

    else:
        st.warning("Sem informações suficientes para gerar gráfico")

with col1_graf2:
    if not df_filtered.empty:
        salaries_graf = px.histogram(
            df_filtered,
            x='salario_usd',
            nbins= 40,
            title="Distribuição de sálaios anuais",
            labels={'salario_usd': 'Salário anual em USD'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        salaries_graf.update_layout(title_x=0.1)
        st.plotly_chart(salaries_graf, width="stretch")

    else:
        st.warning("Sem informações suficientes para gerar gráfico")

col2_graf1, col2_graf2 = st.columns(2)

with col2_graf1:
    if not df_filtered.empty:
        df_only_data_scientist = df_filtered[df_filtered['cargo'] == "Data Scientist"]
        df_mean_countries = df_only_data_scientist.groupby('residencia_iso3')['salario_usd'].mean().reset_index()

        map_graf = px.choropleth(
            df_mean_countries,
            locations='residencia_iso3',
            color='salario_usd',
            color_continuous_scale='YlGnBu',
            title="Média salarial anual em USD por país (cargo de Data Scientist)",
            labels={'salario_usd': 'Média salarial anual em USD', 'residencia_iso3': 'País'}
        )

        map_graf.update_layout(title_x=0.1)
        st.plotly_chart(map_graf, width="stretch")
        st.markdown(
            """
            <div style='margin-top: -100px; margin-bottom: 20px; font-size: 0.9rem; color: #e2e8f0;'>
            ⚠️ <b>Atenção:</b> A representatividade global pode ser limitada pela alta concentração de dados nos EUA.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("Sem informações suficientes para gerar gráfico")

with col2_graf2:
    if not df_filtered.empty:
        remote_count = df_filtered['modalidade'].value_counts().reset_index()
        remote_count.columns = ['modalidade', 'quantidade']

        remote_graf = px.pie(
            remote_count,
            names='modalidade',
            values='quantidade',
            title='Proporção de quantidade de tipos de trabalho',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        remote_graf.update_traces(textinfo='percent+label')
        remote_graf.update_layout(title_x=0.1)
        st.plotly_chart(remote_graf, width="stretch")

    else:
        st.warning("Sem informações suficientes para gerar gráfico")


#_DataFrame_
st.space('large')
st.subheader("📁 Dados Detalhados")
st.space('small')
st.dataframe(df_filtered)










