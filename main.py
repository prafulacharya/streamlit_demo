import streamlit as st


st.set_page_config(page_title="Demand Volatility - Supply Chain", layout="wide")

st.title("Demand Volatility Inputs for Supply Chain")
st.markdown("Enter your parameters below to trigger the Databricks notebook.")

with st.form("volatility_form"):
    with st.expander("🔧 Configuration Inputs", expanded=True):
        num_comparison_runs = st.slider("Number of Comparison Runs", 1, 100, 5)

        st.subheader("⚖️ Weights (0 to 1)")

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

        selected_reference_run = st.slider("Select Reference Run", 1, 100, 10)

    submit = st.form_submit_button("Run")

if submit:
    user_input = {
        "num_comparison_runs": num_comparison_runs,
        **weights,
        "selected_reference_run": selected_reference_run
    }
    msg, result = trigger_notebook(user_input)
    st.success(msg)
    st.json(result)
