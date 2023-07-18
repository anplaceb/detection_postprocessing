import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def raster2poly(raster, value_damage, output):
    print('Raster to polygon')

    # Extract value 1 (damage)
    print("Extract value 1")

    extract_damage = ExtractByAttributes(raster, f'Value = {value_damage}')

    out = arcpy.RasterToPolygon_conversion(in_raster=extract_damage,
                                           out_polygon_features=output,
                                           simplify="NO_SIMPLIFY",
                                           raster_field="Value",
                                           create_multipart_features="SINGLE_OUTER_PART",
                                           max_vertices_per_feature="")