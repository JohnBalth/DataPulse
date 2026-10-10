from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"


FILES = {
    "pedidos": "olist_orders_dataset.csv",
    "itens": "olist_order_items_dataset.csv",
    "produtos": "olist_products_dataset.csv",
    "pagamentos": "olist_order_payments_dataset.csv",
}


def inspect_csv(name: str, filename: str) -> None:
    file_path = DATA_DIR / filename

    print(f"\n{'=' * 60}")
    print(f"ARQUIVO: {name}")
    print(f"{'=' * 60}")

    if not file_path.exists():
        print(f"Arquivo não encontrado: {file_path}")
        return

    df = pd.read_csv(file_path)

    print(f"Linhas: {len(df):,}")
    print(f"Colunas: {len(df.columns)}")

    print("\nColunas disponíveis:")
    print(df.columns.tolist())

    print("\nTipos de dados:")
    print(df.dtypes)

    print("\nPrimeiras cinco linhas:")
    print(df.head().to_string(index=False))

    print("\nValores ausentes por coluna:")
    print(df.isna().sum())


def main() -> None:
    for name, filename in FILES.items():
        inspect_csv(name, filename)


if __name__ == "__main__":
    main()