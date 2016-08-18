# nyc_taxi

This project is an attempt to create a template to connect various data sources with the NYC taxi data to extract meaningful insight with respect to NYC neighborhood growth and trend. 

NYC taxi data served as the primary data source, with Google Places API, Geonames and weather data used as additional data sources. In addition, for the visualization piece Google Directions and OSRM were integrated.

Due to the scale involved (1.1 Billion distinct trips), making calls to the Google Places API became a limitation. Because of this the project was scaled down to focus on key blocks that were most utilized by passengers as a pilot.

The following scripts should be executed in order: 

1.	ddl.sql – creates the database in postgres that will store the relevant data
2.	build_db.sh – script that will execute aggregation query on big query and then extract data from big query and store it into postgres
3.	Google places-Final.ipynb – produces google places full extract of the key blocks and creates csv file that contains count of types of locations by block id.
4.	parse_top_places.py – 
5.	weather.py – produces historical weather file. File should be executed by passing a start date and end date argument, i.e. `./weather.py YYYY-MM-DD YYYY-MM-DD`
6.	secondary_data.sql – inserts data from steps 3-5 into postgres
