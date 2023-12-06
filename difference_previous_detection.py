import os
import re
import arcpy


def diff_prev_detection(polygon, erase_poly, output):
    """
    Remove the damage detection polygons for the previous years from the current year
    :param str polygon: The input shapefile from where the previous detection will be erased
    :param str erase_poly: The feature class with the merged previous detection
    :param str output: The output feature class with the previous detection erased
    :return: No return, the output file is saved in the database
    """
    print('Remove detection previous years')

    # Search for current year
    current_year = re.findall(r"(?<!\d)\d{4}(?!\d)", polygon)[0]

    print(f'Using past_detection_{current_year}')
    arcpy.PairwiseErase_analysis(in_features=polygon,
                                 erase_features=erase_poly,
                                 out_feature_class=output)
