import folium as fo
from folium import Choropleth
from folium.plugins import HeatMap
import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit as st
from streamlit_folium import st_folium, folium_static
from folium import plugins
from folium.plugins import MousePosition, MeasureControl, FeatureGroupSubGroup
from shapely.geometry import Polygon, LineString, mapping
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely import wkt
import h3
import json

#Function to display the map
def display_map(map):
    """Dispays the Base Map of Europe

    Args:
        map (Folium Map Object)
    """
    st_map = folium_static(map, width=1200, height=570)

@st.cache_data
def make_grid():
    
    # The lat and long coordinates for the edges of the grid map:
    n = 71.911
    s = 34.229
    e = -30.617
    w = 55.546
    lon_lat_list = [(w, n), (w,s), (e,s), (e,n)]

    polygon_geom = Polygon(lon_lat_list)
    d = {'col1': ['board_boundary'], 'geometry': polygon_geom}
    gdf = gpd.GeoDataFrame(d, geometry='geometry')

    # Get Hexagons
    geojson_shape = (json.loads(gdf.geometry.to_json())
                 ['features'][0]['geometry'])
    hexs = list(h3.polyfill(geojson_shape, res=3, geo_json_conformant=False))

    # Get polygons and linestrings
    polys = []
    lines = []
    centroids = []
    for hid in hexs:
        poly = Polygon(h3.h3_to_geo_boundary(hid))
        polys.append(poly)
        lines.append(LineString(poly.exterior.coords))
        centroids.append(poly.centroid)
    
    label_loc = []
    for p in polys:
        label_loc.append(p.representative_point().coords[:])

    label_loc = [coords[0] for coords in label_loc]

    # Truncate Names
    short_name = [name[:6] for name in hexs]

    hex_df = gpd.GeoDataFrame(data={'hex_name': hexs, 'short_name': short_name,
                                'polys': polys, 'lines': lines,
                                'centroids': centroids,
                                'label_loc': label_loc},
                          geometry='lines', crs="EPSG:3857")
    
    #hex_df = hex_df.to_crs('epsg:3857')
    # Extracting the longitude from the centroids:
    longs = []
    for i in range(len(hex_df)):
        longs.append(hex_df['label_loc'][i][0])
    hex_df['long'] = longs

    # Extracting the latitudes from the centroids:
    lats = []
    for i in range(len(hex_df)):
        lats.append(hex_df['label_loc'][i][1])
    hex_df['lat'] = lats

    # Sorting by the longitudes then the latitudes:
    hex_df2 = hex_df.sort_values(by=['long', 'lat'])
    # Resetting the index of the dataframe:
    hex_df2 = hex_df2.reset_index(drop=True)
    
    return hex_df2


def display_grid(map,hex_df):
    """Display the grid layer on the map based on the hexagon dataframe.

    Args:
        map (Folium Object): The folium base map
        hex_df (Geopandas Geodataframe): The dataframe of hexagons
    """
    
    batch_size = 150
    num_hex = len(hex_df)
    hex_series = gpd.GeoSeries(hex_df['polys'], crs='EPSG:3857')
    
    for i in range(0,num_hex, batch_size):
        batch_hexs = hex_series[i:i+batch_size]

        for j, hex in enumerate(batch_hexs):
            text = "Grid " + str(i+j+1)
            fo.GeoJson(hex, name = "hex"+str(i), tooltip = text,
                    style_function = lambda x: {'opacity':0.1, 'fillOpacity':0,'weight':1, 'color':'#151515'}).add_to(map)
            
        
        
    #sub_group = FeatureGroupSubGroup(feature_group, name = 'Grid Layer')
    
    '''
    for i in range(len(hex_df)):
        geometry = hex_df.iloc[i]['polys']
        h = gpd.GeoSeries(geometry, crs = 'EPSG:3857')
        text = "Grid " + str(i+1)
        fo.GeoJson(h[0], name = "hex"+str(i), tooltip = text,
                style_function = lambda x: {'opacity':0.1, 'fillOpacity':0,'weight':1, 'color':'#151515'} ).add_to(map)
    

    '''


