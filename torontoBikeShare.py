import folium
import pandas as pd
import json

TORONTO_COORDs = [43.660209, -79.387387]



def get_trip_counts_by_hour(selected_hour):

    # collect coordinates of stations
    locations = bike_data.groupby("from_station_name").first()
    locations = locations.loc[:, ["stations_lat", "stations_lon"]]

    # create a subset of requested time
    subset = bike_data[bike_data["hour"]==selected_hour]

    departure_counts =  subset.groupby("from_station_name").count().iloc[:,[0]]
    departure_counts.columns= ["Departure Count"]

    arrival_counts =  subset.groupby("to_station_name").count().iloc[:,[0]]
    arrival_counts.columns= ["Arrival Count"]

    trip_counts = departure_counts.join(locations).join(arrival_counts)
    return trip_counts



def plot_station_counts():
    # create a new map
    map = folium.Map(location=TORONTO_COORDs, zoom_start=14,  tiles="CartoDB positron")

    #create a new feature group


    for i in range (0, 24):
        name = "Bike stations statistic for " + str(i) +":00"
        fg = folium.FeatureGroup(name=name)
        trip_counts = get_trip_counts_by_hour(i)

        for index, row in trip_counts.iterrows():
            # calculate net departures
            net_departures = (row["Departure Count"]-row["Arrival Count"])

            # generate the popup message that is shown on click.
            popup_text = "{}<br> Total departures: {}<br> Total arrivals: {}<br> Net departures: {}"
            popup_text = popup_text.format(index.replace("'", ""),
                                                  row["Arrival Count"],
                                                  row["Departure Count"],
                                                  net_departures)

            # radius of circles
            radius = net_departures / 8

            # choose the color of the marker
            if net_departures>0:
                # color="#FF533D" # WATERMELON
                 color="#E14658" # CORAL
                #color="#E37222" # tangerine
            else:
                # color="#0375B4" # blue
                # color="#88D317" # LIME
                color="#0A8A9F" # teal

            # add marker to the map
            fg.add_child(folium.CircleMarker(location=(row["stations_lat"],
                                                        row["stations_lon"]),
                                                        radius=radius,
                                                        color=color,
                                                        parse_html=True,
                                                        popup=popup_text,
                                                        fill=True))

        fg.add_to(map)

    return map




# execute main
if __name__ == "__main__":
    bike_data = pd.read_csv('TorontoBikeRideshareData.csv')
    bike_data["trip_start_time"] = pd.to_datetime(bike_data["trip_start_time"])
    bike_data["trip_stop_time"] = pd.to_datetime(bike_data["trip_stop_time"])
    bike_data["hour"] = bike_data["trip_start_time"].map(lambda x: x.hour)

    # trip_counts = get_trip_counts_by_hour(5)
    map = plot_station_counts()
    folium.LayerControl().add_to(map)
    map.save("TorontoBikeRideshareData.html")
