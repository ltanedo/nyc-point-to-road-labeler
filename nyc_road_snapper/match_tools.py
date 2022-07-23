import pandas    as pd
import numpy     as np
from . import easy_json as easy_json
from sklearn.neighbors import BallTree, KDTree
import os
import requests

def geojson_to_pd(geojson_file):
    geojson_featues = easy_json.get(geojson_file)["features"]
    return pd.json_normalize(geojson_featues)

def get_ny_frame():
    resp = requests.get("https://data.cityofnewyork.us/api/geospatial/svwp-sbcd?method=export&format=GeoJSON").json()["features"]
    df = pd.json_normalize(resp).rename(
        columns={
                "geometry.coordinates":"NB_geometry.coordinates",
                "properties.stname_lab":"NB_properties.stname_lab",
            }
    )
    df = df.explode("NB_geometry.coordinates").reset_index()
    return df

def df_to_formatted_json(df, sep="."):
    result = []
    for idx, row in df.iterrows():
        parsed_row = {}
        for col_label,v in row.items():
            keys = col_label.split(".")

            current = parsed_row
            for i, k in enumerate(keys):
                if i==len(keys)-1:
                    current[k] = v
                else:
                    if k not in current.keys():
                        current[k] = {}
                    current = current[k]
        # save
        result.append(parsed_row)
    return result

def match(
    sources, 
    neighbors, 
    sources_gps_label, 
    sources_loc_label, 
    neighbors_gps_label, 
    neighbors_loc_label,
    k = 1
):

    kd              = KDTree(np.array(neighbors[neighbors_gps_label].tolist()), metric='euclidean')
    output          = kd.query(np.array(sources[sources_gps_label].tolist()), k)
    distances       = pd.DataFrame(output[0])
    neighbors_index = pd.DataFrame(output[1])
    sources         = sources.rename(columns={sources_loc_label : f"Source_Location"})

    for i, column in enumerate(neighbors_index):
        indexes = list(neighbors_index[column])
        new_neighbors = neighbors.reindex(indexes).reset_index()
        new_distances = distances[distances.columns[i]].rename(f"Distance_{i}")
        
        if i < 1:
            sources = pd.concat([sources,new_neighbors[[neighbors_loc_label,neighbors_gps_label]], new_distances], axis=1)#.drop(columns=['index'])
        else:
            sources = pd.concat([sources, new_distances], axis=1)#.drop(columns=['index'])
        
        sources = sources.rename(
            columns = {
                "NB_properties.stname_lab" : f"properties.neighboring_street",
                "NB_geometry.coordinates"  : f"geometry.neighboring_coordinates",
                "Distance_0"        : f"geometry.neighboring_distance_0",
                "Distance_1"        : f"geometry.neighboring_distance_1",
                "Distance_2"        : f"geometry.neighboring_distance_2"

            }
        )
    return sources



def match_geojson(geojson_file):
    origin = geojson_to_pd(
        geojson_file
    )
    output = match(
        sources              =geojson_to_pd(geojson_file), 
        neighbors            =get_ny_frame(),
        sources_gps_label    ="geometry.coordinates",
        sources_loc_label    ="properties.stname_lab",
        neighbors_gps_label  ="NB_geometry.coordinates",
        neighbors_loc_label  ="NB_properties.stname_lab",
        k=1
    )
    return output

def match_point(
    lat,
    lon,
    label="N/A", 
    k = 1
):
    sources  = pd.DataFrame([[label, [lat, lon]],], columns = ["Location", "Coordinates"])
    neighbors = get_ny_frame()
    sources_gps_label   = "Coordinates"
    sources_loc_label   = "Location"
    neighbors_gps_label = "NB_geometry.coordinates"
    neighbors_loc_label = "NB_properties.stname_lab"

    print(neighbors)
    kd        = KDTree(np.array(neighbors[neighbors_gps_label].tolist()), metric='euclidean')
    output    = kd.query(np.array(sources[sources_gps_label].tolist()), k)
    distances = pd.DataFrame(output[0])
    neighbors_index = pd.DataFrame(output[1])

    for i, column in enumerate(neighbors_index):
        indexes = list(neighbors_index[column])
        new_neighbors = neighbors.reindex(indexes) \
                                .reset_index()
        new_distances = distances[distances.columns[i]] \
                                .rename(f"Distance_{i}")
        
        if i < 1:
            sources = pd.concat([sources,new_neighbors[[neighbors_loc_label,neighbors_gps_label]], new_distances], axis=1)#.drop(columns=['index'])
        else:
            sources = pd.concat([sources, new_distances], axis=1)#.drop(columns=['index'])
        
        sources = sources.rename(
            columns = {
                "NB_properties.stname_lab" : f"properties.neighboring_street",
                "NB_geometry.coordinates"  : f"geometry.neighboring_coordinates",
                "Distance_0"        : f"geometry.neighboring_distance_0",
                "Distance_1"        : f"geometry.neighboring_distance_1",
                "Distance_2"        : f"geometry.neighboring_distance_2"

            }
        )

    return sources