def display_airports(df, map, aircrafts):

    aircraft_list = list(aircrafts["Aircraft"])
    colors = {1: '#0101DF', 2: '#0101DF', 3: '#0101DF'}
    for i in range(len(df)):
            
            # The text to be displayed when hovered over:

            text = ("ICAO: " + df.iloc[i]["ident"]+"<br>"+ "Name: " + df.iloc[i]["name"]+ "<br>"+
            "Elevation: " + str(df.iloc[i]["elevation_ft"])+"<br>"+ "Runway Length: " + str(df.iloc[i]["RWY_LENGTH"]) + "<br>" +
            "Group: " + str(df.iloc[i]["Group"]))

            # The airport text to be displayed when clicked:
            text2 = ["<b>"+name+ "</b>" + ": " + str(df.iloc[i][name]) for name in aircraft_list]
            text3 = "<b><i>"+df.iloc[i]['name']+ "</i></b>" + '<br>' + '<br>'.join(text2)
            
            popup = fo.Popup(text3, min_width=100, max_width=500)
            fo.CircleMarker(location=[df.iloc[i]['latitude_deg'], df.iloc[i]['longitude_deg']], radius=3, 
                        tooltip=text, color = colors[df.iloc[i]['Group']], popup = popup).add_to(map)

def display_nato(map, nato_countries):
    """Displays the non-bordering NATO nations in blue

    Args:
        map (Folium Map Object): The base map to project the NATO nations on
        nato_countries (csv file): The csv file containg the polygons of the NATO countries

    Returns:
        GeoPandas Polygon: Polygon of the NATO countries
        Float: Area of the polygon in square kilometers 
    """

    nato = pd.read_csv('natocsv2.csv')
    nato['geometry'] = nato['geometry'].apply(wkt.loads)
    gdf_all = gpd.GeoDataFrame(nato, crs='4326')

    # The eastern flank of NATO:
    eastern_flank = ["Estonia", "Latvia", "Lithuania", "Poland", "Finland", "Slovakia", "Hungary", "Romania", "Bulgaria", "Turkey"]
    nato = list(gdf_all['name'].unique())

    remaining = set(nato) - set(eastern_flank) - set(["Canada"])

    remaining = list(remaining)

    gdf = gdf_all.loc[gdf_all['name'].isin(remaining)]
    style_nato = {'fillColor': '#1E90FF', 'color': '#1E90FF', 'opacity':0.1}
    boundary = gpd.GeoSeries(unary_union(gdf['geometry']), crs = 'EPSG:4326')
    boundaries = gpd.GeoSeries(gdf['geometry'], crs = 'EPSG:4326')
    #fo.GeoJson(boundary[0], name='nato', style_function= lambda x: style_nato).add_to(map)
    
    for i in range(len(gdf_all)):
        geometry = gdf_all.iloc[i]['geometry']
        country = gpd.GeoSeries(geometry, crs = 'EPSG:4326')
        fo.GeoJson(country[0], name='NATO', style_function=lambda x: {'color': '#1E90FF', 'opacity':0.5}).add_to(map)

    
    # Converting the NATO shape to meters:
    boundary_meters = boundary.to_crs("EPSG:3035")
    area = (boundary_meters.area[0])/1000000

    return boundary_meters, area


