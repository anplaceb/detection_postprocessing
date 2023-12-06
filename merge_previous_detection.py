import os
import re
import arcpy


def merge_prev_detection(polygon, output):
    """
    Merge the detection previous to the current detection year. It searches in the folder where the input file is for
    files from previous years, and it merges them
    :param str polygon: The input detection shapefile from the current year
    :param str output: The output feature class is the merged detection from the years previous to the input
    :return: No return, the output file is saved in the database
    """
    print(f'Merge previous detection for polygon: {polygon}')

    # List all files in the folder of polygon
    folder_files = os.path.split(polygon)[0]  # folder containing polygons all years
    list_files = [os.path.join(folder_files, file) for file in os.listdir(folder_files) if file.endswith('.shp')]

    # List only polygons from previous years as the actual year
    past_polygons = list_files[0:list_files.index(polygon)]  # the list is in temporal order
    print(f'past polygons of file {os.path.basename(polygon)}: '
          f'{list(map(os.path.basename, past_polygons))}')

    if past_polygons:
        # merge and save past year/s detection
        print(f"Merging {list(map(os.path.basename, past_polygons))}")
        arcpy.Merge_management(inputs=past_polygons,
                               output=output)
    else:
        pass

