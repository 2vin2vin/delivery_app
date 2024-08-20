import requests
from functions_osm import *

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}
module='directions'
vehicle='driving-car'
key='5b3ce3597851110001cf6248e0c38a8e89e64af09fc8ba8f56371942'
initial_coord='78.380355,17.443495'
final_coord='78.388417,17.435777'
call = requests.get('https://api.openrouteservice.org/v2/{}/{}?api_key={}&start={}&end={}'.format(module,vehicle,key,initial_coord,final_coord), headers=headers)
'''
print(call.status_code, call.reason)
print(call.text)
'''
#a=call.text
#print(save_map(a))

def generate_map(initial_coord, final_coord):
    call = requests.get('https://api.openrouteservice.org/v2/{}/{}?api_key={}&start={}&end={}'.format(module,vehicle,key,initial_coord,final_coord), headers=headers)
    a=call.text
#    print(a)
    print(save_map(a))
