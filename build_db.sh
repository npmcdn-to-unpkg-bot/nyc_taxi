export project=skillful-hull-137823

# create base tables
# bq rm nyc.trips_green_2014_base
# bq rm nyc.trips_green_2015_base
# bq rm nyc.trips_base
# bq rm nyc.trips_by_hour_base

    bq query --destination_table=nyc.trips_green_2014_base "SELECT
            CAST(pickup_latitude * 200 AS integer) / 200 pickup_latitude,
            CAST(pickup_longitude * 200 AS integer) / 200 pickup_longitude,
            CAST(dropoff_latitude * 200 AS integer) / 200 dropoff_latitude,
            CAST(dropoff_longitude * 200 AS integer) / 200 dropoff_longitude,
            YEAR(pickup_datetime) year,
        SUM(TIMESTAMP_TO_SEC(dropoff_datetime) - TIMESTAMP_TO_SEC(pickup_datetime)) length,
        COUNT(*) trips,
        SUM(fare_amount) fares,
        SUM(tip_amount) tips,
        SUM(passenger_count) passengers,
        SUM(trip_distance) trip_distance
        FROM [nyc-tlc:green.trips_2014]
        WHERE pickup_longitude < -70 and dropoff_longitude < -70
        GROUP BY 1,2,3,4,5 HAVING COUNT(*) > 3 ORDER BY trips DESC;"

    bq query --destination_table=nyc.trips_green_2015_base "SELECT
            CAST(pickup_latitude * 200 AS integer) / 200 pickup_latitude,
            CAST(pickup_longitude * 200 AS integer) / 200 pickup_longitude,
            CAST(dropoff_latitude * 200 AS integer) / 200 dropoff_latitude,
            CAST(dropoff_longitude * 200 AS integer) / 200 dropoff_longitude,
            YEAR(pickup_datetime) year,
        SUM(TIMESTAMP_TO_SEC(dropoff_datetime) - TIMESTAMP_TO_SEC(pickup_datetime)) length,
        COUNT(*) trips,
        SUM(fare_amount) fares,
        SUM(tip_amount) tips,
        SUM(passenger_count) passengers,
        SUM(trip_distance) trip_distance
        FROM [nyc-tlc:green.trips_2015]
        WHERE pickup_longitude < -70 and dropoff_longitude < -70
        GROUP BY 1,2,3,4,5 HAVING COUNT(*) > 3 ORDER BY trips DESC;"

    bq query --destination_table=nyc.trips_base "SELECT
            CAST(pickup_latitude * 200 AS integer) / 200 pickup_latitude,
            CAST(pickup_longitude * 200 AS integer) / 200 pickup_longitude,
            CAST(dropoff_latitude * 200 AS integer) / 200 dropoff_latitude,
            CAST(dropoff_longitude * 200 AS integer) / 200 dropoff_longitude,
            YEAR(pickup_datetime) year,
        SUM(TIMESTAMP_TO_SEC(dropoff_datetime) - TIMESTAMP_TO_SEC(pickup_datetime)) length,
        COUNT(*) trips,
        SUM(fare_amount) fares,
        SUM(tip_amount) tips,
        SUM(passenger_count) passengers,
        SUM(trip_distance) trip_distance
        FROM [nyc-tlc:yellow.trips]
        WHERE pickup_longitude < -70 and dropoff_longitude < -70
        GROUP BY 1,2,3,4,5 HAVING COUNT(*) > 20 ORDER BY trips DESC;"

    bq query --destination_table=nyc.trips_by_hour_base "SELECT CAST(pickup_latitude * 200 AS integer) / 200 pickup_latitude,
            CAST(pickup_longitude * 200 AS integer) / 200 pickup_longitude,
        HOUR(pickup_datetime) hour,
        COUNT(*) trips
        FROM [nyc-tlc:green.trips_2015],
        [nyc-tlc:green.trips_2014],
        [nyc-tlc:yellow.trips]
        WHERE pickup_longitude < -70 and dropoff_longitude < -70
        GROUP BY 1,2,3 HAVING COUNT(*) > 3 ORDER BY trips DESC;"


    bq query --destination_table=nyc.trips_by_month_base "SELECT CAST(pickup_latitude * 200 AS integer) / 200 pickup_latitude,
            CAST(pickup_longitude * 200 AS integer) / 200 pickup_longitude,
        SUBSTR(CAST(pickup_datetime as string), 1, 7) + '-01' month,
        COUNT(*) trips,
        SUM(fare_amount) fares,
        SUM(tip_amount) tips,
        SUM(passenger_count) passengers
        FROM [nyc-tlc:green.trips_2015],
        [nyc-tlc:green.trips_2014],
        [nyc-tlc:yellow.trips]
        WHERE pickup_longitude < -70 and dropoff_longitude < -70
        GROUP BY 1,2,3 HAVING COUNT(*) > 3 ORDER BY trips DESC;"

    # bq rm nyc.trips_green_2014
    # bq rm nyc.trips_green_2015
    # bq rm nyc.trips
    # bq rm nyc.trips_by_hour

    bq query --destination_table=nyc.trips_green_2014 "SELECT B.block_id as pickup_block, C.block_id as dropoff_block,
        year,
        length,
        trips,
        fares,
        tips,
        passengers,
        trip_distance,
        'green' taxi_type 
        FROM [$project:nyc.trips_green_2014_base] A  JOIN
        [$project:nyc.large_blocks] B ON pickup_latitude = B.latitude AND pickup_longitude = B.longitude  JOIN
        [$project:nyc.large_blocks] C ON dropoff_latitude = C.latitude AND dropoff_longitude = C.longitude;"

    bq query --destination_table=nyc.trips_green_2015 "SELECT B.block_id as pickup_block, C.block_id as dropoff_block,
        year,
        length,
        trips,
        fares,
        tips,
        passengers,
        trip_distance,
        'green' taxi_type 
        FROM [$project:nyc.trips_green_2015_base] A  JOIN
        [$project:nyc.large_blocks] B ON pickup_latitude = B.latitude AND pickup_longitude = B.longitude  JOIN
        [$project:nyc.large_blocks] C ON dropoff_latitude = C.latitude AND dropoff_longitude = C.longitude;"

    bq query --destination_table=nyc.trips "SELECT B.block_id as pickup_block, C.block_id as dropoff_block,
        year,
        length,
        trips,
        fares,
        tips,
        passengers,
        trip_distance,
        'yellow' taxi_type 
        FROM [$project:nyc.trips_base] A  JOIN
        [$project:nyc.large_blocks] B ON pickup_latitude = B.latitude AND pickup_longitude = B.longitude  JOIN
        [$project:nyc.large_blocks] C ON dropoff_latitude = C.latitude AND dropoff_longitude = C.longitude;"

    bq query --destination_table=nyc.trips_by_hour "SELECT block_id,
        hour, trips
        FROM [$project:nyc.trips_by_hour_base] A  JOIN
        [$project:nyc.large_blocks] B ON pickup_latitude = B.latitude AND pickup_longitude = B.longitude"

    bq query --destination_table=nyc.trips_by_month "SELECT block_id,
        month, trips, fares, tips, passengers
        FROM [$project:nyc.trips_by_month_base] A  JOIN
        [$project:nyc.large_blocks] B ON pickup_latitude = B.latitude AND pickup_longitude = B.longitude"
    # extract data to cloud storage

    bq extract nyc.trips_green_2014 gs://$project.appspot.com/trips_green_2014.csv
    bq extract nyc.trips_green_2015 gs://$project.appspot.com/trips_green_2015.csv
    bq extract nyc.trips gs://$project.appspot.com/trips.csv
    bq extract nyc.trips_by_hour gs://$project.appspot.com/trips_by_hour.csv
    bq extract nyc.trips_by_month gs://$project.appspot.com/trips_by_month.csv

    # download from cloud storage

    gsutil -m cp gs://$project.appspot.com/*.csv .
    # gsutil cp gs://$project.appspot.com/trips_by_month.csv .

    # create database schema
    # psql -U "DROP DATABASE taxi;"
    psql -U "CREATE DATABASE taxi;"

    psql taxi -U postgres -f ddl.sql

    # insert data
    # psql taxi -U postgres -c "TRUNCATE TABLE trips"

    psql taxi -U postgres -c "\copy trips from trips.csv CSV HEADER"
    psql taxi -U postgres -c "\copy trips from trips_green_2014.csv CSV HEADER"
    psql taxi -U postgres -c "\copy trips from trips_green_2015.csv CSV HEADER"
    psql taxi -U postgres -c "\copy trips_by_hour from trips_by_hour.csv CSV HEADER"
    psql taxi -U postgres -c "\copy trips_by_month from trips_by_month.csv CSV HEADER"

    # psql taxi -U postgres -c "select trip_type, sum(trips) from trips group by 1 order by 1"
    # psql taxi -U postgres -c "select year, sum(trips) from trips group by 1 order by 1"

