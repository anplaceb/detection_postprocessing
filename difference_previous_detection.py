import os
import re
import arcpy


def diff_prev_detection(polygon, output, past_files_path):
    """Removes the damage detection from previous years.
    """
    print('Remove detection previous years')

    # Search for current year
    year = re.findall(r"(?<!\d)\d{4}(?!\d)", polygon)[0]
    arcpy.PairwiseErase_analysis(in_features=polygon,
                                 erase_features=os.path.join(past_files_path, f'past_detection_{year}'),
                                 out_feature_class=output
                                 )





