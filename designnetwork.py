import streamlit as st
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Function to geocode using Nominatim
def geocode_province(province):
    geolocator = Nominatim(user_agent="geoapiExercises")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geocode(f"{province}, Vietnam")
    if location:
        return location.latitude, location.longitude
    return None, None

# Function to load data and add geocode if necessary
def load_data():
    data = pd.read_excel('D:/SCM/Supply Chain/Competition/SCMission 2024/Round 3/Visualization Design Network.xlsx')
    # Check if latitude and longitude columns exist
    if 'latitude' not in data.columns or 'longitude' not in data.columns:
        # Apply geocoding if latitude and longitude are not present
        data[['latitude', 'longitude']] = data['Province'].apply(
            lambda x: pd.Series(geocode_province(x))
        )
    return data

# Function to create a map using Pydeck
def create_map(data, latitude, longitude):
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=6,
        pitch=0)
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        data,
        get_position=['longitude', 'latitude'],
        get_color='[200, 30, 0, 160]',
        get_radius=10000,
    )
    
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer]
    )

def main():
    st.title('Warehouse Placement Scenarios Visualization')
    
    # Load your data
    data = load_data()
    
    # Calculate average latitude and longitude for the initial map centering
    avg_lat = data['latitude'].mean()
    avg_lon = data['longitude'].mean()
    
    # Create a map
    map_fig = create_map(data, avg_lat, avg_lon)
    
    # Display the map
    st.pydeck_chart(map_fig)

if __name__ == "__main__":
    main()
