from taipy.gui import Gui
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

# ========== KPI:er från data/  ==========
def compute_kpis(data_dir: str = "data"):
    base = Path(data_dir)
    if not base.exists():
        return 0, 0, "—"

    total_rows = 0
    course_set = set()
    latest_ts = 0

    # Tillåtna filtyper
    exts = {".csv", ".parquet", ".pq", ".feather", ".xlsx", ".xls"}
    course_cols = {"course", "kurs", "utbildning", "utbildningsnamn",
                   "program", "course_name", "kursnamn", "utbildningsnamn_kort"}

    files = [p for p in base.rglob("*") if p.suffix.lower() in exts]

    for f in files:
        try:
            # uppdaterad tid
            latest_ts = max(latest_ts, f.stat().st_mtime)

            if f.suffix.lower() == ".csv":
                df = pd.read_csv(f)
            elif f.suffix.lower() in {".parquet", ".pq", ".feather"}:
                df = pd.read_parquet(f)
            elif f.suffix.lower() in {".xlsx", ".xls"}:
                df = pd.read_excel(f)
            else:
                continue

            # summera rader
            total_rows += len(df)

            # hitta ev. kolumn som beskriver kurs/utbildning
            cols_lower = {c.lower(): c for c in df.columns}
            hit = next((cols_lower[c] for c in cols_lower.keys() if c in course_cols), None)
            if hit is not None:
                # unika kursnamn
                course_set.update(x for x in df[hit].dropna().astype(str).str.strip() if x)

        except Exception:
            # hoppa över konstiga filer – fortsätt
            continue

    last_update = "—" if latest_ts == 0 else datetime.fromtimestamp(latest_ts).strftime("%Y-%m-%d")
    return total_rows, len(course_set), last_update

# Beräkna KPI vid start
total_applications, num_courses, last_update = compute_kpis("data")

# ========== Sidor ==========
from frontend.pages.utbildningsomrade import utbildningsomrade
from frontend.pages.statistikansökningar import ansökningar
from frontend.pages.demografi import gender_age
from frontend.pages.home import home_page
from frontend.pages.anordnare import anordnare
from frontend.pages.karta import map_page

pages = {
    "Home": home_page,
    "Karta": map_page,
    "Kursansökningar": ansökningar,
    "Utbildningsområden": utbildningsomrade,
    "Anordnare": anordnare,
    "Demografi": gender_age,
}

# ========== Start ==========
if __name__ == "__main__":
    gui = Gui(pages=pages, css_file="assets/main.css")
    gui.run(dark_mode=False, use_reloader=False, port="auto")
