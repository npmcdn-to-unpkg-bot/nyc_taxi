from __future__ import division

from flask import render_template, redirect, flash, request, jsonify, url_for
from app import app

import json
import grequests
import psycopg2

from .forms import QueryForm


def parse_json(origin, r):
    output = json.loads(r.text)
    path = [origin]
    for step in output['routes'][0]['legs'][0]['steps']:
        coords = step['end_location']
        path.append((coords['lat'], coords['lng']))
    return path


def get_path(origin, destinations):
    urls = ['https://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=%s,%s&key=AIzaSyCOXJJ7zN4y-t7z2Lc3CEkU5BW3WwkAefM' % (
        origin[0], origin[1], destination[0], destination[1]) for destination in destinations]
    print urls[0]

    rs = (grequests.get(u) for u in urls)

    return [parse_json(origin, r) for r in grequests.map(rs)]


@app.route('/map')
def map():
    conn = psycopg2.connect('dbname=taxi user=postgres')
    curs = conn.cursor()

    block_id = 692
    curs.execute(
        "select latitude + 1/400, longitude + 1/400 from blocks where block_id = %s" % block_id)
    origin = list(curs.fetchone())
    curs.execute(
        "SELECT DISTINCT neighborhood, neighborhood FROM pois ORDER BY neighborhood")
    neighborhoods = [row for row in curs.fetchall()]
    form = QueryForm()
    form.neighborhood.choices = neighborhoods

    curs.execute("""
                select latitude, longitude, name, neighborhood, sum(trips), sum(fares) / sum(trips), sum(length) / sum(trips)
                from trips a join blocks b
                ON dropoff_block = b.block_id
                join pois c on b.block_id = c.block_id
                where pickup_block = %s
                group by 1,2,3,4 order by 5 desc limit 10
                """ % block_id)
    results = curs.fetchall()

    destinations = [[x[0], x[1]] for x in results]
    names = [{"name": str("%s, %s" % (x[2], x[3])), "trips": x[4], "avg_fare": "$%.2f" % x[5], "avg_time": "%.1f mins" % x[6]}
             for x in results]
    print names

    paths = get_path(origin, destinations)
    destinations = [x[-1] for x in paths]
    return render_template('map.html',
                           form=form,
                           paths=paths,
                           destinations=destinations,
                           origin=origin,
                           names=names)


@app.route('/get_blocks', methods=['GET'])
def blocks():
    conn = psycopg2.connect('dbname=taxi user=postgres')
    curs = conn.cursor()

    if request.method == 'GET':
        sql = "SELECT block_id, name FROM pois WHERE neighborhood = '%s'" % request.args.get(
            'neighborhood', '')
        curs.execute(sql)
        rows = [row for row in curs.fetchall()]
        print rows
    return jsonify(rows)


@app.route('/map_api', methods=['GET'])
def map_api():
    conn = psycopg2.connect('dbname=taxi user=postgres')
    curs = conn.cursor()

    if request.method == 'GET':
        block_id = request.args.get('block', '')
        curs.execute(
            "select latitude + 1/400, longitude + 1/400 from blocks where block_id = %s" % block_id)
        origin = list(curs.fetchone())

        curs.execute("""
                    select latitude, longitude, name, neighborhood, sum(trips), sum(fares) / sum(trips), sum(length) / sum(trips)
                    from trips a join blocks b
                    ON dropoff_block = b.block_id
                    join pois c on b.block_id = c.block_id
                    where pickup_block = %s
                    group by 1,2,3,4 order by 5 desc limit 10
                    """ % block_id)

        results = curs.fetchall()

        destinations = [[x[0], x[1]] for x in results]
        names = [{"name": str("%s, %s" % (x[2], x[3])), "trips": x[4], "avg_fare": "$%.2f" % x[5], "avg_time": "%.1f mins" % x[6]}
                 for x in results]

        paths = get_path(origin, destinations)
        destinations = [x[-1] for x in paths]
        print origin
        print paths
        print destinations
        print names
        return jsonify(dict(origin=origin, paths=paths, destinations=destinations, names=names))
