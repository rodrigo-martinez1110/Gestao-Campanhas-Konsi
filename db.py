import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

SUPABASE_URL = st.secrets["SUPABASE_URL"]

engine = create_engine(SUPABASE_URL)

def inserir_campanha(dados):
    df = pd.DataFrame([dados])
    df.to_sql("campanhas_planejadas", engine, if_exists="append", index=False)
    
def listar_campanhas_por_semana(semana_iso):
    query = f"""
        SELECT * FROM campanhas_planejadas
        WHERE semana_iso = '{semana_iso}'
        ORDER BY data_disparo;
    """
    return pd.read_sql(query, engine)

def atualizar_quantidade_disparo(tag_campanha, nova_quantidade):
    query = f"""
    UPDATE campanhas_planejadas
    SET quantidade_disparo = {nova_quantidade}
    WHERE tag_campanha = '{tag_campanha}';
    """
    with engine.connect() as conn:
        conn.execute(query)
