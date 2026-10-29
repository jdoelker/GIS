from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject

# 1. Initialize the URI object
uri = QgsDataSourceUri()

# 2. Set database connection details
uri.setConnection("localhost", "5432", "gisdb", "gisadmin", "postgreSQL")

# 3. Specify the schema, table, geometry column, and an optional SQL subset/where clause
# (schema_name, table_name, geometry_column, a_subset_string, a_primary_key_column)
uri.setDataSource("gis", "us_county", "geom", "", "id")

# 4. Create the vector layer ("postgres" is the provider key)
layer_name = "us_county"
vlayer = QgsVectorLayer(uri.uri(False), layer_name, "postgres")

# 5. Add it to the QGIS Project interface
if vlayer.isValid():
    QgsProject.instance().addMapLayer(vlayer)
    print("Layer loaded successfully!")
else:
    print("Failed to load layer. Check your connection settings.")