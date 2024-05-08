import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Example data creation
def create_data():
    # Data with city names, coordinates, and hypothetical transport cost and lead time
    data = pd.DataFrame({
        'City': ['Hanoi', 'Ho Chi Minh City', 'Da Nang', 'Hai Phong', 'Can Tho'],
        'Latitude': [21.0285, 10.7626, 16.0544, 20.8449, 10.0452],
        'Longitude': [105.8544, 106.6297, 108.2022, 106.6881, 105.7469],
        'Transport_Cost': [1000, 1200, 1100, 1050, 1150],  # Hypothetical costs in USD
        'Lead_Time': [24, 18, 20, 22, 19]  # Hypothetical lead times in hours
    })
    return data

data = create_data()

# Sidebar for location selection
st.sidebar.header('Location Selector')
option = st.sidebar.selectbox('Select a location:', data['City'])

# Filter data based on selection
selected_location = data[data['City'] == option]

# Display the map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=selected_location['Latitude'].iloc[0],
        longitude=selected_location['Longitude'].iloc[0],
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=data,
            get_position='[Longitude, Latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=20000,
        ),
    ],
))

# Dynamic cost and lead time calculations
st.header('Cost and Lead Time Calculations')
if st.button('Recalculate Costs and Lead Time'):
    # Example of how real calculations might be performed
    transport_cost = np.random.normal(1, 0.1) * selected_location['Transport_Cost'].iloc[0]  # Simulated variability
    lead_time = np.random.normal(1, 0.05) * selected_location['Lead_Time'].iloc[0]  # Simulated variability

    st.subheader(f"Total Cost for Warehouse and Transportation: ${transport_cost:,.2f}")
    st.subheader(f"Average Lead Time: {lead_time:.2f} hours")

