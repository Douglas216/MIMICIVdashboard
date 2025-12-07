import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------------------------------------
# Page settings
# -----------------------------------------------------------
st.set_page_config(page_title="MIMIC-IV Demo Dashboard", layout="wide")

st.title("MIMIC-IV Demo Dashboard")
st.subheader("Racial Distribution of Hospital Admissions (Demo Dataset)")


# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------
@st.cache_data
def load_admissions():
    # CSV path is relative to the repo root
    admissions = pd.read_csv("data/admissions.csv")

    # Simplify race categories
    def simplify_race(x):
        x = str(x).upper()

        if "HISPANIC" in x or "LATINO" in x:
            return "Hispanic / Latino"
        if "BLACK" in x:
            return "Black"
        if "WHITE" in x or x in ["PORTUGUESE"]:
            return "White"
        return "Other / Unknown"

    admissions["race_simplified"] = admissions["race"].apply(simplify_race)
    return admissions


admissions = load_admissions()


# -----------------------------------------------------------
# Race distribution
# -----------------------------------------------------------
st.write("### Simplified Race Distribution")

# Build counts table
race_counts = (
    admissions["race_simplified"]
    .value_counts()
    .reset_index(name="Count")      # count column
    .rename(columns={"index": "Race"})  # label column
)

# (Optional) debug print – safe to keep or remove later
st.write("Race counts dataframe:")
st.write(race_counts)
st.write("Columns:", race_counts.columns.tolist())
st.write("Number of rows:", len(race_counts))

# Altair bar chart
chart = (
    alt.Chart(race_counts)
    .mark_bar()
    .encode(
        x=alt.X("Race:N", sort="-y", title="Race"),
        y=alt.Y("Count:Q", title="Number of Admissions"),
        color=alt.Color("Race:N", legend=None),
        tooltip=["Race", "Count"],
    )
)

st.altair_chart(chart, use_container_width=True)

# Show numeric table
st.write("### Table of Counts")
st.dataframe(race_counts)
