import os
import re
import arcpy


def diff_prev_detection(polygon, output, past_files_path, first_year):
    """Removes the damage detection from previous years.
    """
    print('Remove detection previous years')

    # List only polygons from previous years as the actual year
    year = re.findall(r"(?<!\d)\d{4}(?!\d)", polygon)[0]  # search for current year for later searching for past
    # detection
    if year != first_year:
        arcpy.PairwiseErase_analysis(in_features=polygon,
                                     erase_features=os.path.join(past_files_path, f'past_detection_{year}'),
                                     out_feature_class=output
                                     )

    else:
        pass
        # the first year has not previous detection, nothing to remove
        # erase past detection

