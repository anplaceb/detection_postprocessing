import arcpy


def fun_poly_dissolve(polygon, output, part="SINGLE_PART"):
    """
    Dissolve polygons and create individual features for each part. The attribute values year (year of the damage
    detection) and gridcode (value for damage class) remain in the output same as in the input
    :param str polygon: The input feature class with the polygons to dissolve
    :param str output: The output feature class with the dissolved polygons
    :param str part: Specifies whether multipart features will be allowed in the output, in this case they are not
    allowed and individual features are created for each part
    :return: No return, the output file is saved in the database
    """
    arcpy.Dissolve_management(in_features=polygon, out_feature_class=output,
                              statistics_fields="year MIN;gridcode MIN",
                              multi_part=part)

    arcpy.AlterField_management(in_table=output, field='MIN_year', new_field_name='year')
    arcpy.AlterField_management(in_table=output, field='MIN_gridcode', new_field_name='gridcode')

