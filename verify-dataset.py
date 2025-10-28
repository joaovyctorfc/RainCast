import os
import xarray as xr

# ==============================
# CONFIGURAÇÕES
# ==============================
anos = ["2010","2011","2012","2013","2014","2015", "2016", "2017", "2018", "2019", "2020"]

variaveis = [
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_dewpoint_temperature",
    "2m_temperature",
    "mean_sea_level_pressure",
    "sea_surface_temperature",
    "skin_temperature",
    "surface_latent_heat_flux",
    "surface_sensible_heat_flux",
]

# Nome base dos arquivos (mesma lógica do script original)
def nome_arquivo(var, ano):
    var_sigla = var.replace(" ", "_").replace("/", "_")
    return f"era5_{var_sigla}_{ano}.nc"

# ==============================
# VERIFICAÇÃO
# ==============================
ok = []
falhas = []

for var in variaveis:
    for ano in anos:
        fname = nome_arquivo(var, ano)
        if not os.path.exists(fname):
            falhas.append((var, ano, "Arquivo não encontrado"))
            continue

        # Verifica tamanho mínimo (ex: >100 KB)
        if os.path.getsize(fname) < 100_000:
            falhas.append((var, ano, "Arquivo muito pequeno — possivelmente corrompido"))
            continue

        # Tenta abrir com xarray (checagem de integridade)
        try:
            ds = xr.open_dataset(fname)
            # Verifica se há dados
            if len(ds.data_vars) == 0:
                falhas.append((var, ano, "Arquivo sem variáveis"))
            else:
                ok.append((var, ano))
            ds.close()
        except Exception as e:
            falhas.append((var, ano, f"Erro ao abrir: {e}"))

# ==============================
# RELATÓRIO FINAL
# ==============================
print("\n📋 RELATÓRIO DE VERIFICAÇÃO")
print("=" * 60)
print(f"Total esperado: {len(variaveis) * len(anos)} arquivos")
print(f"✅ OK: {len(ok)}")
print(f"⚠️ Falhas: {len(falhas)}")
print("=" * 60)

if falhas:
    print("\n❌ Detalhes das falhas:")
    for var, ano, msg in falhas:
        print(f" - {var} ({ano}): {msg}")
else:
    print("🎉 Tudo certo! Todos os arquivos foram baixados e abertos com sucesso.")
