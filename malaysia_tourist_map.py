import csv
import folium
import streamlit as st
from streamlit_folium import st_folium

# Function to generate a CSV file
def generate_malaysia_tourist_attractions_csv(filename, data):
    """
    Generate a CSV file containing popular tourist attractions in Malaysia.

    :param filename: Name of the CSV file to be created.
    :param data: List of dictionaries, each containing 'name', 'latitude', 'longitude', 'description', and 'type'.
    """
    headers = ['Name', 'Latitude', 'Longitude', 'Description', 'Type']

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow({
                'Name': row['name'],
                'Latitude': row['latitude'],
                'Longitude': row['longitude'],
                'Description': row['description'],
                'Type': row['type']
            })

# Function to create an interactive map
def create_interactive_map(data):
    """
    Create an interactive map.

    :param data: List of dictionaries containing 'name', 'latitude', 'longitude', 'description', and 'type'.
    """
    # Initialize the map centered at Malaysia
    malaysia_map = folium.Map(location=[4.2105, 101.9758], zoom_start=6)

    # Define marker colors for different types of attractions
    marker_colors = {
        'Historical Site': 'red',
        'Natural Wonder': 'green',
        'Amusement Park': 'blue'
    }

    # Create feature groups for each type of attraction
    feature_groups = {attraction_type: folium.FeatureGroup(name=attraction_type) for attraction_type in marker_colors.keys()}

    # Add markers for each attraction
    for attraction in data:
        color = marker_colors.get(attraction['type'], 'gray')  # Default to gray if type is unknown
        marker = folium.Marker(
            location=[attraction['latitude'], attraction['longitude']],
            popup=f"<b>{attraction['name']}</b><br>{attraction['description']}",
            icon=folium.Icon(color=color, icon='info-sign')
        )
        feature_groups[attraction['type']].add_child(marker)

    # Add feature groups to the map
    for group in feature_groups.values():
        group.add_to(malaysia_map)

    # Add layer control
    folium.LayerControl().add_to(malaysia_map)

    # Add a marker with the total number of attractions
    total_attractions = len(data)
    folium.Marker(
        location=[4.2105, 101.9758],
        popup=f"<b>Total Attractions:</b> {total_attractions}",
        icon=folium.Icon(color="darkblue", icon="info-sign")
    ).add_to(malaysia_map)

    return malaysia_map

# Data for popular tourist attractions in Malaysia
malaysia_tourist_attractions = [
    {
        'name': 'Petronas Twin Towers',
        'latitude': 3.1579,
        'longitude': 101.7118,
        'description': 'Iconic twin skyscrapers in Kuala Lumpur, a must-visit landmark in Malaysia.',
        'type': 'Historical Site'
    },
    {
        'name': 'Batu Caves',
        'latitude': 3.2370,
        'longitude': 101.6832,
        'description': 'A limestone hill with caves and Hindu temples, featuring a giant Lord Murugan statue.',
        'type': 'Historical Site'
    },
    {
        'name': 'Langkawi Sky Bridge',
        'latitude': 6.3742,
        'longitude': 99.6653,
        'description': 'A curved pedestrian bridge above Langkawi Island, offering stunning views.',
        'type': 'Natural Wonder'
    },
    {
        'name': 'Penang Hill',
        'latitude': 5.4226,
        'longitude': 100.2767,
        'description': 'A hill resort with a funicular train, offering panoramic views of Penang.',
        'type': 'Natural Wonder'
    },
    {
        'name': 'Taman Negara',
        'latitude': 4.7109,
        'longitude': 102.4070,
        'description': 'One of the world’s oldest tropical rainforests, popular for trekking and wildlife watching.',
        'type': 'Natural Wonder'
    },
    {
        'name': 'Sunway Lagoon',
        'latitude': 3.0731,
        'longitude': 101.6073,
        'description': 'A famous amusement park in Selangor offering thrilling rides and water attractions.',
        'type': 'Amusement Park'
    }
]

# Save data to a CSV file
csv_filename = 'malaysia_tourist_attractions.csv'
generate_malaysia_tourist_attractions_csv(csv_filename, malaysia_tourist_attractions)

# Streamlit App
st.title("Malaysia Tourist Attractions Map")
st.write("Explore the tourist attractions across Malaysia. Each marker provides details about the attraction.")

# Display the CSV download link
with open(csv_filename, "rb") as file:
    st.download_button(
        label="Download Attractions CSV",
        data=file,
        file_name=csv_filename,
        mime="text/csv"
    )

# Create and display the map
map_display = create_interactive_map(malaysia_tourist_attractions)
st_folium(map_display, width=700, height=500)
