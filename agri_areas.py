import arcpy


def agri_areas(polygon, agri, output):
    """
    Remove agriculture polygons from detection polygons
    :param str polygon: The input feature class from which the agriculture areas will be erased
    :param str agri: The features that will be used to erase coincident features in the input
    :param str output: The output feature class with the agriculture areas erased
    :return: No return, the output file is saved in the database
    """
    print('Remove detection from agriculture areas')
    arcpy.PairwiseErase_analysis(in_features=polygon, erase_features=agri, out_feature_class=output)
