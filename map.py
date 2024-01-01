import ee
import requests

# Initialize the Earth Engine module
ee.Initialize()

# Define the image ID
img = ee.Image('COPERNICUS/S2_SR/20210109T185751_20210109T185931_T10SEG')

# Define the region of interest as a bounding box
region = ee.Geometry.BBox(-122.0859, 37.0436, -122.0626, 37.0586)

# Get the download URL for the image
url = img.getDownloadUrl({
    'bands': ['B3', 'B8', 'B11'],
    'region': region,
    'scale': 20,
    'format': 'GEO_TIFF'
})

# Download the image using requests
response = requests.get(url)
with open('sentinel_2.tif', 'wb') as fd:
    fd.write(response.content)
