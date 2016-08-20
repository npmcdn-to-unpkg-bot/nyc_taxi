# New York Taxi Data

## Overview

This project is an attempt to create a template to connect various data sources with the NYC taxi data to extract meaningful insight with respect to NYC neighborhood growth and trend. 

NYC taxi data served as the primary data source, with Google Places API, Geonames and weather data used as additional data sources. In addition, for the visualization piece Google Directions and OSRM were integrated. All of the data was eventually stored in postgres.

Due to the scale involved (1.1 Billion distinct trips), making calls to the Google Places API became a limitation. Because of this, the project was scaled down to focus on key blocks that were most utilized by passengers. In addition, because the API call to Google Places is for what is available currently the temporal aspects could not be readily captured. While it was scaled down, the integration of these various data sources still yielded interesting results. 

The operational website can be found here: http://ec2-54-197-5-212.compute-1.amazonaws.com:8000/map

While the publicly available taxi data is static, it would be interesting to run a similar pipeline in realtime to better understand the movement of the NYC population and how new places (restaurants, gym, etc) and changes in neighborhood begin to affect the flow of the population. 


## Set-up

The following scripts should be executed in order to recreate: 

1.	ddl.sql – creates the database in postgres that will store the relevant data
2.	build_db.sh – script that will execute aggregation query on big query and then extract data from big query and store it into postgres
3.	Google places-Final.ipynb – produces google places full extract of the key blocks and creates csv file that contains count of types of locations by block id.
4.	parse_top_places.py – 
5.	weather.py – produces historical weather file. File should be executed by passing a start date and end date argument, i.e. `./weather.py YYYY-MM-DD YYYY-MM-DD`
6.	secondary_data.sql – inserts data from steps 3-5 into postgres

## Tech Stack

- Hosted on EC2
- BigQuery to do heavy data processing of raw taxi data
- Postgresql to stored processed results
- Flask with gunicorn workers to serve app
- Bokeh used to generate charts and Leaflet.js to plot routes
- Redis used to cache API calls and bokeh graphs

### APIs Used

- Google Places to retrieve nearby points of interest
- Google Directions to retrieve route between two points
- GeoNames to get nearest intersection of a given point
- Forecast.io to get historical weather data
