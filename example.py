import nyc_road_snapper as nyc

""" retuns pandas dataframe

"""
origin = nyc.match_geojson(geojson_file = "Points Of Interest.geojson")

""" converts dataframe back to geojson
"""
origin = nyc.df_to_formatted_json(origin)
print(len(origin))

""" Returns Dataframe of single point
"""
output = nyc.match_point(
    lat   =-74.00701717096757,
    lon   = 40.724634757833414,
    label ="N/A", 
    k     = 3
)
print(output.columns)