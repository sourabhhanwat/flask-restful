# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json, os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import urllib.request

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

def get_exif(image_file_path):

	print('image_file_path')
	exif_table = {}
	image = Image.open(urllib.request.urlopen(image_file_path))
	info = image.getexif()
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		exif_table[decoded] = value
	gps_info = {}
	for key in exif_table['GPSInfo'].keys():
		decode = GPSTAGS.get(key,key)
		gps_info[decode] = exif_table['GPSInfo'][key]
	return gps_info

class pattern (Resource):

	# is a GET request for this resource
	def get(self):

		return jsonify({'message': 'hello world'})

	# Corresponds to POST request
	def post(self):
		
		record = json.loads(request.data)
		exif = get_exif(record['image'])
		print(exif)
		return jsonify({'data': exif})



# adding the defined resources along with their corresponding urls
api.add_resource(pattern, '/')


# driver function
if __name__ == '__main__':

	app.run(debug = True)
