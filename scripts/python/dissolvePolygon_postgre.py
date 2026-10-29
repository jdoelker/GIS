from qgis import processing
from qgis.core import QgsDataSourceUri, QgsVectorLayer

# 1. CONFIGURE AND LOAD SOURCE POSTGIS LAYER
source_uri = QgsDataSourceUri()
source_uri.setConnection("localhost", "5432", "gisdb", "gisadmin", "postgreSQL")
source_uri.setDataSource("gis", "us_county", "geom", "")

source_layer = QgsVectorLayer(source_uri.uri(), "us_county", "postgres")
if not source_layer.isValid():
    raise Exception("Failed to load source layer from PostgreSQL.")

# 2. RUN DISSOLVE (Outputs to temporary memory layer)
dissolve_params = {
    'INPUT': source_layer,
    'FIELD': ['state_fips'],  # Put column name here if grouping (e.g., ['category'])
    'SEPARATE_DISJOINT': False,
    'OUTPUT': 'memory:us_county_diss'
}
print("Dissolving layer...")
dissolve_result = processing.run("native:dissolve", dissolve_params)
memory_layer = dissolve_result['OUTPUT']

# 3. EXPORT DIRECTLY VIA PROCESSING (Bypasses manual exporter issues)
# This uses your existing QGIS connection profile name or specific DB settings
pg_export_params = {
    'INPUT': memory_layer,
    'DATABASE': 'local-gisdb',        # Name of database connection saved in QGIS Browser
    'SCHEMA': 'gis',
    'TABLE': 'us_county_diss',
    'PK': 'id',
    'GEOCOLUMN': 'geom',
    'OVERWRITE': True,
    'APPEND': False,
    'PROMOTETOMULTI': True              # Crucial step: forces geometry into MultiPolygon
}

print("Exporting dissolved data via native importer...")
processing.run("qgis:importintopostgis", pg_export_params)
print("Finished! Check your destination table now.")


