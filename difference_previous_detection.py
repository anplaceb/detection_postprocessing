import os
import re
import arcpy


def diff_prev_detection(polygon, erase_poly, output):
    """Removes the damage detection from previous years.
    """
    print('Remove detection previous years')

    # Search for current year
    year = re.findall(r"(?<!\d)\d{4}(?!\d)", polygon)[0]

    print(f'Using past_detection_{year}')
    arcpy.PairwiseErase_analysis(in_features=polygon,
                                 erase_features=erase_poly,
                                 out_feature_class=output
                                 )





