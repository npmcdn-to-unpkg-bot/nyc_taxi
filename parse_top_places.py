from __future__ import division

import json
import urllib
import os
# from io import open
from collections import Counter


class typeCounter:

    def __init__(self, l):
        l = [t for t in poi_types if t not in [
            'point_of_interest', 'establishment']]
        self.len = len(l)
        self.c = Counter(l)

    def vectorize(self, normalize=False):
        vector = self.c.most_common()
        if normalize:
            return [(x[0], x[1] / self.len) for x in vector]
        else:
            return vector

    def most_common_type(self, n=1):
        try:
            return self.c.most_common(n)[0][0]
        except:
            return ""

files = os.listdir(".")

outf = open("pois.txt", "w", encoding='utf-8')

for filename in files:
    if filename.startswith("google"):
        with open(filename) as json_file:
            d = json.load(json_file)

        for place in d:
            poi_types = []
            for i, poi in enumerate(d[place]):
                if poi == 'lng':
                    lng = d[place][poi]
                elif poi == 'lat':
                    lat = d[place][poi]
                else:
                    entry = d[place][poi]
                    top_poi = None
                    # take the most prominent place as a fallback
                    if i == 0:
                        neighborhood = entry['neighborhood']
                        fallback = entry['name']
                    # try and use the most prominent point of interest as the
                    # block name
                    if not top_poi and 'point_of_interest' in entry['type']:
                        top_poi = entry['name']

                    poi_types.extend(entry['type'])

            poi_types = typeCounter(poi_types)
            # if top_poi:
            #     name = top_poi
            # else:
            #     name = fallback
            name = fallback
            outf.write('%s\t%s\t%s\t%s\n' %
                       (place, name, neighborhood, poi_types.most_common_type()))
