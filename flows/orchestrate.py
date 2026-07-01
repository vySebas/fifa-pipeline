from prefect import flow, task
import subprocess
from flows.ingest import ingest_data

@task(name="Ingesta de Datos FIFA")
def task_ingest():
    ingest_data()

@task(name="Transformación Analítica dbt")
def task_dbt_run():
    print("Ejecutando dbt run...")
    subprocess.run(
        ["dbt", "run", "--project-dir", ".", "--profiles-dir", "."],
        check=True
    )

@task(name="Pruebas de Calidad dbt")
def task_dbt_test():
    print("Ejecutando dbt test...")
    subprocess.run(
        ["dbt", "test", "--project-dir", ".", "--profiles-dir", "."],
        check=True
    )

@task(name="Activacion del Dashboard")
def task_dashboard():
    print("Activando el Dashboard en el puerto 8050...")
    subprocess.run(["python3", "dashboard.py"], check=True)

@flow(name="Pipeline FIFA World Cup 2026")
def fifa_pipeline():
    task_ingest()
    task_dbt_run()
    task_dbt_test()
    task_dashboard()

if __name__ == "__main__":
    fifa_pipeline()
