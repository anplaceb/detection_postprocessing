import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def raster2poly(raster, value_damage, year, output):
    """
    Extract the pixels with the value that characterizes the damage class from raster. Convert this raster to
    polygon and add attribute year which is year of the detected damage
    :param raster: The input raster with the damage detection
    :param int value_damage: The pixel value that characterizes the damage class
    :param int year: The year of the image raster where the damage is detected
    :param str output: The path where the polygon output is saved
    :return: No return, the output file is saved in the database
    """
    print('Raster to polygon')

    # Extract value 1 (damage)
    extract_damage = ExtractByAttributes(raster, f'Value = {value_damage}')

    arcpy.RasterToPolygon_conversion(in_raster=extract_damage,
                                     out_polygon_features=output,
                                     simplify="NO_SIMPLIFY",
                                     raster_field="Value",
                                     create_multipart_features="SINGLE_OUTER_PART",
                                     max_vertices_per_feature="")

    arcpy.AddField_management(output, "year", "SHORT")
    arcpy.CalculateField_management(output, "year", year)
