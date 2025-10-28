import cdsapi
import time
import os

# Inicializa o cliente da API
client = cdsapi.Client()

# Dataset
dataset = "derived-era5-single-levels-daily-statistics"

# Anos desejados
anos = ["2011"]

# Lista de variáveis
variaveis = [
    #"10m_u_component_of_wind",
    "10m_v_component_of_wind",
    #"2m_dewpoint_temperature",
    #"2m_temperature",
    #"mean_sea_level_pressure",
    #"sea_surface_temperature",
    #"skin_temperature",
    #"surface_latent_heat_flux",
    #"surface_sensible_heat_flux"
]

# Lista de meses e dias (para o pedido completo do ano)
meses = [f"{m:02d}" for m in range(1, 13)]
dias = [f"{d:02d}" for d in range(1, 32)]

# Arquivo de log
log_file = "download_log.txt"

# Função para escrever no log
def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)  # também imprime no console

# Loop principal
for var_nome in variaveis:
    for ano in anos:
        var_sigla = var_nome.replace(" ", "_").replace("/", "_")
        output_file = f"era5_{var_sigla}_{ano}.nc"

        if os.path.exists(output_file):
            log(f"⏩ Arquivo já existe, pulando: {output_file}")
            continue

        log(f"🔹 Baixando {var_nome} - {ano}...")

        request = {
            "product_type": "reanalysis",
            "variable": [var_nome],
            "year": ano,
            "month": meses,
            "day": dias,
            "daily_statistic": "daily_mean",
            "time_zone": "utc+00:00",
            "frequency": "1_hourly",
            "area": [12.9, -82.7, -56.5, -33.2],
            "format": "netcdf"
        }

        try:
            client.retrieve(dataset, request).download(output_file)
            log(f"✅ Download concluído: {output_file}")

        except Exception as e:
            log(f"❌ Erro ao baixar {var_nome} ({ano}): {e}")
            log("⏳ Tentando novamente em 60 segundos...")
            time.sleep(60)
            try:
                client.retrieve(dataset, request).download(output_file)
                log(f"✅ Download concluído na segunda tentativa: {output_file}")
            except Exception as e2:
                log(f"🚫 Falha definitiva em {var_nome} ({ano}): {e2}")

log("🎯 Todos os downloads finalizados!")
