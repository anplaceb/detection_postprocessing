import arcpy


def buffer_vect(polygon, buffer_dist, output):
    """
    Perform a buffer operation
    :param str polygon: The input polygon that will be buffered
    :param str buffer_dist: The buffer distance
    :param str output: The output feature class with the buffer performed
    :return: No return, the output file is saved in the database
    """
    arcpy.PairwiseBuffer_analysis(in_features=polygon, buffer_distance_or_field=buffer_dist, out_feature_class=output)
