import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
from db import inserir_campanha, listar_campanhas_por_semana
from utils import gerar_tag, calcular_semana_iso

st.set_page_config(layout="wide")
st.title("📅 Planejamento de Campanhas - Semana")

def gerar_semanas_ano(ano):
    primeiro_dia = datetime(ano, 1, 1)
    primeiro_segunda = primeiro_dia + timedelta(days=(7 - primeiro_dia.weekday()) % 7)
    
    semanas = []
    data_atual = primeiro_segunda
    
    while data_atual.year == ano:
        segunda = data_atual
        sabado = segunda + timedelta(days=5)
        semanas.append((segunda, sabado))
        data_atual += timedelta(weeks=1)
    return semanas

def formatar_semana(semana):
    segunda, sabado = semana
    return f"{segunda.strftime('%d/%m/%Y')} a {sabado.strftime('%d/%m/%Y')}"

ano_atual = datetime.today().year
semanas = gerar_semanas_ano(ano_atual)

# --- NOVO: seleção de mês e ano ---
meses_display = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]
mes_ano_selecionado = st.selectbox("Escolha o mês e ano", meses_display, index=datetime.today().month-1)
mes_num = meses_display.index(mes_ano_selecionado) + 1

# Filtra semanas que começam no mês selecionado
semanas_do_mes = [s for s in semanas if s[0].month == mes_num]
semanas_formatadas_do_mes = [formatar_semana(s) for s in semanas_do_mes]

semana_selecionada = st.selectbox("Escolha a semana", semanas_formatadas_do_mes)

indice_semana = semanas_formatadas_do_mes.index(semana_selecionada)
segunda_escolhida, sabado_escolhido = semanas_do_mes[indice_semana]

st.markdown(f"### Semana escolhida: {semana_selecionada}")

# Calcula semana_iso a partir da segunda-feira
semana_iso = calcular_semana_iso(str(segunda_escolhida.date()))

campanhas = listar_campanhas_por_semana(semana_iso)

if not campanhas.empty:
    campanhas['data_disparo'] = pd.to_datetime(campanhas['data_disparo'])
    campanhas = campanhas[(campanhas['data_disparo'].dt.date >= segunda_escolhida.date()) & 
                          (campanhas['data_disparo'].dt.date <= sabado_escolhido.date())]
    
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    campanhas['dia_semana'] = campanhas['data_disparo'].dt.dayofweek
    campanhas['dia_semana_nome'] = campanhas['dia_semana'].apply(lambda x: dias_semana[x])

    cols = st.columns(7)
    for i, dia in enumerate(dias_semana):
        with cols[i]:
            st.markdown(f"### {dia}")
            campanhas_dia = campanhas[campanhas['dia_semana_nome'] == dia]

            if not campanhas_dia.empty:
                for _, row in campanhas_dia.iterrows():
                    st.markdown(f"""
                        <div style="border:1px solid #1e3a8a; border-radius:10px; padding:10px; margin-bottom:10px; background-color:#1e3a8a; color: white;">
                            <strong>{row['convenio']}</strong><br>
                            Produto: {row['produto']}<br>
                            Canal: {row['canal']}<br>
                            Meta: {row['meta_leads']}<br>
                            Disparos: {row['quantidade_disparo']}<br>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("🟦")
else:
    st.info("Nenhuma campanha cadastrada para essa semana.")

with st.sidebar.expander("➕ Adicionar nova campanha"):
    convenio = st.text_input("Convênio (Ex: GOV SP)")
    produto = st.selectbox("Produto", ["Novo", "Benefício", 'Cartão', 'Benefício e Cartão'])
    canal = st.selectbox("Canal", ["RCS + SMS", 'RCS', 'SMS', 'Whatsapp', 'Email', 'Resgate'])
    data_disparo = st.date_input("Data do disparo", value=datetime.today().date())
    meta = st.number_input("Meta de leads", min_value=0)
    observacoes = st.text_area("Observações")

    if st.button("Salvar campanha"):
        tag = gerar_tag(convenio, produto, str(data_disparo))
        
        nova_campanha = {
            "tag_campanha": tag,
            "convenio": convenio,
            "produto": produto,
            "canal": canal,
            "data_disparo": data_disparo,
            "semana_iso": calcular_semana_iso(str(data_disparo)),
            "meta_leads": meta,
            "observacoes": observacoes,
            "quantidade_disparo": 0
        }

        inserir_campanha(nova_campanha)
        st.success(f"Campanha '{tag}' salva com sucesso!")
        st.experimental_rerun()
