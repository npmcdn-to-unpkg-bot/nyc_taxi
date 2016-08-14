--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: blocks; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blocks (
    block_id integer,
    latitude double precision,
    longitude double precision,
    count integer
);


ALTER TABLE public.blocks OWNER TO postgres;

--
-- Name: google_places_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE google_places_type (
    block_id integer NOT NULL,
    lodging integer,
    clothing_store integer,
    cafe integer,
    restaurant integer,
    school integer,
    health integer,
    meal_delivery integer,
    point_of_interest integer,
    subway_station integer,
    electronics_store integer,
    home_goods_store integer,
    bar integer,
    police integer,
    convenience_store integer,
    store integer,
    synagogue integer,
    furniture_store integer,
    food integer,
    sublocality_level_1 integer,
    florist integer,
    bicycle_store integer,
    locality integer,
    hardware_store integer,
    night_club integer,
    park integer,
    grocery_or_supermarket integer,
    general_contractor integer,
    pharmacy integer,
    church integer,
    jewelry_store integer,
    bakery integer,
    meal_takeaway integer,
    pet_store integer,
    shoe_store integer,
    post_office integer,
    book_store integer,
    neighborhood integer,
    art_gallery integer,
    finance integer,
    gym integer,
    lawyer integer,
    doctor integer,
    insurance_agency integer,
    real_estate_agency integer,
    accounting integer,
    car_dealer integer,
    physiotherapist integer,
    travel_agency integer,
    liquor_store integer,
    parking integer,
    bus_station integer,
    atm integer,
    hospital integer,
    spa integer,
    movie_theater integer,
    library integer,
    museum integer,
    moving_company integer,
    cemetery integer,
    storage integer,
    local_government_office integer,
    car_repair integer,
    transit_station integer,
    courthouse integer,
    gas_station integer,
    dentist integer,
    department_store integer,
    car_rental integer,
    hindu_temple integer,
    funeral_home integer,
    painter integer,
    car_wash integer,
    bank integer,
    mosque integer,
    locksmith integer,
    university integer,
    hair_care integer,
    beauty_salon integer,
    shopping_mall integer,
    place_of_worship integer,
    roofing_contractor integer,
    plumber integer,
    laundry integer,
    veterinary_care integer,
    electrician integer,
    amusement_park integer,
    stadium integer,
    movie_rental integer,
    campground integer,
    bowling_alley integer,
    premise integer,
    natural_feature integer,
    zoo integer,
    aquarium integer,
    light_rail_station integer,
    rv_park integer,
    embassy integer,
    city_hall integer,
    airport integer,
    fire_station integer,
    casino integer
);


ALTER TABLE public.google_places_type OWNER TO postgres;

--
-- Name: pois; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE pois (
    block_id integer,
    name character varying(100),
    neighborhood character varying(100),
    type character varying(50)
);


ALTER TABLE public.pois OWNER TO postgres;

--
-- Name: trips; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE trips (
    pickup_block integer,
    dropoff_block integer,
    year integer,
    length double precision,
    trips integer,
    fares double precision,
    tips double precision,
    passengers double precision,
    trip_distance double precision,
    trip_type character varying(10)
);


ALTER TABLE public.trips OWNER TO postgres;

--
-- Name: trips_by_hour; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE trips_by_hour (
    block_id integer,
    hour integer,
    trips integer
);


ALTER TABLE public.trips_by_hour OWNER TO postgres;

--
-- Name: trips_by_month; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE trips_by_month (
    block_id integer,
    month date,
    trips integer,
    fares double precision,
    tips double precision,
    passengers integer
);


ALTER TABLE public.trips_by_month OWNER TO postgres;

--
-- Name: weather; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE weather (
    datetime timestamp without time zone NOT NULL,
    temperature double precision,
    humidity double precision,
    precip_intensity double precision,
    precip_type character varying(10)
);


ALTER TABLE public.weather OWNER TO postgres;

--
-- Name: google_places_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY google_places_type
    ADD CONSTRAINT google_places_type_pkey PRIMARY KEY (block_id);


--
-- Name: weather_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY weather
    ADD CONSTRAINT weather_pkey PRIMARY KEY (datetime);


--
-- Name: ix_block; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_block ON trips_by_month USING btree (block_id);


--
-- Name: ix_blockid; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_blockid ON trips_by_hour USING btree (block_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

