import streamlit as st
import pandas as pd
import unidecode
import re


@st.cache
def read_csv():
    return pd.read_csv("Dados_FAQ.csv")


@st.cache
def compila_string():
    return re.compile("^(##[A-Z]\.[0-9]\.[0-9])")


@st.cache
def trata_dataframe(df):
    df[['origem', 'pergunta', 'resposta']] = df['Dados'].str.split('|', expand=True)
    df.drop(["Dados"], axis=1, inplace=True)
    df["redirecionamento"] = df.apply(lambda x: limpa(x), axis=1)
    return df


@st.cache
def get_origem(df):
    return df.origem.value_counts().to_frame().reset_index(level=0)


@st.cache
def get_pergunta(df):
    return df.pergunta.value_counts().to_frame().reset_index(level=0)


@st.cache
def get_resposta(df):
    return df[df.redirecionamento.isnull()].resposta.value_counts().to_frame().reset_index(level=0)


@st.cache
def get_redirect(df):
    return df.redirecionamento.value_counts().to_frame().reset_index(level=0)


def limpa(x):
    for i in range(len(x)):
        x[i] = unidecode.unidecode(x[i]).strip()
        if i == 2:
            if pattern.match(x[i]):
                return x[i][:7]
            else:
                return None


st.write("Análise de interações chatbot")
st.write("Autor: Lucas Perin Manchine")
st.sidebar.title("Filtros")
df = read_csv()
pattern = compila_string()
df_tratado = trata_dataframe(df[:])
origem = get_origem(df_tratado)
pergunta = get_pergunta(df_tratado)
resposta = get_resposta(df_tratado)
redirecionamento = get_redirect(df_tratado)
origens = st.sidebar.multiselect(
    label="Origens",
    options=origem['index'].unique()
)
redirects = st.sidebar.multiselect(
    label="Redirecionamentos",
    options=redirecionamento['index'].unique()
)

if origens or redirects:
    if origens and redirects:
        df_tratado = trata_dataframe(
            df[df_tratado.origem.isin(origens) & df_tratado.redirecionamento.isin(redirects)][:]
        )
    elif origens:
        df_tratado = trata_dataframe(
            df[df_tratado.origem.isin(origens)][:]
        )
    else:
        df_tratado = trata_dataframe(
            df[df_tratado.redirecionamento.isin(redirects)][:]
        )
    origem = get_origem(df_tratado)
    pergunta = get_pergunta(df_tratado)
    resposta = get_resposta(df_tratado)
    redirecionamento = get_redirect(df_tratado)

lista_casos = ["origem","pergunta","resposta","redirecionamento"]
casos = st.multiselect(
    label="Casos a serem analisados",
    options=lista_casos
)

for caso in casos:
    st.write(f"Top 5 casos de {caso}")
    for i in range([5,len(eval(caso))][len(eval(caso))<5]):
        st.write(f"{caso} {i+1} (quantidade: {eval(caso).eval(caso)[i]}):")
        st.write(f"{eval(caso)['index'][i]}")
        st.write("\n")
    for _ in range(3):
        st.write("\n")
