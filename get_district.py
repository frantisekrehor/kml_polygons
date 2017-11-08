import json
import csv
from shapely.geometry import Point, Polygon
from pprint import pprint


def load_def(json_file):
	"""
	Load definition of district polygons - boarders defined with GPS coordinates

	PARAMS		json_file - district objects - boarders defined with GPS coordinates in list
	RETURN 		df - definition of polygons in dict
	"""

	with open(json_file) as f:
		df = json.loads(f.read())

	return df

def init_polygons(df):
	"""
	Creating Polygon objects and store it in dict
	
	PARAMS		df - definition of polygons in dict
	RETURN 		polygons - initialized polygons stored in dict
	"""

	polygons = {}

	for district, coor in df.items():
		polygons[district] = Polygon(coor)

	return polygons

def get_district(polygons, latitute, longitude):
	"""
	Assign district for a point
	
	PARAMS		polygons - initialized polygons stored in dict
				latitude - latitude GPS coor
				longitude - longitude GPS coor
	RETURN 		district - where the point defined with latitude/longitude belongs to
	"""
	
	tested_point = Point(latitute, longitude)
	district = None

	for d, p in polygons.items():

		contains = p.contains(tested_point)
		if not contains:
			continue
		else:
			district = d
			break

	return district

def main():
	"""
	Main function
	"""

	df = load_def('data/sg_polygons.json')
	polygons = init_polygons(df)

	with open('data/data_in.csv', 'r') as data_in, open('data/data_out.csv', 'w') as data_out:
		reader = csv.DictReader(data_in, delimiter=';')
		writer = csv.DictWriter(data_out, fieldnames=reader.fieldnames+['district'])
		writer.writeheader()

		#iterate over rows
		for r in reader:

			if r['latitude'] != '':
				r['district'] = get_district(polygons, float(r['latitude']), float(r['longitude']))
			else:
				r['district'] = ''
			
			writer.writerow(r)
		
	print('Success, the dataset is enriched with `distric` column ans stored into a file.')


if __name__ == '__main__':
	main()
		







