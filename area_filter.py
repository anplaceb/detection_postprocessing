import arcpy


def fun_area_filter(polygon, min_area, output):
    """
    Filter polygons which area is under a certain value. If not area field attribute found, one is created
    :param str polygon: The input feature class with the polygons to filter
    :param float min_area: Minimal area for the detection polygons in ha
    :param str output: The output file path with the polygons over or equal to the minimal area value
    :return: No return, the output file is saved in the output folder
    """
    print("Area filter")

    # Set local variables
    field_name = "area_ha"
    expression = "!SHAPE.area@hectares!"

    # check if field exists
    fields = arcpy.ListFields(polygon)  # returns a list of field objects
    fields = [f.name for f in fields]  # access name attribute

    # if field doesn't exist, create it
    if field_name not in fields:
        arcpy.AddField_management(polygon, field_name, "DOUBLE", field_precision=10,
                                  field_scale=2)

    # Execute CalculateField
    arcpy.CalculateField_management(polygon, "area_ha", expression)

    arcpy.ExportFeatures_conversion(polygon, output, f'area_ha >= {min_area}',
                                    "NOT_USE_ALIAS", None, None)

