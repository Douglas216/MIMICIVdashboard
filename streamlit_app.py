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
    admissions = pd.read_csv('admissions.csv')

    # Function to simplify race
    def simplify_race(x):
        x = str(x).upper()

        # Hispanic / Latino
        if "HISPANIC" in x or "LATINO" in x:
            return "Hispanic / Latino"

        # Black
        if "BLACK" in x:
            return "Black"

        # White
        if "WHITE" in x or x in ["PORTUGUESE"]:
            return "White"

        # Other / Unknown
        return "Other / Unknown"

    # Apply mapping
    admissions["race_simplified"] = admissions["race"].apply(simplify_race)

    return admissions


admissions = load_admissions()


# -----------------------------------------------------------
# Visualization
# -----------------------------------------------------------
st.write("### Simplified Race Distribution")

race_counts = (
    admissions["race_simplified"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "Race", "race_simplified": "Count"})
)

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
    .properties(width=600, height=400)
)

st.altair_chart(chart, use_container_width=True)

# Display numeric counts
st.write("### Table of Counts")
st.dataframe(race_counts)
