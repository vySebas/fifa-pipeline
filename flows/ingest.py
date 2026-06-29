import polars as pl
import os

def ingest_data():
    print("Iniciando la ingesta con eliminación de duplicados de FIFA 2026...")
    
    csv_path = "data/raw/fifa_data.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: No se encontró el archivo en {csv_path}")
        return

    # 1. Leer el CSV completo
    df = pl.read_csv(csv_path, infer_schema_length=10000)

    required_columns = [
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

    # 2. Filtrar columnas, quitar nulos, y ELIMINAR DUPLICADOS por ID antes del limit
    df_filtered = (
        df.select(required_columns)
        .drop_nulls(subset=["player_id"])
        .unique(subset=["player_id"])
        .limit(5000)
    )

    # 3. Guardar en Parquet limpio
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/fifa_clean.parquet"
    df_filtered.write_parquet(output_path)

    print(f"¡Ingesta y Depuración completada exitosamente!")
    print(f"Total de registros únicos guardados para dbt: {df_filtered.height}")

if __name__ == "__main__":
    ingest_data()

