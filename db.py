import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def inserir_campanha(dados: dict):
    try:
        response = supabase.table("campanhas_planejadas").insert(dados).execute()
        if response.data is None:
            st.error("Erro ao inserir campanha: resposta vazia")
        else:
            st.success("Campanha inserida com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inserir campanha: {e}")

def listar_campanhas_por_semana(semana_iso: str):
    try:
        response = (
            supabase.table("campanhas_planejadas")
            .select("*")
            .eq("semana_iso", semana_iso)
            .order("data_disparo")
            .execute()
        )
        if response.data is None:
            st.info("Nenhuma campanha encontrada para esta semana.")
            return []
        return response.data
    except Exception as e:
        st.error(f"Erro ao listar campanhas: {e}")
        return []

def atualizar_quantidade_disparo(tag_campanha: str, nova_quantidade: int):
    try:
        response = (
            supabase.table("campanhas_planejadas")
            .update({"quantidade_disparo": nova_quantidade})
            .eq("tag_campanha", tag_campanha)
            .execute()
        )
        if response.data is None:
            st.error("Erro ao atualizar campanha: resposta vazia")
    except Exception as e:
        st.error(f"Erro ao atualizar campanha: {e}")
