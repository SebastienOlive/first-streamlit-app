import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("My First Streamlit App")

vTextToStream = "This text here will be as type written using this amazing Streamlit which I just discover yesterday evening!"

def stream_data():
    for word in vTextToStream.split(" "):
        yield word + " "
        time.sleep(0.05)

if st.button('Write text'):
    st.write_stream(stream_data)

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 15,000 rows of data into the dataframe.
data = load_data(15000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done! (using st.cache_data)')

hist_values = np.histogram(data[DATE_COLUMN].dt.hour,bins=24,range=(0,24))[0]

if st.checkbox('Show raw data'):
    st.subheader("Raw data")
    st.write(data)
    st.subheader("Pickups by hour")
    st.write(hist_values)

st.subheader("The histogram now!")
st.bar_chart(hist_values)

st.subheader("Locatioons of the pickups")

#Zoom required
vZoom=st.slider('Zoom map',1,20,8)
vHour = st.slider('Hour',0,23,17)

st.subheader(f'Pickups made at {vHour}')

filtered_data = data[data[DATE_COLUMN].dt.hour == vHour]
st.map(filtered_data,zoom=vZoom)