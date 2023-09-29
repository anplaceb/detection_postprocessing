import arcpy


def fun_poly_dissolve(polygon, output, part="SINGLE_PART"):
    arcpy.Dissolve_management(in_features=polygon, out_feature_class=output,
                              statistics_fields="year MIN;gridcode MIN",
                              multi_part=part)

    arcpy.AlterField_management(in_table=output, field='MIN_year', new_field_name='year')
    arcpy.AlterField_management(in_table=output, field='MIN_gridcode', new_field_name='gridcode')