def display_flank(map, nato_countries):
    """Displays the flank of NATO highlighted in orange

    Args:
        map (Folium Map Object): The base map to project the flank on
        nato_countries (csv file): The file containing the geopandas polygons of the countries

    Returns:
        GeoPandas Polygon: Polygon of the flank in meters
        Float: Area of the polygon in square kilometers 
    """

    # Loading in the country shapes
    nato = pd.read_csv(nato_countries)
    nato['geometry'] = nato['geometry'].apply(wkt.loads)
    gdf_all = gpd.GeoDataFrame(nato, crs='4326')

    # The eastern flank of NATO:
    eastern_flank = ["Estonia", "Latvia", "Lithuania", "Poland", "Finland", "Slovakia", "Hungary", "Romania", "Bulgaria", "Turkey"]
    # Getting the shapes for the eastern flank:
    flank = gdf_all.loc[gdf_all['name'].isin(eastern_flank)]
    # Orange style color for flank:
    style_flank = {'fillColor': '#FF8C00', 'color': '#FF8C00'}
    # Adding the flanks to the map:
    boundary = gpd.GeoSeries(unary_union(flank['geometry']), crs="EPSG:4326")
    fo.GeoJson(boundary[0], name='flank', style_function = lambda x:style_flank).add_to(map)

    boundary_meters = boundary.to_crs("EPSG:3035")
    flank_area = (boundary_meters.area)/1000000
    
    
    return boundary_meters, flank_area

# Displaying the radius based on the type of aircraft chosen:
def display_radius(df, type, group, aircrafts ,map):
    """For individual view, all aircraft ranges for the chosen type available at each airport will be displayed with mouse hovering ability
    to identify the aircraft.
    For combined view, the largest aircraft range for the chosen type available at each airport will be displayed. The ranges will also 
    combine to create merged polygons.

    Args:
        df (Pandas DataFrame): DataFrame containing information on the airports and the aircraft available for each
        type (Streamlit Select Box): User chosen type of aircraft to display
        aircrafts (Pandas DataFram): DataFrame of the aircrafts and their ranges
        map (Folium Map Object): Base map to project the radius
        view (Streamlit Radio Button): User chosen view for the map

    Returns:
        GeoPandas Polygon: Polygon of the range rings (only for combined view)
        Float: Area of the range rings in square kilometers (only for combined view)
    """

    # Making a dictionary for the aircraft ranges:
    range_dict = pd.Series(aircrafts['Max Range'].values, index = aircrafts['Aircraft']).to_dict()
    style_range = {'fillColor': '#013ADF', 'color': '#013ADF'}
    
    geometry = gpd.points_from_xy(df.longitude_deg, df.latitude_deg)
    geo = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")
    geo2 = geo.to_crs("EPSG:3035")
    buffer_list=[]
    # Options for the dropdown:
    #options = list(aircrafts['Aircraft'][aircrafts['Aircraft'] == type].values)
    if group == ["All"]:
        group = [1,2,3]
    for i in range(len(geo2)):
        for option in type:
            if df.iloc[i][option]>0 and df.iloc[i]['Group'] in group:
                port_range = aircrafts['Max Range'][aircrafts['Aircraft'] == option].values[0]
                buffer_list.append(geo2.iloc[i]['geometry'].buffer((port_range/10)*1852))
        
   
    buffer_df = gpd.GeoDataFrame(geometry=buffer_list, crs="3035")
    buffer_df2 = buffer_df.to_crs("EPSG:4326")
    boundary = gpd.GeoSeries(unary_union(buffer_df2['geometry']), crs="4326")
    fo.GeoJson(boundary[0], name='Blue Aircraft', style_function=lambda x:style_range).add_to(map)

    for i in range(len(df)):
        # Iterating over the options of aircraft available at the airport:
        for option in type:
            # If the airport has that type of aircraft:
            if df.iloc[i][option]>0 and df.iloc[i]["Group"] in group:
                port_range = aircrafts['Max Range'][aircrafts['Aircraft'] == option].values[0]
                # Adding the range of the aircraft around the airport:
                fo.Circle(location=[df.iloc[i]['latitude_deg'], df.iloc[i]['longitude_deg']], 
                        radius=float(((port_range/10)*1852)), color='#556B2F', fill_color='#013ADF', 
                        fill_opacity=0.05*df.iloc[i][option], tooltip = aircrafts["Aircraft"][aircrafts["Aircraft"] == option].values[0], stroke=False).add_to(map)

    boundary_meters = boundary.to_crs("EPSG:3035")
    area = (boundary_meters.area)/1000000
        

    return boundary_meters, area
    
