import json
import requests

start_x = 40.75
start_y = -73.99
origin = [start_x + 1 / 400, start_y + 1 / 400]
destination = [40.75, -73.975]


def get_path(origin, destination):
    get_url = 'https://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=%s,%s&key=AIzaSyCOXJJ7zN4y-t7z2Lc3CEkU5BW3WwkAefM' % (
        origin[0], origin[1], destination[0], destination[1])
    print(get_url)
    r = requests.get(get_url)

    output = json.loads(r.text)

    path = [origin]

    for step in output['routes'][0]['legs'][0]['steps']:
        path.append([step['end_location']['lat'], step['end_location']['lng']])

    return path

targets = [[40.75, -73.975],
           [40.755, -73.975],
           [40.755, -73.98],
           [40.755, -73.985],
           [40.76, -73.98],
           [40.755, -74.0],
           [40.74, -73.985],
           [40.76, -73.975],
           [40.755, -73.97],
           [40.76, -73.97]]

print([get_path(origin, target) for target in targets])
