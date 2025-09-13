
# Placement Data Analytics Dashboard 📊

This project is a **Placement Data Analytics Dashboard** built with **Python (pandas, NumPy, Matplotlib)** and **MySQL** (optional).  
It provides data insights and visualizations on student placements.

---

## 🚀 Features
- MySQL schema for structured placement data storage
- Synthetic dataset for demo (`data/sample_placements.csv`)
- Python script (`dashboard.py`) for data processing and visualization
- Plots: Branch-wise placements, average salary, top companies, salary distribution, heatmap of companies vs. branches
- Ready-to-run demo using CSV (no database setup required)

---

## 📂 Project Structure
```

placement\_dashboard/
│── README.md
│── requirements.txt
│── dashboard.py
│── data/
│   └── sample\_placements.csv
│── plots/                # generated visualizations
│── sql/
│   └── schema\_and\_sample.sql

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/placement_dashboard.git
cd placement_dashboard
````

### 2️⃣ Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
pip install -r requirements.txt
```

### 3️⃣ Run the Dashboard

Using demo CSV data:

```bash
python dashboard.py --mode csv
```

This will generate plots inside the `plots/` folder.

Using MySQL (optional):

* Start MySQL and run `sql/schema_and_sample.sql`
* Update `DB_CONFIG` in `dashboard.py`
* Run:

```bash
python dashboard.py --mode mysql
```

---

## 📊 Sample Outputs

### 1. Placements per Branch

![Placements per Branch](plots/placements_per_branch_all.png)

### 2. Average Package per Branch

![Average Package per Branch](plots/avg_package_per_branch_all.png)

### 3. Top Companies by Offers

![Top Companies](plots/top_companies_all.png)

### 4. Salary Distribution

![Salary Distribution](plots/salary_distribution_all.png)

### 5. Branch vs Company Heatmap

![Heatmap Branch vs Company](plots/heatmap_branch_company_all.png)

---

## 🔮 Future Enhancements

* Streamlit/Flask front-end for interactive dashboard
* More visualizations: role-wise stats, median vs mean salaries
* Integration with real placement data
* Deployment on cloud (Heroku/Render)

---

## 📝 License

MIT License — feel free to use and modify.

---

👨‍💻 Created by **Mohammad Enayatullah Safwan**
🌟 If you like this project, don't forget to star ⭐ the repo!

```

---

Would you also like me to generate a **`.gitignore` file** (Python + venv + VSCode) and a **ready-to-use first commit message** so you can initialize and push this repo quickly?
```
