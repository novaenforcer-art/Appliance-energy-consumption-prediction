import streamlit as st
import pandas as pd
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define SCOPES and credentials file
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDS_FILE = 'D:/py projects/Appliance energy prediction/client_secret_1018041509959-jh6cq471ag4coeeic6srjgm1hpfbtfu9.apps.googleusercontent.com.json'  # Path to your credentials file

# Function to authenticate and create Google Drive service
def authenticate_google_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDS_FILE, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

# Function to download and load model from Google Drive
def load_model_from_drive(file_id):
    service = authenticate_google_drive()
    request = service.files().get_media(fileId=file_id)
    file = request.execute()
    # Load the model using appropriate method (e.g., pickle)
    model = pickle.loads(file)
    return model

# Define your Google Drive file ID for the model
MODEL_FILE_ID = '1I5_hsndPNdNfyfMSNeYZAeeEVD6vFxAM'  # Replace 'YOUR_FILE_ID' with the actual file ID

# Load the model from Google Drive
model = load_model_from_drive(MODEL_FILE_ID)

# Function to predict
def predict(appliances, hu_build_out, windspeed, tdewpoint, month, weekday, hour, humidity_difference):
    data = {'hu_build_out': [hu_build_out],
            'Windspeed': [windspeed],
            'Tdewpoint': [tdewpoint],
            'month': [month],
            'weekday': [weekday],
            'hour': [hour],
            'Humidity_difference': [humidity_difference]}
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return prediction

# Streamlit app
def main():
    st.title('Appliances Energy Prediction')

    # Input fields
    humidity = st.number_input('Humidity', format="%.6f", value=0.0)
    windspeed = st.number_input('Windspeed', format="%.6f", value=0.0)
    tdewpoint = st.number_input('Tdewpoint', format="%.6f", value=0.0)
    month = st.number_input('Month', min_value=0.0, max_value=12.0, value=0.0, step=0.01, format="%.2f")
    weekday = st.number_input('Weekday', min_value=0.0, max_value=6.0, value=0.0, format="%.6f")
    hour = st.number_input('Hour', min_value=0.0, max_value=23.0, value=0.0, format="%.6f")
    humidity_difference = st.number_input('Humidity Difference', format="%.6f", value=0.0)

    # Predict button
    if st.button('Predict'):
        prediction = predict('Appliances', humidity, windspeed, tdewpoint, month, weekday, hour, humidity_difference)
        st.success(f'Predicted Appliances value: {prediction}')

if __name__ == '__main__':
    main()