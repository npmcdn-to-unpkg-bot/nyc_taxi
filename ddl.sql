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
-- Name: pois; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE pois (
    block_id integer,
    name character varying(100),
    neighborhood character varying(100),
    type character varying(50)
);

--
-- Name: trips; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE trips (
    pickup_block integer,
    dropoff_block integer,
    year 
,
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
-- Name: ix_dropoff; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_dropoff ON trips USING btree (dropoff_block);


--
-- Name: ix_pickup; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_pickup ON trips USING btree (pickup_block);


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

