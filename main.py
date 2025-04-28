import streamlit as st
from trigger import trigger_notebook

st.set_page_config(page_title="Demand Volatility", layout="wide")

st.title("Demand Volatility")
st.markdown("Configure your parameters below to run the business logic")

with st.form("volatility_form"):
    with st.expander("Configuration Attributes", expanded=True):
        num_comparison_runs = st.number_input(
            "Number of Comparison Runs", 
            min_value=1, 
            max_value=100, 
            value=5, 
            step=1
        )

        cols = st.columns(5)
        weights = {}
        for i in range(1, 11):
            with cols[(i-1) % 5]:
                weights[f"weight_{i}"] = st.number_input(
                    f"Weight {i}", 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=0.2, 
                    step=0.01, 
                    format="%.2f"
                )

        selected_reference_run = st.number_input(
            "Select Reference Run", 
            min_value=1, 
            max_value=100, 
            value=10, 
            step=1
        )

    submit = st.form_submit_button("Run")

if submit:
    user_input = {
        "num_comparison_runs": num_comparison_runs,
        **weights,
        "selected_reference_run": selected_reference_run
    }

    # --- Trigger Databricks function (assumed ready) ---
    msg, result = trigger_notebook(user_input)

    st.success(msg)
    st.json(result)
