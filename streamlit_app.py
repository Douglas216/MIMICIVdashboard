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
    admissions["marital_status"] = (
        admissions["marital_status"]
        .fillna("Unknown")
        .replace({"?": "Unknown", "": "Unknown"})
    )
    return admissions


admissions = load_admissions()


# -----------------------------------------------------------
# Race distribution
# -----------------------------------------------------------
st.write("### Race")

# Altair bar chart directly from the simplified column
chart = (
    alt.Chart(admissions)
    .mark_bar()
    .encode(
        x=alt.X(
            "race_simplified:N",
            sort=["White", "Black", "Hispanic / Latino", "Other / Unknown"],
            title="Race",
            axis=alt.Axis(labelAngle=0),
        ),
        y=alt.Y("count():Q", title="Number of Admissions"),
        color=alt.Color("race_simplified:N", legend=None),
        tooltip=[alt.Tooltip("race_simplified:N", title="Race"), alt.Tooltip("count():Q", title="Count")],
    )
)

st.altair_chart(chart, use_container_width=True)


# -----------------------------------------------------------
# Additional categorical bar charts
# -----------------------------------------------------------
def categorical_bar(df, column, title):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(f"{column}:N", sort="-y", title=title, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("count():Q", title="Number of Admissions"),
            color=alt.Color(f"{column}:N", legend=None),
            tooltip=[
                alt.Tooltip(f"{column}:N", title=title),
                alt.Tooltip("count():Q", title="Count"),
            ],
        )
    )
    st.altair_chart(chart, use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    st.write("### Insurance")
    categorical_bar(admissions, "insurance", "Insurance")

with col2:
    st.write("### Marital Status")
    categorical_bar(admissions, "marital_status", "Marital Status")
