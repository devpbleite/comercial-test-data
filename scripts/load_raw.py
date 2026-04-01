import sys, duckdb, pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "output" / "sales.duckdb"
RAW_DIR = ROOT / "data" / "raw"

RAW_FILES = {
    "vendas_1t":   RAW_DIR / "Vendas.xlsx",
    "vendas_2t":   RAW_DIR / "Vendas_2T.xlsx",
    "consultores": RAW_DIR / "Consultores.xlsx",
    "lojas":       RAW_DIR / "Lojas.xlsx",
    "metas":       RAW_DIR / "Metas.xlsx",
}

def main():
    print("=" * 55)
    print("  Load RAW data to DuckDB")
    print("=" * 55)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    
    # Criar schema raw se não existir
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    print("[RAW] Lendo Excel e salvando no DuckDB (schema: raw)...")
    
    for key, path in RAW_FILES.items():
        if not path.exists():
            print(f"  [AVISO] Arquivo não encontrado: {path}")
            continue

        table_name = f"raw.raw_{key}"
        
        if key == "vendas_2t":
            df = pd.read_excel(path, sheet_name="Vendas 2T-24")
        else:
            df = pd.read_excel(path)

        con.register("_tmp_df", df)
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM _tmp_df")
        
        count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"  [{table_name:<20}] {count:>7,} linhas inseridas.")

    con.close()
    print("[RAW] Concluído.\n")

if __name__ == "__main__":
    main()
