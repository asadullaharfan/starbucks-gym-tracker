# Gym Nutrition Tracker

A beginner-friendly Streamlit app for gym users. Includes food search, nutrition estimates per serving, a daily food log, nutrition goals, charts, and CSV export.

## Files
- `app.py` — Streamlit app
- `foods.csv` — starter food nutrition dataset (approximate values per 100 g)
- `requirements.txt` — Python dependencies

## Run on Windows
1. Put all three files in the same folder.
2. Open that folder in File Explorer.
3. Click the address bar, type `cmd`, and press Enter.
4. Run:
   `python -m pip install -r requirements.txt`
5. Then run:
   `python -m streamlit run app.py`
6. Open the local URL shown, usually `http://localhost:8501`.

## Publish online
Upload `app.py`, `foods.csv`, and `requirements.txt` to a GitHub repository. In Streamlit Community Cloud, create a new app, choose that repository, and set the main file path to `app.py`.

## Important
Nutrition values are estimates per 100 g and can differ by recipe, brand, cooking method, and portion. Food log is kept in the current session; download it as CSV before closing if you need a copy. This is a general tracking tool, not medical advice.
