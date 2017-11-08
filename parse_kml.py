from pykml import parser
from pprint import pprint
import json


def open_kml(file):
	"""
	Open file

	PARAMS		file - path to the KML file
	RETURN 		doc - relevant part of the doc
	"""

	with open(file, 'r') as f:
		doc = parser.parse(f).getroot().Document.Folder.Placemark

	return doc

def get_polygons(doc):
	"""
	Extract polygons defined with coordinates

	PARAMS		doc - relevant part of the doc
	RETURNS		polygons - dict with districs and border coordinates
	"""
	polygons = {}

	# iterate over all polygons
	for p in doc:

		# district name
		district = str(p.name).lower().title()

		# find and split the coordinates
		coordinates = p.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates.text

		polygons[district] = coordinates

	return polygons


def parse_coordinates(coor):
	"""
	Parse coordinates
	
	PARAMS		coor - coordinates in the form KML stores them
	RETURNS		polygon_parsed - list of lists with coordinates of particular district
	"""

	polygon_parsed = []

	#iterate over and parse the coordinates
	coor = coor.split(' ')
	for c in coor:
		if c == '':
			continue
		else:
			latlong = c.split(',')
			polygon_parsed.append([float(latlong[1]), float(latlong[0])])

	return polygon_parsed

def write_json(final_data, out_file):
	"""
	Writing data to file
	"""
	with open(out_file, 'w') as out:
		json.dump(final_data, out)

	print('Success, JSON data dumped to file!')
	return


def main():
	"""
	Main method
	"""

	final_data = {}

	#open file and return relevant part of the doc
	doc = open_kml('data/sg_districts.kml')
	# return dict with all polygons
	polygons = get_polygons(doc)
	# iterate over polygons and prepare final data
	for district, polygon in polygons.items():
		final_data[district] = parse_coordinates(polygon)
	# write json data to file
	write_json(final_data, 'data/sg_polygons.json')


if __name__ == '__main__':
	main()