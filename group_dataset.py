import xarray as xr
import os

arquivos = [f for f in os.listdir(".") if f.endswith(".nc")]

print(f"🔍 Encontrados {len(arquivos)} arquivos para juntar...")

# Usa leitura com Dask (sem carregar tudo na memória)
ds_completo = xr.open_mfdataset(
    arquivos,
    combine="by_coords",
    chunks={"time": 100},  # carrega 100 timesteps por vez
    parallel=False          # evita travamentos
)

output_file = "ERA5_todas_variaveis_2015_2020.nc"
ds_completo.to_netcdf(output_file, compute=True)

print(f"✅ Arquivo combinado salvo como: {output_file}")
