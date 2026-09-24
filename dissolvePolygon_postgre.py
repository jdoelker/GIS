from qgis import processing
from qgis.core import QgsDataSourceUri, QgsVectorLayer

# 1. CONFIGURE AND LOAD SOURCE POSTGIS LAYER
source_uri = QgsDataSourceUri()
source_uri.setConnection("localhost", "5432", "dbasename", "username", "password")
source_uri.setDataSource("schema", "table_name", "geom", "")

source_layer = QgsVectorLayer(source_uri.uri(), "table_name", "postgres")
if not source_layer.isValid():
    raise Exception("Failed to load source layer from PostgreSQL.")

# 2. RUN DISSOLVE
dissolve_params = {
    'INPUT': source_layer,
    'FIELD': [],  # agg column
    'SEPARATE_DISJOINT': False,
    'OUTPUT': 'memory:temp_output_table'
}
print("Dissolving layer...")
dissolve_result = processing.run("native:dissolve", dissolve_params)
memory_layer = dissolve_result['OUTPUT']

# EXPORT PARAMS
pg_export_params = {
    'INPUT': memory_layer,
    'DATABASE': 'dbname',        # Name specific to QGIS
    'SCHEMA': 'schema_name',
    'TABLE': 'output_table',
    'PK': 'id',
    'GEOCOLUMN': 'geom',
    'OVERWRITE': True,
    'APPEND': False,
    'PROMOTETOMULTI': True              #force geometry into multi
}

print("Exporting dissolved data via native importer...")
processing.run("qgis:importintopostgis", pg_export_params)
print("Finished! Check your destination table now.")


