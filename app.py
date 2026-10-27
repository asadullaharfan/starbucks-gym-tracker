import streamlit as st
import joblib
import pandas as pd

st.title("Starbucks Calories Predictor")
st.write("Nutrition values enter karein, phir Predict dabayein.")

@st.cache_resource
def load_model():
    return joblib.load("starbucks_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"Model load nahi hua: {e}")
    st.stop()

# Kaggle ke feature names bilkul waise hi, spaces samet
FEATURES = [
    "Trans Fat (g) ",
    "Saturated Fat (g)",
    " Sodium (mg)",
    " Total Carbohydrates (g) ",
    "Cholesterol (mg)",
    " Dietary Fibre (g)",
    " Sugars (g)",
    " Protein (g) "
]

with st.form("calorie_form"):
    col1, col2 = st.columns(2)

    with col1:
        trans_fat = st.number_input("Trans Fat (g)", min_value=0.0, value=0.0, step=0.1)
        saturated_fat = st.number_input("Saturated Fat (g)", min_value=0.0, value=0.0, step=0.1)
        sodium = st.number_input("Sodium (mg)", min_value=0.0, value=0.0, step=1.0)
        carbohydrates = st.number_input("Total Carbohydrates (g)", min_value=0.0, value=0.0, step=1.0)

    with col2:
        cholesterol = st.number_input("Cholesterol (mg)", min_value=0.0, value=0.0, step=1.0)
        fibre = st.number_input("Dietary Fibre (g)", min_value=0.0, value=0.0, step=0.1)
        sugars = st.number_input("Sugars (g)", min_value=0.0, value=0.0, step=1.0)
        protein = st.number_input("Protein (g)", min_value=0.0, value=0.0, step=0.1)

    predict_button = st.form_submit_button("Predict Calories")

if predict_button:
    values = [
        trans_fat,
        saturated_fat,
        sodium,
        carbohydrates,
        cholesterol,
        fibre,
        sugars,
        protein
    ]

    input_data = pd.DataFrame([values], columns=FEATURES)

    # Model ke trained columns ka order use karein
    expected_features = getattr(model, "feature_names_in_", None)

    if expected_features is not None:
        expected_features = list(expected_features)

        if set(expected_features) != set(FEATURES):
            st.error(f"Model ke expected feature names: {expected_features}")
            st.stop()

        input_data = input_data.reindex(columns=expected_features)

    try:
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Calories: {float(prediction):.1f} kcal")
    except Exception as e:
        st.error(f"Prediction nahi ho saki: {e}")
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Gym Nutrition Tracker", page_icon="💪", layout="wide")

st.title("💪 Gym Nutrition Tracker")
st.caption("Search foods, estimate nutrition by grams, and track your daily intake.")

@st.cache_data
def load_foods():
    return pd.read_csv("foods.csv")

try:
    foods = load_foods()
except Exception as e:
    st.error("Could not load foods.csv. Keep foods.csv in the same folder as app.py.")
    st.stop()

if "food_log" not in st.session_state:
    st.session_state.food_log = []

with st.sidebar:
    st.header("🎯 Daily goals (optional)")
    goal_cal = st.number_input("Calories goal (kcal)", min_value=0, max_value=10000, value=2400, step=100)
    goal_protein = st.number_input("Protein goal (g)", min_value=0, max_value=500, value=140, step=5)
    goal_carbs = st.number_input("Carbs goal (g)", min_value=0, max_value=1000, value=280, step=10)
    goal_fat = st.number_input("Fat goal (g)", min_value=0, max_value=400, value=75, step=5)
    st.caption("Goals are optional estimates, not medical advice. Choose goals suitable for you.")

tab_add, tab_dashboard, tab_log, tab_foods = st.tabs(
    ["➕ Add food", "📊 Daily dashboard", "🧾 Food log", "🥗 Food database"]
)

with tab_add:
    st.subheader("Add food to today's log")
    search = st.text_input("Search food", placeholder="e.g. chicken, oats, roti, banana")
    categories = ["All"] + sorted(foods["category"].dropna().unique().tolist())
    category = st.selectbox("Category", categories)
    filtered = foods.copy()
    if search.strip():
        filtered = filtered[filtered["food"].str.contains(search.strip(), case=False, na=False)]
    if category != "All":
        filtered = filtered[filtered["category"] == category]

    if filtered.empty:
        st.warning("No matching food found. Try another name or category.")
    else:
        chosen = st.selectbox("Choose food", filtered["food"].tolist())
        food_row = foods[foods["food"] == chosen].iloc[0]
        grams = st.number_input("Amount (grams)", min_value=1, max_value=3000, value=100, step=10)
        factor = grams / 100
        values = {
            "Calories": food_row["calories_kcal"] * factor,
            "Protein (g)": food_row["protein_g"] * factor,
            "Carbs (g)": food_row["carbs_g"] * factor,
            "Fat (g)": food_row["fat_g"] * factor,
            "Fibre (g)": food_row["fibre_g"] * factor,
        }
        st.caption("Estimated nutrition for this serving:")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Calories", f'{values["Calories"]:.0f} kcal')
        m2.metric("Protein", f'{values["Protein (g)"]:.1f} g')
        m3.metric("Carbs", f'{values["Carbs (g)"]:.1f} g')
        m4.metric("Fat", f'{values["Fat (g)"]:.1f} g')
        m5.metric("Fibre", f'{values["Fibre (g)"]:.1f} g')
        meal = st.selectbox("Meal", ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-workout", "Post-workout"])
        if st.button("Add to daily log", type="primary"):
            st.session_state.food_log.append({
                "date": str(date.today()),
                "meal": meal,
                "food": chosen,
                "grams": int(grams),
                "calories_kcal": round(values["Calories"], 1),
                "protein_g": round(values["Protein (g)"], 1),
                "carbs_g": round(values["Carbs (g)"], 1),
                "fat_g": round(values["Fat (g)"], 1),
                "fibre_g": round(values["Fibre (g)"], 1),
            })
            st.success(f"Added {grams} g of {chosen} to your log.")

with tab_dashboard:
    st.subheader(f"Nutrition dashboard — {date.today().strftime('%d %b %Y')}")
    log = pd.DataFrame(st.session_state.food_log)
    if not log.empty:
        today_log = log[log["date"] == str(date.today())].copy()
    else:
        today_log = pd.DataFrame()

    if today_log.empty:
        st.info("Your log is empty. Use the Add food tab to record what you eat.")
        totals = {"calories_kcal": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fibre_g": 0}
    else:
        totals = today_log[["calories_kcal","protein_g","carbs_g","fat_g","fibre_g"]].sum().to_dict()

    a,b,c,d,e = st.columns(5)
    a.metric("Calories", f'{totals["calories_kcal"]:.0f} kcal', f'Goal {goal_cal} kcal')
    b.metric("Protein", f'{totals["protein_g"]:.1f} g', f'Goal {goal_protein} g')
    c.metric("Carbs", f'{totals["carbs_g"]:.1f} g', f'Goal {goal_carbs} g')
    d.metric("Fat", f'{totals["fat_g"]:.1f} g', f'Goal {goal_fat} g')
    e.metric("Fibre", f'{totals["fibre_g"]:.1f} g')

    goal_data = pd.DataFrame({
        "Nutrient": ["Calories (kcal)", "Protein (g)", "Carbs (g)", "Fat (g)"],
        "Consumed": [totals["calories_kcal"], totals["protein_g"], totals["carbs_g"], totals["fat_g"]],
        "Goal": [goal_cal, goal_protein, goal_carbs, goal_fat],
    })
    st.plotly_chart(px.bar(goal_data, x="Nutrient", y=["Consumed", "Goal"], barmode="group",
                           title="Today's intake vs goals"), use_container_width=True)

    if not today_log.empty:
        nutrient = st.selectbox("Chart nutrient", ["calories_kcal", "protein_g", "carbs_g", "fat_g", "fibre_g"])
        st.plotly_chart(px.bar(today_log, x="food", y=nutrient, color="meal",
                               title=f"{nutrient.replace('_',' ').title()} by food"), use_container_width=True)
        st.dataframe(today_log, use_container_width=True, hide_index=True)

with tab_log:
    st.subheader("Food log")
    log = pd.DataFrame(st.session_state.food_log)
    if log.empty:
        st.info("No foods recorded yet.")
    else:
        st.dataframe(log, use_container_width=True, hide_index=True)
        csv_data = log.to_csv(index=False).encode("utf-8")
        st.download_button("Download food log as CSV", data=csv_data,
                           file_name="gym_food_log.csv", mime="text/csv")
        if st.button("Clear all logged foods"):
            st.session_state.food_log = []
            st.rerun()
    st.caption("This starter version stores entries in the current app session. Download the CSV before closing if you want to keep a copy.")

with tab_foods:
    st.subheader("Food database — nutrition per 100 g")
    st.caption("Values are approximate. Recipes, brands, cooking methods, oil, and portion sizes change nutrition.")
    st.dataframe(foods, use_container_width=True, hide_index=True)
    st.download_button("Download foods.csv", data=foods.to_csv(index=False).encode("utf-8"),
                       file_name="foods.csv", mime="text/csv")

st.divider()
st.caption("Use food labels or a reliable nutrition source for more accurate values. This app is for general tracking and does not provide medical advice.")
