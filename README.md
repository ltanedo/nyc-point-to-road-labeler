# nyc-snap-to-road
A python libray to rapidly label single-points or complete geojson files against all ~150k roads in the 5 boroughs of NYC.  Implementation builds a lookup index from the NYC Open-Data Portal and efficiently matches using SKLearns KDTree.  Very useful in performing geospatial data science such as snapping certain incidents like traffic, crime, or event data to their retrospective roads. Also great for higher level detail analysis after clustering by NYC Census regions or Precincts.

## 1. Setup Guide
- Install required packages
```
pip install -r requirements.txt
```

## 2. Methods/Functions
> when running code, wait 60sec + for the roads.geojson to download from the NYC_Portal

- import the library 
```
import nyc_road_snapper as nyc
```

- get original points labeled with respective roads
```
origin = nyc.match_geojson(geojson_file = "Points Of Interest.geojson")
```
```
          type                                   properties.name  ...          geometry.neighboring_coordinates geometry.neighboring_distance_0
0      Feature                                           HOLLAND  ...   [-74.00702722131126, 40.72449594711067]                        0.000139
1      Feature                                        WHITESTONE  ...  [-73.82658912975347, 40.797242921781546]                        0.000066
2      Feature                                          BROOKLYN  ...   [-73.99393860604367, 40.70334425633271]                        0.000503
3      Feature                                         MANHATTAN  ...   [-73.99194346565635, 40.70958905248659]                        0.000011
4      Feature                                           PULASKI  ...    [-73.95265702902643, 40.7388788759719]                        0.000187
...        ...                                               ...  ...                                       ...                             ...
20567  Feature                   COLUMBIA UNIVERSITY EAST CAMPUS  ...   [-73.9584066268315, 40.807419210867444]                        0.000552
20568  Feature                 BARNARD COLLEGE HARLAN FISKE HALL  ...   [-73.96347671925801, 40.81037320181099]                        0.000280
20569  Feature  COLUMBIA UNIVERSITY HEYMAN CENTER FOR HUMANITIES  ...   [-73.9584066268315, 40.807419210867444]                        0.000510
20570  Feature                  BARNARD COLLEGE BRINCKERHOF HALL  ...   [-73.96258278994867, 40.80998664702823]                        0.000255
20571  Feature                                      CABANA HOTEL  ...   [-73.92820646002045, 40.84098170055525]                        0.000245

```

- convert result(pd) to geojson
```
origin = nyc.df_to_formatted_json(origin)
```
```
[
  {
    "type": "Feature",
    "properties": {
      "name": "HOLLAND",
      
      .
      .
      .
      .
      
      "neighboring_street": "BROOME ST"
    },
    "geometry": {
      "type": "Point",
      "coordinates": [
        -74.00701717096757,
        40.724634757833414
      ],
      "neighboring_coordinates": [
        -74.00702722131126,
        40.72449594711067
      ],
      "neighboring_distance": 0.00013917408579699914
    }
  },
  
     .
     .
     .
  
```

- get Dataframe from single point
```
output = nyc.match_point(
    lat   =-74.00701717096757,
    lon   = 40.724634757833414,
    label ="N/A", 
    k     = 3
)
```
```
  Location                               Coordinates  ... geometry.neighboring_distance_1 geometry.neighboring_distance_2
0      N/A  [-74.00701717096757, 40.724634757833414]  ...                        0.000139                        0.000139
```
