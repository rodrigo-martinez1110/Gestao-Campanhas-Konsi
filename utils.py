from datetime import datetime

def gerar_tag(convenio, produto, data_disparo):
    data_fmt = datetime.strptime(data_disparo, "%Y-%m-%d").strftime("%d%m%Y")
    return f"{convenio.lower().replace(' ', '')}_{produto.lower()}_{data_fmt}_outbound"

def calcular_semana_iso(data_disparo):
    dt = datetime.strptime(data_disparo, "%Y-%m-%d")
    return f"{dt.year}-W{dt.isocalendar()[1]}"
