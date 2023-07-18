import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def fun_area_filter(polygon):
    print("Area filter")

    # Set local variables
    in_table = polygon
    field_name = "area_ha"
    expression = "getClass(float(!SHAPE.area!)/10000)"

    codeblock = """
    def getClass(area):
        if area >= 0.25:
            return 1
        else:
            return 2"""

    # Execute AddField
    arcpy.management.AddField("raster2poly_nbr_threshold_2019", "area_ha", "LONG", None, None, None, '', "NULLABLE",
                              "NON_REQUIRED", '')


    arcpy.AddField_management(in_table, field_name, "DOUBLE", field_precision=10,
                              field_scale=2)

    # Execute CalculateField
    arcpy.CalculateField_management(in_table, field_name, expression, "PYTHON_9.3",
                                    codeblock)


