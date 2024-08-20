'''a={"type":"FeatureCollection","features":[{"bbox":[78.37941,17.43157,78.388651,17.443546],"type":"Feature","properties":{"segments":[{"distance":2510.2,"duration":252.9,"steps":[{"distance":7.7,"duration":2.8,"type":11,"instruction":"Head northeast","name":"-","way_points":[0,1]},{"distance":14.1,"duration":5.1,"type":1,"instruction":"Turn right","name":"-","way_points":[1,3]},{"distance":183.6,"duration":66.1,"type":1,"instruction":"Turn right","name":"-","way_points":[3,13]},{"distance":245.1,"duration":21.2,"type":7,"instruction":"Enter the roundabout and take the 2nd exit","name":"-","exit_number":2,"way_points":[13,26]},{"distance":167.6,"duration":20.0,"type":7,"instruction":"Enter the roundabout and take the 1st exit","name":"-","exit_number":1,"way_points":[26,34]},{"distance":161.9,"duration":19.4,"type":1,"instruction":"Turn right","name":"-","way_points":[34,37]},{"distance":843.9,"duration":57.9,"type":0,"instruction":"Turn left onto Inorbit Mall Road","name":"Inorbit Mall Road","way_points":[37,51]},{"distance":374.9,"duration":27.0,"type":12,"instruction":"Keep left onto Inorbit Mall Road","name":"Inorbit Mall Road","way_points":[51,73]},{"distance":511.5,"duration":33.5,"type":4,"instruction":"Turn slight left onto Durgam Cheruvu Road","name":"Durgam Cheruvu Road","way_points":[73,88]},{"distance":0.0,"duration":0.0,"type":10,"instruction":"Arrive at Durgam Cheruvu Road, on the right","name":"-","way_points":[88,88]}]}],"summary":{"distance":2510.2,"duration":252.9},"way_points":[0,88]},"geometry":{"coordinates":[[78.380348,17.443503],[78.380404,17.443546],[78.380452,17.443469],[78.380472,17.443437],[78.380351,17.443342],[78.380185,17.443131],[78.380098,17.442946],[78.380075,17.442872],[78.380037,17.442703],[78.380031,17.442469],[78.380051,17.44234],[78.380084,17.442244],[78.380209,17.442074],[78.380292,17.441996],[78.380346,17.442008],[78.380402,17.441999],[78.380449,17.44197],[78.38048,17.441926],[78.380489,17.44186],[78.380464,17.441798],[78.380438,17.441772],[78.380406,17.441754],[78.380342,17.441642],[78.379987,17.441088],[78.379788,17.440753],[78.379751,17.440697],[78.37941,17.440244],[78.379417,17.440219],[78.379573,17.440102],[78.379658,17.440002],[78.37967,17.439989],[78.379868,17.439807],[78.380123,17.439549],[78.380389,17.439239],[78.380465,17.439134],[78.380399,17.439011],[78.380282,17.438894],[78.379514,17.438],[78.379662,17.437877],[78.380692,17.437038],[78.381037,17.436758],[78.381218,17.436618],[78.382179,17.435859],[78.382508,17.435615],[78.382628,17.435469],[78.383235,17.435026],[78.383973,17.434468],[78.384207,17.43429],[78.384666,17.433943],[78.38512,17.43359],[78.385341,17.433426],[78.385659,17.433191],[78.385804,17.433164],[78.385899,17.433169],[78.386123,17.433208],[78.386323,17.433227],[78.386547,17.433189],[78.386683,17.43316],[78.386863,17.433111],[78.387115,17.433031],[78.387271,17.432956],[78.387367,17.432904],[78.38765,17.432743],[78.387795,17.432642],[78.38788,17.432574],[78.387953,17.4325],[78.388023,17.432399],[78.38807,17.432244],[78.388078,17.43219],[78.388082,17.432124],[78.38814,17.43176],[78.388162,17.431694],[78.388209,17.43163],[78.38826,17.431586],[78.388337,17.43157],[78.388454,17.431581],[78.388519,17.431604],[78.388587,17.431658],[78.388625,17.43172],[78.388651,17.431808],[78.38865,17.43204],[78.388592,17.432333],[78.388446,17.432625],[78.388278,17.432888],[78.388156,17.433135],[78.388118,17.433389],[78.388149,17.433693],[78.388308,17.435128],[78.388381,17.435781]],"type":"LineString"}}],"bbox":[78.37941,17.43157,78.388651,17.443546],"metadata":{"attribution":"openrouteservice.org | OpenStreetMap contributors","service":"routing","timestamp":1671547973225,"query":{"coordinates":[[78.380355,17.443495],[78.388417,17.435777]],"profile":"driving-car","format":"json"},"engine":{"version":"6.8.0","build_date":"2022-10-21T14:34:31Z","graph_date":"2022-11-17T23:46:05Z"}}}
'''
import folium
import json

def waypoint_data(a):
  '''
  INPUT
  =====
  a-json output of the request from the osm
  
  OUTPUT
  ======
  g-geometrical co-ordinates of the route that the vehicle has to take
  d-data of the co-ordinates like the distance for a specific set of waypoints,
   instruction for the waypoints 
   and the number of waypoints required to complete a specified path in the route
  '''
  a=json.loads(a)
  b=a['features']
  c=[]
  d=[]
  g=[]
  for i in b:
      c=i
      d1=c['properties']['segments'][0]['steps']
      g1=c["geometry"]["coordinates"]
      g.append(g1)
      for j in d1:
          d.append([j['distance'],j['instruction'],j['way_points']])
  g1=[]
  if len(g)>1:
      for i in g:
          print(i)
          for j in i:
              g1.append[j]
      return g1,d
  else:
      return g[0],d


def save_map(a):
	'''
	INPUT
	=====
	a-json output of the request from the osm
	
	OUTPUT
	======
	map-the map with all waypoints saved in it
	'''
	g,d=waypoint_data(a)
	
	my_map4 = folium.Map(location = [g[0][1],g[0][0]],zoom_start = 12)
	for m in g:
		folium.Marker([m[1],m[0]]).add_to(my_map4)

	my_map4.save("./static/my_map4.html")
	
#save_map(a)
