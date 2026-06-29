from prefect import flow, task
import subprocess
import os
from ingest import ingest_data

os.environ["PREFECT_API_URL"] = ""

@task(name="Ingesta de Datos FIFA")
def task_ingest():
    # Llama a la función que ya creamos en ingest.py
    ingest_data()

@task(name="Transformacion Analitica dbt")
def task_dbt_transform():
    print("Iniciando transformaciones y modelos con dbt...")
    # Ejecuta dbt run apuntando a la raíz del proyecto
    result_run = subprocess.run(
        ["dbt", "run", "--project-dir", ".", "--profiles-dir", "."],
        capture_output=True, text=True
    )
    print(result_run.stdout)
    if result_run.returncode != 0:
        print(result_run.stderr)
        raise Exception("Falló la ejecución de dbt run")

@task(name="Pruebas de Calidad dbt")
def task_dbt_test():
    print("Iniciando pruebas de calidad con dbt test...")
    # Ejecuta dbt test
    result_test = subprocess.run(
        ["dbt", "test", "--project-dir", ".", "--profiles-dir", "."],
        capture_output=True, text=True
    )
    print(result_test.stdout)
    if result_test.returncode != 0:
        print(result_test.stderr)
        raise Exception("Fallaron las pruebas de calidad de dbt")

@flow(name="Pipeline Integrado FIFA World Cup 2026")
def fifa_pipeline_flow():
    # Definimos la secuencia exacta que exige la rúbrica
    task_ingest()
    task_dbt_transform()
    task_dbt_test()

if __name__ == "__main__":
    fifa_pipeline_flow()
