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
    if response.status_code not in [200, 201]:
        st.error(f"Erro ao inserir campanha: {response.status_code} - {response.json()}")
    
def listar_campanhas_por_semana(semana_iso):
    response = supabase \
        .table("campanhas_planejadas") \
        .select("*") \
        .eq("semana_iso", semana_iso) \
        .order("data_disparo") \
        .execute()

    if response.status_code == 200:
        return response.data  # pode usar pd.DataFrame(response.data) se quiser
    else:
        st.error("Erro ao listar campanhas: " + str(response.status_code))
        return []

def atualizar_quantidade_disparo(tag_campanha, nova_quantidade):
    response = supabase \
        .table("campanhas_planejadas") \
        .update({"quantidade_disparo": nova_quantidade}) \
        .eq("tag_campanha", tag_campanha) \
        .execute()

    if response.status_code not in [200, 204]:
        st.error("Erro ao atualizar: " + str(response.status_code))