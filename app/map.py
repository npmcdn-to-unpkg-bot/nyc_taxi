from __future__ import division

import json

import colour
import grequests
import numpy as np
import pandas as pd
import psycopg2
import redis
from bokeh.charts import Bar, hplot, output_file, show
from bokeh.plotting import figure
from bokeh.charts.attributes import CatAttr, ColorAttr
from bokeh.embed import components
from flask import flash, jsonify, redirect, render_template, request, url_for

from app import app

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


def chart_theme(p):
    p.toolbar.logo = None
    p.toolbar_location = None
    p.background_fill_alpha = 0
    p.border_fill_alpha = 0
    p.outline_line_width = 0
    p.outline_line_alpha = 0
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.major_label_text_color = '#bbbbbb'
    p.yaxis.major_label_text_color = '#bbbbbb'
    p.xaxis.axis_label_text_color = '#bbbbbb'
    p.yaxis.axis_label_text_color = '#bbbbbb'
    p.yaxis.minor_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = '#bbbbbb'
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = "#bbbbbb"
    p.yaxis.axis_line_color = "#bbbbbb"
    return p


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range]
                for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


@app.route('/map')
def map_page():
    conn = psycopg2.connect('dbname=taxi user=postgres')
    curs = conn.cursor()

    curs.execute(
        "SELECT DISTINCT neighborhood, neighborhood FROM pois ORDER BY neighborhood")
    neighborhoods = [row for row in curs.fetchall()]
    form = QueryForm()
    form.neighborhood.choices = neighborhoods
    form.neighborhood.default = 'Midtown'

    return render_template('map.html',
                           form=form)


@app.route('/get_blocks', methods=['GET'])
def blocks():
    conn = psycopg2.connect('dbname=taxi user=postgres')
    curs = conn.cursor()

    if request.method == 'GET':
        sql = "SELECT block_id, name FROM pois WHERE neighborhood = '%s' and name <> 'Non-NYC' order by name" % request.args.get(
            'neighborhood', '')
        curs.execute(sql)
        rows = [row for row in curs.fetchall()]
        print rows
    return jsonify(rows)


def rg_gradient(start, end, point):
    gradient = colour.color_scale(colour.web2hsl(
        'red'), colour.web2hsl('green'), 20)
    stepsize = (end - start) / 20
    gradient_bin = np.clip(0, 19, int((point - start) / stepsize))
    return colour.hsl2web(gradient[gradient_bin])


@app.route('/map_api', methods=['GET'])
def map_api():
    conn = psycopg2.connect('dbname=taxi user=postgres')
    curs = conn.cursor()
    r = redis.StrictRedis()

    if request.method == 'GET':
        block_id = request.args.get('block', 514)
        cached = r.get(block_id)
        if cached:
            return jsonify(eval(cached))
        else:
            curs.execute(
                "select latitude + 1/400, longitude + 1/400 from blocks where block_id = %s" % block_id)
            origin = list(curs.fetchone())

            curs.execute("""
                        select latitude, longitude, name, neighborhood, sum(trips) * 1.0 / 181, 
                        sum(fares) / sum(trips), sum(length) / sum(trips) / 60
                        from trips a join blocks b
                        ON dropoff_block = b.block_id
                        join pois c on b.block_id = c.block_id
                        where pickup_block = %s and year = 2015
                        group by 1,2,3,4 order by 5 desc limit 10
                        """ % block_id)

            results = curs.fetchall()

            destinations = [[x[0], x[1]] for x in results]
            names = [{"name": str("%s, %s" % (x[2], x[3])), "trips": "%.1f" % x[4], "avg_fare": "$%.2f" % x[5], "avg_time": "%.1f mins" % x[6]}
                     for x in results]

            paths = get_path(origin, destinations)
            destinations = [x[-1] for x in paths]

            averages = [474.889564336372847,
                        5998.46586211914, 792.464691318635]

            curs.execute(
                "select sum(trips) * 1.0 / 181, sum(fares) / sum(trips), sum(tips) / sum(trips) from trips_by_month where block_id = %s and date >= '2015-01-01'" % block_id)
            trips, fares, tips = map(lambda x: float(x), curs.fetchone())
            perc = trips / averages[0] * 100
            color = rg_gradient(0, 200, perc)

            info = """This block had on average <b>%.1f</b> trips per day in the first half of 2015. This is <font color="%s"><b >%.0f%%</b></font> more than the average block.
                        <br><br>
                        The average fare from this block is $%.2f with a tip of $%.2f""" % (
                trips, color, perc, fares, tips)

            curs.execute("""
                    select cast(hour as varchar) as hour, trips * 1.0 / sum(trips) over() percentage from (
                    select * from 
                    (select hour, trips from trips_by_hour where block_id = %s and hour > 5 order by 1) a

                    union all 
                    select * from 
                    (select hour, trips from trips_by_hour where block_id = %s and hour <= 5 order by 1) b) a
                    """ % (block_id, block_id))

            output = curs.fetchall()
            conn.commit()
            df = pd.DataFrame(output, columns=['Hour', 'Percentage'])
            df['Percentage'] = df['Percentage'].astype(float)

            bar = Bar(df, label=CatAttr(columns=['Hour'], sort=False), values='Percentage',
                      title=None, width=500, legend=None, height=300, color='#375a7f')

            bk = {}

            bar = chart_theme(bar)
            bar.yaxis.axis_label = 'Percentage of Trips'
            bk['bar'] = "\n".join(reversed(components(bar)))

            curs.execute(
                "select date, trips from trips_by_month where block_id = %s order by 1" % block_id)
            output = curs.fetchall()
            line_dates = np.array([x[0] for x in output])
            line_trips = np.array([x[1] / 1000 for x in output])

            p = figure(width=500, height=300, x_axis_type="datetime")

            p.scatter(line_dates, line_trips, color='#375a7f')
            p.line(line_dates, savitzky_golay(
                line_trips, 11, 3), color='#bbbbbb', line_width=3)

            p = chart_theme(p)
            p.yaxis.axis_label = 'Number of trips (k)'

            bk['line'] = "\n".join(reversed(components(p)))
            results = dict(origin=origin, paths=paths,
                           destinations=destinations, names=names, info=info, bk=bk)
            r.set(block_id, results)
            return jsonify(results)
