import polars as pl
import duckdb
import os

REQUIRED_COLUMNS = [
    "player_id",
    "player_name",
    "nationality",
    "position",
    "age",
    "height_cm",
    "goals",
    "shots_on_target",
    "expected_goals_xg",
    "yellow_cards"
]

# Esquema esperado: columna -> tipo Polars (para validar tipos de dato)
EXPECTED_TYPES = {
    "player_id": pl.Utf8,
    "player_name": pl.Utf8,
    "nationality": pl.Utf8,
    "position": pl.Utf8,
    "age": pl.Int64,
    "height_cm": pl.Int64,
    "goals": pl.Int64,
    "shots_on_target": pl.Int64,
    "expected_goals_xg": pl.Float64,
    "yellow_cards": pl.Int64,
}

DB_PATH = "data/transformed/fifa.duckdb"


def ingest_data():
    print("Iniciando la ingesta del dataset de FIFA 2026...")

    csv_path_full = "data/raw/fifa_data.csv"
    csv_path_sample = "data/raw/fifa_sample.csv"

    if os.path.exists(csv_path_full):
        csv_path = csv_path_full
        print("-> Procesando dataset completo proporcionado por el evaluador.")
    elif os.path.exists(csv_path_sample):
        csv_path = csv_path_sample
        print("-> Procesando dataset de muestra integrado en el repositorio.")
    else:
        raise FileNotFoundError(
            "No se encontro ningun archivo CSV de origen en data/raw/ "
            "(se esperaba fifa_data.csv o fifa_sample.csv)"
        )

    # 1. Leer el CSV con manejo de errores
    try:
        df = pl.read_csv(csv_path, infer_schema_length=10000)
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo CSV '{csv_path}': {e}")

    # 2. Validar que existan las columnas requeridas
    columnas_faltantes = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if columnas_faltantes:
        raise ValueError(f"Faltan columnas requeridas en el CSV: {columnas_faltantes}")

    df = df.select(REQUIRED_COLUMNS)

    # 3. Validar y castear tipos de dato
    for columna, tipo in EXPECTED_TYPES.items():
        try:
            df = df.with_columns(pl.col(columna).cast(tipo, strict=False))
        except Exception as e:
            raise RuntimeError(f"Error al castear la columna '{columna}' a {tipo}: {e}")

    filas_antes = df.height
    # Descartar filas con datos invalidos/nulos en columnas clave tras el casteo
    df = df.drop_nulls(subset=["player_id", "goals", "position"])
    filas_despues = df.height
    if filas_antes != filas_despues:
        print(f"-> Se descartaron {filas_antes - filas_despues} filas con datos invalidos o nulos.")

    # 4. Eliminar duplicados por player_id y limitar a 5000 registros
    df_filtered = df.unique(subset=["player_id"]).limit(5000)

    if df_filtered.height == 0:
        raise ValueError("El dataset quedo vacio despues de la limpieza. Revisa el archivo de origen.")

    # 5. Escribir tabla cruda en DuckDB
    os.makedirs("data/transformed", exist_ok=True)
    try:
        con = duckdb.connect(DB_PATH)
        con.execute("CREATE OR REPLACE TABLE raw_player_performance AS SELECT * FROM df_filtered")
        con.close()
    except Exception as e:
        raise RuntimeError(f"Error al escribir en DuckDB ({DB_PATH}): {e}")

    print("Ingesta, validacion y carga en DuckDB completadas exitosamente!")
    print(f"Total de registros unicos guardados en tabla 'raw_player_performance': {df_filtered.height}")


if __name__ == "__main__":
    ingest_data()
