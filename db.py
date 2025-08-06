import streamlit as st
import pandas as pd
from supabase import create_client


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

SUPABASE_URL = st.secrets["SUPABASE_URL"]


supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)


def inserir_campanha(dados):
    response = supabase.table("campanhas_planejadas").insert(dados).execute()
    if response.error is not None:
        st.error(f"Erro ao inserir campanha: {response.error.message}")
    else:
        st.success("Campanha inserida com sucesso!")
    
def listar_campanhas_por_semana(semana_iso):
    response = (
        supabase.table("campanhas_planejadas")
        .select("*")
        .eq("semana_iso", semana_iso)
        .order("data_disparo")
        .execute()
    )
    if response.error is None:
        return response.data  # que é uma lista de dicionários
    else:
        st.error(f"Erro ao buscar campanhas: {response.error.message}")
        return []


def atualizar_quantidade_disparo(tag_campanha, nova_quantidade):
    response = (
        supabase.table("campanhas_planejadas")
        .update({"quantidade_disparo": nova_quantidade})
        .eq("tag_campanha", tag_campanha)
        .execute()
    )
    if response.error is not None:
        st.error(f"Erro ao atualizar campanha: {response.error.message}")