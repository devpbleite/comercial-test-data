"""
explore.py — Inspetor do sales.duckdb
---------------------------------------
Visualize o conteúdo do banco sem precisar de ferramenta externa.

Uso:
    python scripts/explore.py                        # visão geral
    python scripts/explore.py mart_faturamento       # preview + stats de uma tabela
    python scripts/explore.py --sql "SELECT ..."     # query livre
"""

import sys, duckdb
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DB_PATH = ROOT / "output" / "sales.duckdb"
SEP     = "─" * 70
SEP2    = "═" * 70

TABLES_QUERY = """
    SELECT table_name FROM information_schema.tables
    WHERE table_schema='main' AND table_type IN ('BASE TABLE', 'VIEW')
    ORDER BY table_name
"""


def fmt(val) -> str:
    if isinstance(val, float): return f"{val:,.2f}"
    if isinstance(val, int):   return f"{val:,}"
    return str(val) if val is not None else "NULL"


def print_rows(rows, headers):
    if not rows:
        print("  (sem resultados)")
        return
    widths = [max(len(str(h)), max(len(fmt(r[i])) for r in rows)) for i, h in enumerate(headers)]
    print("  " + "  ".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    print("  " + "  ".join("─" * w for w in widths))
    for row in rows:
        print("  " + "  ".join(fmt(v).ljust(w) for v, w in zip(row, widths)))


def overview(con):
    print(f"\n{SEP2}\n  SALES.DUCKDB — Visão Geral\n{SEP2}\n")
    tables = [t[0] for t in con.execute(TABLES_QUERY).fetchall()]

    print(f"  {'TABELA':<28} {'LINHAS':>10}  COLUNAS")
    print(f"  {SEP}")
    for name in tables:
        rows = con.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        cols = con.execute(f"SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{name}' AND table_schema='main'").fetchone()[0]
        print(f"  {name:<28} {rows:>10,}  {cols} colunas")

    print(f"\n  {'KPIs GERAIS':^68}\n  {SEP}")
    kpis = [
        ("Receita total (1T + 2T)",        "SELECT ROUND(SUM(revenue),2) FROM mart_faturamento"),
        ("Receita 1T",                      "SELECT ROUND(SUM(revenue),2) FROM mart_faturamento WHERE quarter=1"),
        ("Receita 2T",                      "SELECT ROUND(SUM(revenue),2) FROM mart_faturamento WHERE quarter=2"),
        ("Crescimento 1T → 2T (%)",         "SELECT ROUND((SUM(CASE WHEN quarter=2 THEN revenue END)/SUM(CASE WHEN quarter=1 THEN revenue END)-1)*100,1) FROM mart_faturamento"),
        ("Ticket médio das lojas",          "SELECT ROUND(AVG(ticket_medio),2) FROM mart_lojas"),
        ("Atingimento médio de meta (%)",   "SELECT ROUND(AVG(pct_achievement),1) FROM mart_metas"),
        ("Loja com maior receita",          "SELECT store_name FROM (SELECT store_name, SUM(total_revenue) r FROM mart_lojas GROUP BY 1 ORDER BY r DESC LIMIT 1)"),
        ("Top vendedor",                    "SELECT seller_name FROM (SELECT seller_name, SUM(total_revenue) r FROM mart_vendedores GROUP BY 1 ORDER BY r DESC LIMIT 1)"),
    ]
    for label, query in kpis:
        val = con.execute(query).fetchone()[0]
        print(f"  {label:<35} {fmt(val):>20}")
    print()


def inspect_table(con, table_name):
    exists = con.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='main' AND table_name='{table_name}' AND table_type IN ('BASE TABLE', 'VIEW')").fetchone()[0]
    if not exists:
        available = [t[0] for t in con.execute(TABLES_QUERY).fetchall()]
        print(f"\n  Tabela '{table_name}' não encontrada. Disponíveis: {available}\n")
        return

    print(f"\n{SEP2}\n  TABELA: {table_name.upper()}\n{SEP2}")
    cols = con.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table_name}' AND table_schema='main' ORDER BY ordinal_position").fetchall()

    print(f"\n  {'COLUNA':<30} TIPO\n  {'─'*30} {'─'*20}")
    for col, dtype in cols:
        print(f"  {col:<30} {dtype}")

    print(f"\n  Preview (5 linhas):\n  {SEP}")
    rows    = con.execute(f'SELECT * FROM "{table_name}" LIMIT 5').fetchall()
    headers = [c[0] for c in cols]
    print_rows(rows, headers)

    num_cols = [c[0] for c in cols if any(t in c[1].upper() for t in ("INT","FLOAT","DOUBLE","DECIMAL","HUGEINT","BIGINT"))]
    if num_cols:
        print(f"\n  Estatísticas numéricas:\n  {SEP}")
        for col in num_cols[:6]:
            s = con.execute(f'SELECT MIN("{col}"), MAX("{col}"), ROUND(AVG("{col}"),2), ROUND(STDDEV("{col}"),2) FROM "{table_name}"').fetchone()
            print(f"  {col:<28}  min={fmt(s[0])}  max={fmt(s[1])}  avg={fmt(s[2])}  std={fmt(s[3])}")
    print()


def run_sql(con, sql):
    print(f"\n{SEP2}\n  SQL: {sql[:65]}{'...' if len(sql)>65 else ''}\n{SEP2}\n")
    try:
        cur  = con.execute(sql)
        rows = cur.fetchall()
        print_rows(rows, [d[0] for d in cur.description])
        print(f"\n  {len(rows)} linha(s) retornada(s).\n")
    except Exception as e:
        print(f"\n  Erro: {e}\n")


def main():
    if not DB_PATH.exists():
        print(f"\n  Banco não encontrado em: {DB_PATH}\n  Execute primeiro: python run_pipeline.py\n")
        sys.exit(1)

    import os
    os.chdir(ROOT / "sales_dbt")
    con  = duckdb.connect(str(DB_PATH), read_only=True)
    args = sys.argv[1:]
    try:
        if not args:          overview(con)
        elif args[0]=="--sql": run_sql(con, " ".join(args[1:]))
        else:                  inspect_table(con, args[0])
    finally:
        con.close()

if __name__ == "__main__":
    main()
