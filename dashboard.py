"""
Placement Data Analytics Dashboard (demo)

Usage:
    # CSV demo (no DB required)
    python dashboard.py --mode csv

    # MySQL mode (optional)
    python dashboard.py --mode mysql

Notes:
- For CSV mode the script reads `data/sample_placements.csv`.
- For MySQL mode update DB_CONFIG below and ensure schema/data from sql/schema_and_sample.sql is loaded.
"""

import os
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ---------- CONFIG ----------
OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

# If you want to use MySQL mode, fill these values
DB_CONFIG = {
    "host": "localhost",
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "database": "placement_db",
    "port": 3306
}

CSV_PATH = Path("data") / "sample_placements.csv"

# ---------- DATA LOADERS ----------
def load_from_csv(path=CSV_PATH):
    if not Path(path).exists():
        raise FileNotFoundError(f"{path} not found. Please add sample CSV or run in mysql mode.")
    df = pd.read_csv(path, parse_dates=["offer_date"])
    # normalize column names if necessary
    # Expected columns: student_id, roll_no, student_name, branch, cgpa, batch_year,
    # company_name, package_lpa, role, offer_date
    df["offer_year"] = df["offer_date"].dt.year
    return df

def load_from_mysql(db_config=DB_CONFIG):
    try:
        import mysql.connector
    except ImportError as e:
        raise ImportError("mysql-connector-python is required for mysql mode. Install via pip.") from e

    conn = mysql.connector.connect(
        host=db_config.get("host", "localhost"),
        user=db_config.get("user"),
        password=db_config.get("password"),
        database=db_config.get("database"),
        port=db_config.get("port", 3306)
    )
    # Read combined query — join placements, students, branches, companies
    query = """
    SELECT
      p.id as placement_id,
      s.id as student_id,
      s.roll_no,
      s.name as student_name,
      b.name as branch,
      s.cgpa,
      s.batch_year,
      c.name as company_name,
      p.package_lpa,
      p.role,
      p.offer_date
    FROM placement p
      JOIN student s ON p.student_id = s.id
      JOIN branch b ON s.branch_id = b.id
      JOIN company c ON p.company_id = c.id
    """
    df = pd.read_sql(query, conn, parse_dates=["offer_date"])
    conn.close()
    df["offer_year"] = df["offer_date"].dt.year
    return df

# ---------- PLOTS / ANALYSES ----------
def placements_per_branch(df, year=None):
    d = df.copy()
    if year is not None:
        d = d[d["offer_year"] == int(year)]
    counts = d.groupby("branch").student_id.nunique().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    counts.plot(kind="bar")
    title = "Students Placed per Branch" + (f" - {year}" if year else "")
    plt.title(title)
    plt.ylabel("Number of students placed")
    plt.xlabel("Branch")
    plt.tight_layout()
    path = OUTPUT_DIR / f"placements_per_branch_{year if year else 'all'}.png"
    plt.savefig(path)
    plt.close()
    print("Saved", path)

def avg_package_per_branch(df, year=None):
    d = df.copy()
    if year is not None:
        d = d[d["offer_year"] == int(year)]
    avg = d.groupby("branch").package_lpa.mean().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    avg.plot(kind="bar")
    title = "Average Package (LPA) per Branch" + (f" - {year}" if year else "")
    plt.title(title)
    plt.ylabel("Average Package (LPA)")
    plt.xlabel("Branch")
    plt.tight_layout()
    path = OUTPUT_DIR / f"avg_package_per_branch_{year if year else 'all'}.png"
    plt.savefig(path)
    plt.close()
    print("Saved", path)

def top_companies_by_offers(df, top_n=5, year=None):
    d = df.copy()
    if year is not None:
        d = d[d["offer_year"] == int(year)]
    counts = d.groupby("company_name").student_id.nunique().sort_values(ascending=False).head(top_n)
    plt.figure(figsize=(6,6))
    counts.plot(kind="pie", autopct="%1.1f%%")
    title = f"Top {top_n} Companies by Offers" + (f" - {year}" if year else "")
    plt.title(title)
    plt.ylabel("")
    plt.tight_layout()
    path = OUTPUT_DIR / f"top_companies_{year if year else 'all'}.png"
    plt.savefig(path)
    plt.close()
    print("Saved", path)

def salary_distribution(df, year=None):
    d = df.copy()
    if year is not None:
        d = d[d["offer_year"] == int(year)]
    plt.figure(figsize=(8,5))
    plt.hist(d["package_lpa"].dropna(), bins=12)
    title = "Salary Distribution (LPA)" + (f" - {year}" if year else "")
    plt.title(title)
    plt.xlabel("Package (LPA)")
    plt.ylabel("Count")
    plt.tight_layout()
    path = OUTPUT_DIR / f"salary_distribution_{year if year else 'all'}.png"
    plt.savefig(path)
    plt.close()
    print("Saved", path)

def heatmap_branch_company(df, year=None):
    d = df.copy()
    if year is not None:
        d = d[d["offer_year"] == int(year)]
    pivot = d.pivot_table(values="student_id", index="branch", columns="company_name",
                          aggfunc="nunique", fill_value=0)
    plt.figure(figsize=(10,6))
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(label="Number of students placed")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45, ha="right")
    plt.yticks(range(len(pivot.index)), pivot.index)
    title = "Branches vs Companies heatmap" + (f" - {year}" if year else "")
    plt.title(title)
    plt.tight_layout()
    path = OUTPUT_DIR / f"heatmap_branch_company_{year if year else 'all'}.png"
    plt.savefig(path)
    plt.close()
    print("Saved", path)

# ---------- MAIN ----------
def main(mode="csv", year=None):
    if mode == "csv":
        df = load_from_csv()
    elif mode == "mysql":
        df = load_from_mysql()
    else:
        raise ValueError("Unsupported mode. Choose 'csv' or 'mysql'.")

    print(f"Loaded {len(df)} placement rows (offers).")
    placements_per_branch(df, year=year)
    avg_package_per_branch(df, year=year)
    top_companies_by_offers(df, top_n=6, year=year)
    salary_distribution(df, year=year)
    heatmap_branch_company(df, year=year)
    print("All plots are saved in", OUTPUT_DIR.resolve())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Placement Data Analytics Dashboard")
    parser.add_argument("--mode", choices=["csv", "mysql"], default="csv",
                        help="Mode: 'csv' (demo) or 'mysql' (connect to DB).")
    parser.add_argument("--year", type=int, default=None, help="Optional: filter plots for a specific year (e.g., 2025)")
    args = parser.parse_args()
    main(mode=args.mode, year=args.year)
