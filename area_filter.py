import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def fun_area_filter(polygon, min_area, output):
    print("Area filter")

    # Set local variables
    expression = "!SHAPE.area@hectares!"
    # Execute AddField

    arcpy.AddField_management(polygon, "area_ha", "DOUBLE", field_precision=10,
                              field_scale=2)

    # Execute CalculateField
    arcpy.CalculateField_management(polygon, "area_ha", expression)

    arcpy.ExportFeatures_conversion(polygon, output, f'area_ha >= {min_area}',
                                    "NOT_USE_ALIAS", None, None)