def display_country(countries, file, map):
    """Displays the outline of the country selected.

    Args:
        countries (Streamlit Selection): User selected countries
        file (CSV): The csv file of NATO country polygons
        map (Folium Map Object): The base Map object that the countries will be displayed on.
    """
    # Reading in the NATO CSV file:
    nato = pd.read_csv(file)

    # Loading in the polygon objects in the correct format:
    nato['geometry'] = nato['geometry'].apply(wkt.loads)
    # Color style:
    style_countries = {'fillColor': '#FF00FF', 'color': '#FF00FF'}
    # GeoPandas dataframe of the NATO countries:
    gdf = gpd.GeoDataFrame(nato, crs='4326')
    
    # Iterating through the choices of countries that were selected:
    for country in countries:
        country_picked = gdf.loc[gdf['name']==country]
        boundary = gpd.GeoSeries(country_picked['geometry'], crs = 'EPSG:4326')
        fo.GeoJson(boundary, name='country', style_function= lambda x: style_countries).add_to(map)

def add_df(df, airport, aircraft, num):

    #Row of cell to change:
    row = df.index[df['name'] == airport].values[0]

    #New value of cell:
    new_val = df[aircraft][df['name'] == airport].values[0] + num

    df.at[row, aircraft] = new_val

def add_to_grid(hex_df2, airport_df, grid_number, aircraft, num):
    

    hex_id = int(grid_number) - 1

    long = hex_df2.iloc[hex_id]['long']
    lat = hex_df2.iloc[hex_id]['lat']
    name = "Hex " + str(grid_number)
    ident = "Hex "+str(grid_number)

    # Checking if the hex airport is already in the airport dataframe
    # If it isn't, a new row will be added:
    if name not in airport_df.name.values:
        new_row = {'ident': ident,'name':name,'latitude_deg': lat, 'longitude_deg':long, 'Group':1, aircraft:num}
        airport_df.loc[len(airport_df)] = new_row
    # If is in the dataframe:
    else:
        #Row of cell to change:
        row = airport_df.index[airport_df['name'] == name].values[0]
        #New value of cell:
        new_val = airport_df[aircraft][airport_df['name'] == name].values[0] + num
        airport_df.at[row, aircraft] = new_val
    



def subtract_df(df, airport, aircraft, num):

    #Row of cell to change:
    row = df.index[df['name'] == airport].values[0]

    #New value of cell:
    new_val = df[aircraft][df['name'] == airport].values[0] - num

    if new_val < 0:
        new_val = 0
    
    df.at[row, aircraft] = new_val



#### Red and Gray functions ####



