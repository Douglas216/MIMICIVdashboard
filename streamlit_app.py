import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------------------------------------
# Page settings
# -----------------------------------------------------------
st.set_page_config(page_title="MIMIC-IV Demo Dashboard", layout="wide")

st.title("MIMIC-IV Demo Dashboard")


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

    def simplify_admission_location(x):
        if pd.isna(x):
            return "Unknown"

        x = str(x).upper()

        if "EMERGENCY" in x:
            return "Emergency"
        if any(keyword in x for keyword in ["REFERRAL", "WALK-IN", "SELF", "PROCEDURE"]):
            return "Referral"
        if "TRANSFER" in x:
            return "Transfer"
        if "PACU" in x:
            return "PACU"
        return "Unknown"

    admissions["admission_loc_simple"] = admissions["admission_location"].apply(
        simplify_admission_location
    )
    return admissions


admissions = load_admissions()


# -----------------------------------------------------------
# Helper for categorical bar charts
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
    st.write("#### Race")
    race_chart = (
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
            tooltip=[
                alt.Tooltip("race_simplified:N", title="Race"),
                alt.Tooltip("count():Q", title="Count"),
            ],
        )
    )
    st.altair_chart(race_chart, use_container_width=True)

with col2:
    st.write("#### Admission Location")
    categorical_bar(admissions, "admission_loc_simple", "Admission Location")

col3, col4 = st.columns(2)

with col3:
    st.write("### Insurance")
    categorical_bar(admissions, "insurance", "Insurance")

with col4:
    st.write("### Marital Status")
    categorical_bar(admissions, "marital_status", "Marital Status")
