import arcpy


def morpho_vect(polygon, buffer_dist, output):
    arcpy.PairwiseBuffer_analysis(in_features=polygon, buffer_distance_or_field=buffer_dist, out_feature_class=output)


