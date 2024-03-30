import streamlit as st
import pandas as pd
import pickle

# Load the pre-trained model
with open('finalized_model.sav', 'rb') as file:
    model = pickle.load(file)


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