def display_red(map, country):

    red_gray = pd.read_csv(country)
    rus = red_gray[red_gray['name'] == 'Russia']
    rus['geometry'] = rus['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(rus, crs='4326')

    style_rus = {'fillColor': '#FF0000', 'color': '#FF0000', 'opacity':0.5}
    boundary = gpd.GeoSeries(unary_union(gdf['geometry']), crs = 'EPSG:4326')
    boundaries = gpd.GeoSeries(gdf['geometry'], crs = 'EPSG:4326')
    fo.GeoJson(boundary[0], name='russia', style_function= lambda x: style_rus).add_to(map)

def display_gray(map, country):
    red_gray = pd.read_csv(country)
    gray = red_gray[red_gray['name'] != 'Russia']
    gray['geometry'] = gray['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(gray, crs='4326')

    style_gray = {'fillColor': '#585858', 'color': '#585858'}
    boundary = gpd.GeoSeries(unary_union(gdf['geometry']), crs = 'EPSG:4326')
    boundaries = gpd.GeoSeries(gdf['geometry'], crs = 'EPSG:4326')
    fo.GeoJson(boundary[0], name='gray', style_function= lambda x: style_gray).add_to(map)
    


def display_rus_airports(df, map, aircrafts):

    aircraft_list = list(aircrafts["Aircraft"])
    
    for i in range(len(df)):
            
            # The text to be displayed when hovered over: 
            text = ("ICAO: " + df.iloc[i]["ident"]+"<br>"+ "Name: " + df.iloc[i]["name"]+ "<br>"+
            "Elevation: " + str(df.iloc[i]["elevation_ft"])+"<br>"+ "Runway Length: " + str(df.iloc[i]["RWY_LENGTH"]) + "<br>")

            # The text to be displayed when clicked:
            text2 = ["<b>"+name+ "</b>" + ": " + str(df.iloc[i][name]) for name in aircraft_list]
            text3 = "<b><i>"+df.iloc[i]['name']+ "</i></b>" + '<br>' + '<br>'.join(text2)
            
            
            popup = fo.Popup(text3, min_width = 100, max_width=500)
            fo.CircleMarker(location=[df.iloc[i]['latitude_deg'], df.iloc[i]['longitude_deg']], radius=3, 
                        tooltip=text, color = '#DF0101', popup = popup).add_to(map)


def display_rus_radius(df, type, aircrafts ,map):
    """For individual view, all aircraft ranges for the chosen type available at each airport will be displayed with mouse hovering ability
    to identify the aircraft.
    For combined view, the largest aircraft range for the chosen type available at each airport will be displayed. The ranges will also 
    combine to create merged polygons.

    Args:
        df (Pandas DataFrame): DataFrame containing information on the airports and the aircraft available for each
        type (Streamlit Select Box): User chosen type of aircraft to display
        map (Folium Map Object): Base map to project the radius

    Returns:
        GeoPandas Polygon: Polygon of the range rings (only for combined view)
        Float: Area of the range rings in square kilometers (only for combined view)
    """

    # Making a dictionary for the aircraft ranges:
    range_dict = pd.Series(aircrafts['Max Range'].values, index = aircrafts['Aircraft']).to_dict()
    style_range = {'fillColor': '#DF0101', 'color': '#DF0101'}
    
    geometry = gpd.points_from_xy(df.longitude_deg, df.latitude_deg)
    geo = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")
    geo2 = geo.to_crs("EPSG:3035")
    buffer_list=[]
    # Options for the dropdown:
    #options = list(aircrafts['Aircraft'][aircrafts['Aircraft'] == type].values)

    for i in range(len(geo2)):
        for option in type:
            if df.iloc[i][option]>0:
                port_range = aircrafts['Max Range'][aircrafts['Aircraft'] == option].values[0]
                buffer_list.append(geo2.iloc[i]['geometry'].buffer((port_range/10)*1852))
        
   
    buffer_df = gpd.GeoDataFrame(geometry=buffer_list, crs="3035")
    buffer_df2 = buffer_df.to_crs("EPSG:4326")
    boundary = gpd.GeoSeries(unary_union(buffer_df2['geometry']), crs="4326")
    fo.GeoJson(boundary[0], name='union', style_function=lambda x:style_range).add_to(map)

    for i in range(len(df)):
        # Iterating over the options of aircraft available at the airport:
        for option in type:
            # If the airport has that type of aircraft:
            if df.iloc[i][option]>0:
                port_range = aircrafts['Max Range'][aircrafts['Aircraft'] == option].values[0]
                # Adding the range of the aircraft around the airport:
                fo.Circle(location=[df.iloc[i]['latitude_deg'], df.iloc[i]['longitude_deg']], 
                        radius=float(((port_range/10)*1852)), color='#DF0101', fill_color='#DF0101', 
                        fill_opacity=0.05*df.iloc[i][option], tooltip = aircrafts["Aircraft"][aircrafts["Aircraft"] == option].values[0], stroke=False).add_to(map)

    boundary_meters = boundary.to_crs("EPSG:3035")
    area = (boundary_meters.area)/1000000
        

    return boundary_meters, area


