# Old code for individual view (scared to delete)
'''
    if view == "Individual":
        # Options for the dropdown:
        options = list(aircrafts['Aircraft'][aircrafts['Type'] == type].values)
        # Iterating over the airports to identify options available:
        for i in range(len(df)):
            # Iterating over the options of aircraft available at the airport:
            for option in options:
                # If the airport has that type of aircraft:
                if df.iloc[i][option]>0:
                    port_range = aircrafts['Max Range'][aircrafts['Aircraft'] == option].values[0]
                    # Adding the range of the aircraft around the airport:
                    fo.Circle(location=[df.iloc[i]['latitude_deg'], df.iloc[i]['longitude_deg']], 
                            radius=float(((port_range/15)*1852)), color='#556B2F', fill_color='#556B2F', 
                            fill_opacity=0.35, tooltip = aircrafts["Aircraft"][aircrafts["Aircraft"] == option].values[0]).add_to(map)

'''

 # Old code for type of aircraft (scared to delete)
'''
        # Making a list of planes available for the airport:
        for i in range(len(geo2)):
            planes = []
            for option in options:
                if df.iloc[i][option]>0:
                    planes.append(option)
            # If there is the type of aircraft at the airport
            if len(planes)>0:
                port_range = max([range_dict[x] for x in planes])
                buffer_list.append(geo2.iloc[i]['geometry'].buffer((port_range/10)*1852))
'''

  # Type of display:
        #map_types = ["Combined", "Individual"]
        #view = st.sidebar.radio("Choose Map View:",
        #                    map_types)


#st.sidebar.subheader(":red[Total Area of Coverage]")
        #st.sidebar.markdown('{:,}'.format(round(coverage_area[0])) + " km\u00b2")
        
        #st.sidebar.subheader(":red[Eastern Flank Coverage]")
        #st.sidebar.markdown('{:,}'.format(round(coverage_flank_area[0])) + " km\u00b2")
        #st.sidebar.markdown(flank_perc)
        
        #st.sidebar.subheader(":red[Total NATO Coverage]")
        #st.sidebar.markdown('{:,}'.format(round(coverage_nato_area[0])) + " km\u00b2")
        #st.sidebar.markdown(nato_perc)


#if view == "Combined":
        # The flank object and its area:
'''
        flank, flank_area = display_flank(eu, "natocsv2.csv")
        flank_df = gpd.GeoDataFrame(geometry=flank)

        # The NATO object and its area:
        nato, nato_area = display_nato(eu, "natocsv2.csv")
        nato_df = gpd.GeoDataFrame(geometry=nato)

        # The range rings object and its area:
        coverage, coverage_area = display_radius(df_joined, chosen_type, chosen_group, aircrafts, eu)
        coverage_df = gpd.GeoDataFrame(geometry=coverage)

        # Finding the coverage of the range rings over the flank area:
        coverage_flank = coverage_df.overlay(flank_df, how = 'intersection')
        coverage_flank_area = (coverage_flank.area)/1000000
        # Computing the percentage of coverage:
        flank_perc = coverage_flank_area/flank_area
        flank_perc = '{:.2f}%'.format(flank_perc[0]*100)

        #Finding the coverage of the range rings over the rest of NATO:
        coverage_nato = coverage_df.overlay(nato_df, how = 'intersection')
        coverage_nato_area = (coverage_nato.area)/1000000
        # Computing the percentage of coverage:
        nato_perc = (coverage_nato_area + coverage_flank_area)/(nato_area + flank_area)
        nato_perc = '{:.2f}%'.format(nato_perc[0]*100)
'''

'''
# Dropdown for Countries:
        country_codes = list(nato['name'].unique())
        country_codes.sort()
        chosen_country = st.sidebar.multiselect("Select Country:",
                                            country_codes)
    
    #Display Country:
        display_country(chosen_country, file, eu)
'''

'''
#text2 = [name + ":" + str(df.iloc[i][name]) for name in aircraft_list]
            text_popup = ("<b><i>"+df.iloc[i]["name"] + "</i></b>" + "<br>" + "Boeing:<br>" + str(df.iloc[i]["Boeing 787"]) + "<br>" + "Airbus:<br>" + str(df.iloc[i]["Airbus A330"]) +
                          "<br>" + "Dorier:<br>" + str(df.iloc[i]["Dorier 228"]) + "<br>" + "Bae Jet:<br>" + str(df.iloc[i]["Bae Jetstream 3"])+
                          "<br>" + "Aviocar:<br>" + str(df.iloc[i]["Aviocar"])+ "<br>" + "Beech:<br>" + str(df.iloc[i]["Beechcraft 1900"])+
                          "<br>" + "Cessna 172:<br>" + str(df.iloc[i]["Cessna 172"]) + "<br>" + "Blackhawk:<br>" + str(df.iloc[i]["Blackhawk"])+
                          "<br>" + "Eurocopter:<br>" + str(df.iloc[i]["Eurocopter"]) + "<br>" + "Bell 47:<br>" + str(df.iloc[i]["Bell 47"]) +
                          "<br>" + "Robinson:<br>" + str(df.iloc[i]["Robinson R22"]) + "<br>" + "Chinese Weather:<br>" + str(df.iloc[i]["ChineseWeather"]))
'''

'''
text_popup = ("<b><i>"+df.iloc[i]["name"] + "</i></b>" + "<br>" + "Mig-35:<br>" + str(df.iloc[i]["Mig-35"]) + "<br>" + "Tu-95:<br>" + str(df.iloc[i]["Tu-95"]) +
                          "<br>" + "Mi-28N:<br>" + str(df.iloc[i]["Mi-28N"]) + "<br>" + "An-12:<br>" + str(df.iloc[i]["An-12"])+
                          "<br>" + "Tu-160:<br>" + str(df.iloc[i]["Tu-160"])+ "<br>" + "Be-200:<br>" + str(df.iloc[i]["Be-200"])+
                          "<br>" + "Be-30:<br>" + str(df.iloc[i]["Be-30"]))
'''

'''
def add_grid_red(hex_df2, rus_aircraft_df, grid_number, aircraft, num):
    

    hex_id = int(grid_number) - 1

    long = hex_df2.iloc[hex_id]['long']
    lat = hex_df2.iloc[hex_id]['lat']
    name = "Hex " + str(grid_number)
    ident = "Hex "+str(grid_number)

    new_row = {'ident': ident,'name':name,'latitude_deg': lat, 'longitude_deg':long, aircraft:num}
    rus_aircraft_df.loc[len(rus_aircraft_df)] = new_row
'''

'''
    df = pd.read_csv('hexagon_grid.csv')
    df['geometry'] = df['lines'].apply(wkt.loads)
    hex_df2 = gpd.GeoDataFrame(df, crs='3857')


    #fo.GeoJson(data = hex_df2['lines'], style_function=lambda x: {'opacity':0.1, 'fillOpacity':0,'weight':10, 'color':'#151515'}).add_to(map)
    '''
'''
    for i in range(len(hex_df2)):
        geometry = hex_df2.iloc[i]['polys']
        h = gpd.GeoSeries(geometry, crs = 'EPSG:3857')
        text = "Grid " + str(i+1)
        fo.GeoJson(h[0], name = "hex"+str(i), tooltip = text,
                style_function = lambda x: {'opacity':0.1, 'fillOpacity':0,'weight':1, 'color':'#151515'} ).add_to(map)
    '''