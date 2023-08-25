import arcpy


def fun_area_filter(polygon, min_area, output):
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

