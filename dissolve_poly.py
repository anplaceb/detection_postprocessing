import arcpy


def fun_poly_dissolve(polygon, output, part="SINGLE_PART"):
    arcpy.Dissolve_management(in_features=polygon, out_feature_class=output,
                              statistics_fields="year MIN;gridcode MIN",
                              multi_part=part)

