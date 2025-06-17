
# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
import requests
import os
import streamlit as st
from dotenv import load_dotenv
import json


load_dotenv()
APPLICATION_TOKEN = os.environ.get("APP_TOKEN") 


def run_flow(message: str) -> dict:
    
    url = f"https://api.langflow.astra.datastax.com/lf/07171a34-fc60-4dfd-973f-94cb3d6c487e/api/v1/run/1e6bdb8b-79dc-4e4a-89da-911b0c4de9ad"
    
    payload = {
    "input_value": message,  # The input value to be processed by the flow
    "output_type": "chat",  # Specifies the expected output format
    "input_type": "chat"  # Specifies the input format
    }
    
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {APPLICATION_TOKEN}"  # Authentication key from environment variable'}
    }
    
    try:
        # Send API request
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except ValueError as e:
        print(f"Error parsing response: {e}")

def main():
    st.title("Chat Interface")
    
    message = st.text_area("Message", placeholder="Ask something...")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
