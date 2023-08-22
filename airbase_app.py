import folium as fo
from folium import Choropleth
from folium.plugins import HeatMap
import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit as st
from streamlit_folium import st_folium, folium_static
from folium import plugins
from folium.plugins import MousePosition, MeasureControl
from shapely.geometry import Polygon, LineString
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely import wkt
from data_loader import *
from airbase_funcs import *

# The title of the page
APP_Title = "_Airbase Dashboard_"

def main():
    
    st.set_page_config(APP_Title, layout="wide")
    #st.title(APP_Title)
    file = "natocsv2.csv"
    nato = pd.read_csv("natocsv2.csv")
    

    # Reading in the sampled airport data:
    #airports = pd.read_csv('Sample_data.csv')
    with st.sidebar.expander("Uploaded Files"):
        st.markdown("Upload Blue Airport Data:")
        blue_ports = upload_airports()
        st.markdown("Upload Blue Aircraft Data:")
        blue_aircrafts = upload_aircraft_ranges()
        st.markdown("Upload Red Airport Data:")
        rus_airports = upload_red_airports()
        st.markdown("Upload Red Aircraft Data")
        rus_aircrafts = upload_red_aircraft_ranges()

        
        

        
        # Keeping the persistence of the blue data:
        if blue_ports is not None and 'airports_loaded' not in st.session_state:
            st.session_state.airport_data = blue_ports
            st.session_state.airports_loaded = True
            
        elif 'airport_data' in st.session_state:
            blue_ports = st.session_state.airport_data
            
        
        # Keeping the persistence of the red data:
        if rus_airports is not None and 'rus_airports_loaded' not in st.session_state:
            st.session_state.rus_airport_data = rus_airports
            st.session_state.rus_airports_loaded = True
        elif 'rus_airport_data' in st.session_state:
            rus_airports = st.session_state.rus_airport_data
        
        
        
        # Keeping the persistence of the blue aircraft data:
        if blue_aircrafts is not None and 'range_data' not in st.session_state:
            st.session_state.range_data = blue_aircrafts
            st.session_state.ranges = True
        elif 'range_data' in st.session_state:
            blue_aircrafts = st.session_state.range_data
        # Keeping the persistence of the red aircraft data:
        if rus_aircrafts is not None and 'rus_range_data' not in st.session_state:
            st.session_state.rus_range_data = rus_aircrafts
            st.session_state.rus_ranges = True
        elif 'rus_range_data' in st.session_state:
            rus_aircrafts = st.session_state.rus_range_data
        
    
    
        
    
        # Reading in the aircraft ranges:
        
    
    # The folium base map:
    #eu = fo.Map(location=[50,20], zoom_start=3.5, scrollWheelZoom=False, tiles = 'cartodbpositron')
   
    # Checking if the files have been uploaded:
    if blue_ports is not None and blue_aircrafts is not None and rus_airports is not None and rus_aircrafts is not None:


        st.sidebar.header("**_Team to Add or Subtract_**")
        # Dropdown for Blue or Red:
        chosen_color = st.sidebar.selectbox("Choose :blue[Blue] or :red[Red]:", ["Blue", "Red"])

        st.sidebar.header("**_View Selections_**")
        # Dropdown for list of aircrafts:
        aircraft_list = list(blue_aircrafts['Aircraft'].unique())
        aircraft_list.sort()
        chosen_type = st.sidebar.multiselect("Choose Blue Aircraft Type:",
                                            aircraft_list)
        
        # Dropdown for Group Filter:
        group_list = list(blue_ports['Group'].unique())
        group_list.sort()
        group_list.append("All")
        chosen_group = st.sidebar.multiselect("Choose Blue Group Number:",
                                              group_list, default="All")


        # Dropdown for Red Aircraft:
        red_aircrafts = list(rus_aircrafts["Aircraft"])
        red_aircrafts.sort()
        chosen_red_aircraft = st.sidebar.multiselect("Choose Red Aircraft Type:",
                                                     red_aircrafts)
        
        


      
        eu = fo.Map(location=[50,20], zoom_start=3.5, scrollWheelZoom=False, tiles = 'cartodbpositron')
        
        
        grid = make_grid()
       

       
        
        # Changing the title for additions based on choice of red or blue:
        
        #if chosen_color == "Blue":
         #   st.subheader("Add or Subtract Aircrafts for :blue[Blue]")
        #else:
        #    st.subheader("Add or Subtract Aircrafts for :red[Red]")
        # Separating the dropdown widgets into columns:
        
        
        with st.expander("Add to Airports"):
            # First column for choosing airport or grid number:
            with st.form('airports'):
                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    if chosen_color == "Blue":
                        # Add to airport option:
                        airport_names = list(blue_ports['name'])
                        airport_names.sort()
                        chosen_airport = st.selectbox("Choose Airport", airport_names)
                    else:
                        airport_names = list(rus_airports['name'])
                        airport_names.sort()
                        chosen_airport = st.selectbox("Choose Airport", airport_names)
                with col2:
                    if chosen_color == "Blue":
                        #Add aircraft option:
                        aircraft_list2 = list(blue_aircrafts['Aircraft'].unique())
                        chosen_type2 = st.selectbox("Aircraft To Add:",
                                                        aircraft_list2)
                    else:
                        #Add aircraft option:
                        aircraft_list2 = list(rus_aircrafts['Aircraft'].unique())
                        chosen_type2 = st.selectbox("Aircraft To Add:",
                                                    aircraft_list2)
                
                with col3:
                    # Number of aircraft to add:
                    add_subtract = st.selectbox("Add/Subtract:", ["Add", "Subtract"])
                # Amount of aircraft to add:
                with col4:
                    #Number of Aircraft to Subtract:
                    nums2 = list(range(0,11))
                    Amount = st.selectbox("Amount:", nums2)
                
                with col5:
                    st.write("")
                    st.write("")
                    # Submit button:
                    submit = st.form_submit_button("Submit")
                    if chosen_color == "Blue":
                        if add_subtract == "Add" and submit:
                            add_df(blue_ports, chosen_airport, chosen_type2, Amount)
                
                        elif add_subtract == "Subtract" and submit:
                            subtract_df(blue_ports, chosen_airport, chosen_type2, Amount)
                    else:
                        if add_subtract == "Add" and submit:
                            add_df(rus_airports, chosen_airport, chosen_type2, Amount)
                    
                        elif add_subtract == "Subtract" and submit:
                            subtract_df(rus_airports, chosen_airport, chosen_type2, Amount)

        with st.expander("Add to Grid Locations"):
            with st.form("grids"):
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    grids = list(range(1,len(grid)+1))
                    chosen_grid = st.selectbox("Choose Grid Number:", grids)
        
        
                # Second column for aircraft to add:
                with col2:
                    if chosen_color == "Blue":
                        #Add aircraft option:
                    
                        chosen_grid_aircraft = st.selectbox("Aircraft to Add To Grid:",
                                                            list(blue_aircrafts['Aircraft'].unique()))
                    else:
                        chosen_grid_aircraft = st.selectbox("Aircraft to Add To Grid:",
                                                        list(rus_aircrafts['Aircraft'].unique()))
                # Third column for adding or subtracting airacraft:
                with col3:
                    # Number of aircraft to add:
                    add_subtract2 = st.selectbox("Add/Subtract to Grid:", ["Add", "Subtract"])
                # Amount of aircraft to add:
                with col4:
                    #Number of Aircraft to Subtract:
                    nums2 = list(range(0,11))
                    Amount2 = st.selectbox("Amount to Grid:", nums2)
                # Submit buttons:
                with col5:

                    st.write("")
                    st.write("")
                    submit2 = st.form_submit_button("Submit to Grid")
                    if chosen_color == "Blue":

                        if add_subtract2 == "Add" and submit2:
                            add_to_grid(grid, blue_ports, chosen_grid, chosen_grid_aircraft, Amount2)
                    
                        elif add_subtract2 == "Subtract" and submit2:
                            subtract_df(blue_ports, "Hex " + str(chosen_grid), chosen_grid_aircraft, Amount2)
                    
                    else:
                        if add_subtract2 == "Add" and submit2:
                            add_to_grid(grid, rus_airports, chosen_grid, chosen_grid_aircraft, Amount2)

                        elif add_subtract2 == "Subtract" and submit2:
                            subtract_df(rus_airports, "Hex " + str(chosen_grid), chosen_grid_aircraft, Amount2)
            
            
            
        
        
        
        
        # Display NATO:
        display_nato(eu, "natocsv2.csv")
        # Displaying the flank:
        #display_flank(eu, "natocsv2.csv")

        # Displaying the red team
        display_red(eu, "red_gray.csv")

        # Displaying the gray area
        display_gray(eu, "red_gray.csv")
        
        
        # Displaying the blue aircraft ranges:
        display_radius(blue_ports, chosen_type, chosen_group, blue_aircrafts, eu)

        display_rus_radius(rus_airports, chosen_red_aircraft, rus_aircrafts, eu)
        # Adding mouse position display: 
        MousePosition().add_to(eu)
        # Adding a fullscreen option for the map:
        fo.plugins.Fullscreen(position='topright', title='Full Screen', title_cancel='Exit Full Screen').add_to(eu)
        #eu.add_child(MeasureControl())

        
        # Display the grid:
        
        #with st.sidebar.form("Grids"):
        #    grid_submit = st.form_submit_button("Add Grids")
        #    if 'grids2' not in st.session_state and grid_submit:
        #        st.session_state.grids2 = display_grid(eu, grid)
        #    elif grid_submit:
        #        st.session_state.grids2
        
        # Adding the hexagon grid to the map:
        grid_button = st.sidebar.button("Add Grid")
        if grid_button:
            display_grid(eu, grid)
        
        # Adding in a reset button to remove all additions to map:
        with st.sidebar.expander("**:red[Reset Map]**"):
            st.write("Are you sure?")
            reset = st.button("Reset")
            if reset:
                for key in st.session_state.keys():
                    del st.session_state[key] #Deleting all of the keys in the session state
                st.experimental_rerun() # Reloading the page after deletion
        # Adding the airport and information to the map:
        display_airports(blue_ports, eu, blue_aircrafts)

        display_rus_airports(rus_airports, eu, rus_aircrafts)

        

        # Displaying the map:
        display_map(eu)
        

if __name__ == "__main__":
    main()
    

