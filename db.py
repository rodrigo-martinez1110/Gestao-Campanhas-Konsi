import streamlit as st
from supabase import create_client

# Configure aqui ou use st.secrets no app principal
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def inserir_campanha(dados: dict):
    """
    Insere um dicionário representando uma campanha na tabela campanhas_planejadas.
    """
    response = supabase.table("campanhas_planejadas").insert(dados).execute()
    if response.error is not None:
        st.error(f"Erro ao inserir campanha: {response.error.message}")
    else:
        st.success("Campanha inserida com sucesso!")

def listar_campanhas_por_semana(semana_iso: str):
    """
    Retorna uma lista de dicionários das campanhas da semana_iso informada.
    """
    response = (
        supabase.table("campanhas_planejadas")
        .select("*")
        .eq("semana_iso", semana_iso)
        .order("data_disparo")
        .execute()
    )
    if response.error is None:
        return response.data  # lista de dicts
    else:
        st.error(f"Erro ao listar campanhas: {response.error.message}")
        return []

def atualizar_quantidade_disparo(tag_campanha: str, nova_quantidade: int):
    """
    Atualiza a quantidade_disparo da campanha identificada pela tag_campanha.
    """
    response = (
        supabase.table("campanhas_planejadas")
        .update({"quantidade_disparo": nova_quantidade})
        .eq("tag_campanha", tag_campanha)
        .execute()
    )
    if response.error is not None:
        st.error(f"Erro ao atualizar campanha: {response.error.message}")
