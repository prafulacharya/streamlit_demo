import requests
import json
import uuid

import os

from dotenv import load_dotenv



# --- Load environment variables from .env ---
load_dotenv()

# --- Now read values ---
DATABRICKS_INSTANCE = os.getenv("DATABRICKS_INSTANCE")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_JOB_ID = os.getenv("DATABRICKS_JOB_ID") 


def trigger_notebook(user_input: dict):
    try:
        # Create idempotency token (to avoid duplicate runs)
        idempotency_token = str(uuid.uuid4())

        # Prepare request headers
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }

        # Build the payload
        payload = {
            "job_id": DATABRICKS_JOB_ID,
            "idempotency_token": idempotency_token,
            "notebook_params": user_input  # Pass user input directly to the notebook
        }

        # Send POST request to Databricks API
        response = requests.post(
            f"{DATABRICKS_INSTANCE}/api/2.2/jobs/run-now",
            headers=headers,
            data=json.dumps(payload)
        )

        # Check response
        if response.status_code == 200:
            result = response.json()
            return "Successfully triggered the Databricks notebook!", result
        else:
            return f"Failed to trigger notebook. Status Code: {response.status_code}", response.text

    except Exception as e:
        return f"Error occurred: {str(e)}", {}
