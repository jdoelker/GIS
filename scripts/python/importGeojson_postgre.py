from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsVectorLayerExporter,
    QgsDataSourceUri,
    QgsProject
)

#Load the local GeoJSON file
geojson_path = "/home/jdoelker/Downloads/DATA/us_states.geojson"
layer = QgsVectorLayer(geojson_path, "us_state", "ogr")

if not layer.isValid():
  print("Failed to load GeoJSON file!")
else:

  # 2. Define the PostGIS connection URI string
  uri = """dbname='gisdb' host='localhost' port='5432' user='gisadmin' password='postgreSQL' table='gis'.'us_state' (geom) key=id"""

#Export the layer to PostGIS
  err, err_message = QgsVectorLayerExporter.exportLayer(
      layer,
      uri,
      "postgres",
      layer.crs(),
      False,  # If True, only selected features are exported
  )

  if err == QgsVectorLayerExporter.NoError:
    print("Successfully imported GeoJSON into PostGIS!")
  else:
    print(f"Export failed: {err_message}")