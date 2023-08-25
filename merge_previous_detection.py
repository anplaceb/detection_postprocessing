import os
import re
import arcpy


def merge_prev_detection(polygon, output):
    print('Merge previous detection')
    print(f'Polygon:{polygon}')
    # List all files in the folder of polygon
    folder_files = os.path.split(polygon)[0]  # folder containing polygons all years
    list_files = [os.path.join(folder_files, file) for file in os.listdir(folder_files) if file.endswith('.shp')]
    print(f'list files: {list_files}')
    print(f'folder files {folder_files}')
    # List only polygons from previous years as the actual year
    past_polygons = list_files[0:list_files.index(polygon)]  # the list is in temporal order # NO!!!!!!
    print(f'past polygons of file {polygon}: {past_polygons}')

    year = re.findall(r"(?<!\d)\d{4}(?!\d)", polygon)[0]  # search for current year for later saving names
    print(year)

    if past_polygons:  # the first year has not previous detection, nothing to remove
        # merge and save past year/s detection
        arcpy.Merge_management(inputs=past_polygons,
                               output=os.path.join(output, f'past_detection_{year}.shp'))
    else:
        pass

