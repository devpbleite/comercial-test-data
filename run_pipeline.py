"""
Pipeline principal — Sales Analytics ETL (DBT Version)
-----------------------------------------
Orquestra as fases:
  1. Ingestão bruta (Raw) dos Excels via python script
  2. Execução das transformações via dbt (Staging e Marts)
  3. Geração direta dos arquivos Parquet pelo dbt-duckdb

Uso:
    python run_pipeline.py
"""

import sys, time, subprocess
from pathlib import Path

ROOT = Path(__file__).parent
DBT_DIR = ROOT / "sales_dbt"
PARQUET_DIR = ROOT / "output" / "parquet"

def run_cmd(cmd, cwd=None):
    process = subprocess.Popen(
        cmd, cwd=cwd, shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    process.communicate()
    if process.returncode != 0:
        print(f"\n[ERRO] Comando falhou: {cmd}")
        sys.exit(1)

def main() -> None:
    print("=" * 55)
    print("  Sales Analytics Pipeline (DBT)")
    print("=" * 55)

    start = time.time()

    print("\n[FASE 1] Ingestão Raw Data...")
    run_cmd(f"{sys.executable} scripts/load_raw.py", cwd=str(ROOT))

    print("\n[FASE 2] Executando modelagem DBT (Staging & Marts)...")
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    run_cmd("dbt run", cwd=str(DBT_DIR))

    elapsed = time.time() - start
    print(f"\n✓ Pipeline concluído em {elapsed:.1f}s")
    
    # Verifica Parquets
    print("\n[VERIFICAÇÃO] Arquivos Parquet gerados (Power BI ready):")
    if PARQUET_DIR.exists():
        for f in PARQUET_DIR.glob("*.parquet"):
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name:<30} {size_kb:>7.1f} KB")
    else:
        print("  [AVISO] Pasta output/parquet não encontrada.")

    db_path = ROOT / "output" / "sales.duckdb"
    if db_path.exists():
        print(f"\n✓ Banco DuckDB atualizado em: {db_path.resolve()}")
    
if __name__ == "__main__":
    main()
