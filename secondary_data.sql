--Secondary data dump into postgres

psql taxi -U postgres -c "\copy google_places_type from /google-places/place_type_count_by_blockid.csv CSV HEADER"
psql taxi -U postgres -c "\copy weather from /weather/Weather_history_20090101_20151231.csv CSV HEADER"