"""
Postprocessing of damage detection.
Postprocessing includes clip to tree mask from FNEWS project, morphological operations in raster, vectorize,
remove detection in agriculture areas, remove detection from previous years, morphological operations in vector and
filter area.
Input: Folder with raster(s) with class damage (1) and no damage (0 or NA).
Output: Polygons with damage detection after postprocessing.
:param str input_folder: The folder path with the detection raster files with class damage (1) and no damage
(0 or NA) and with year of detection in the name
:param str output_folder: The folder path for the resulting damage detection polygons
:param str tree_mask: The file path to the tree mask (Holzbodenmaske FNEWS)
https://atlas.thuenen.de/layers/fnews_holzbodenmaske_2018_32632:geonode:fnews_holzbodenmaske_2018_32632
:param agri_areas_poly: The file path to the "Agrarfoerderung" areas, downloaded from
https://sla.niedersachsen.de/landentwicklung/LEA/  Download -> Agrarfoerderung -> Feldbloecke
:param int min_area: The minimal area of the damage polygons in ha, used to filter.
"""

import os
import re
import forest_mask
import morphological_operations
import raster_to_polygon
import agri_areas
import area_filter
import merge_previous_detection
import difference_previous_detection
import dissolve_poly
import buffer
import arcpy

# Paths input output
input_folder = r"D:\wsf-sat\test\input"
output_folder = r"D:\wsf-sat\test\output"

# Tree mask and agriculture areas
tree_mask = r"P:\WSF-SAT\Permanent\Daten\Postprocessing_Skript\Holzbodenmaske_FNEWS.tif"
agri_areas_poly = r"P:\WSF-SAT\Permanent\Daten\Postprocessing_Skript\Agrar_NDS_2023.shp"

# Parameter
min_area = 0.25

if not os.path.isdir(os.path.join(output_folder, "Postprocessing.gdb")):
    arcpy.CreateFileGDB_management(output_folder, "Postprocessing")

# Environment
arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.path.join(output_folder, "Postprocessing.gdb")

temp_folder = os.path.join(output_folder, "temp")
temp_list = ["0_tree_mask", "1_morpho_op", "2_raster2poly", "3_agri_erase", "4_dissolve", "5_area_filter",
             "6_merge_past",
             "7_diff_previous", "8_dissolve"]

# Create temp folder and sub-folders inside
if not os.path.isdir(temp_folder):
    os.mkdir(temp_folder)

# List files
input_list = [file for file in os.listdir(input_folder) if file.endswith('.tif')]
print(f'input files: {input_list}')

# search for first year of detection
first_year = re.findall(r"(?<!\d)\d{4}(?!\d)", input_list[0])[0]
# first element of the list is first year, regex to isolate year from the file name
print(f'First year:{first_year}')


def main():
    for f in input_list:

        print(f'Postprocessing file {f}')

        year = re.findall(r'(?<!\d)\d{4}(?!\d)', f)[0]  # returns list with 1 element, [0] to unlist
        print(f'Year: {year}')

        # apply forest mask
        detection_tree_mask = forest_mask.apply_forest_mask(raster=os.path.join(input_folder, f),
                                                            tree_mask=tree_mask)
        f = f[:-4]  # remove ending because using gdb
        detection_tree_mask.save(f'tree_mask_{f}')

        # morphological operations
        morphological = morphological_operations.morph_op(raster=detection_tree_mask, number_cells=1, zone_set=[1])
        morphological.save(f'morphological_{f}')

        # raster to polygon
        raster_to_polygon.raster2poly(raster=morphological, value_damage=1, year=year, output=f'raster2poly_{f}')

        # remove detection from agriculture areas
        agri_areas.agri_areas(polygon=f'raster2poly_{f}',
                              agri=agri_areas_poly,
                              output=f'agri_erase_{f}')

        # Dissolve polygons and multipart to single part before area filtering
        dissolve_poly.fun_poly_dissolve(polygon=f'agri_erase_{f}', output=f'dissolve_{f}')

        # area filter now and at the last step to avoid removing correct detections in the next step where previous
        # detected areas are removed from the present year
        area_filter.fun_area_filter(polygon=f'dissolve_{f}', min_area=min_area,
                                    output=os.path.join(temp_folder, f'area_filter_{f}.shp'))

        # if detection of the first year save to final results because the next steps (removing previous detection)
        # are not necessary
        if year == first_year:
            print(f'Year {year} is first year')
            area_filter.fun_area_filter(polygon=f'dissolve_{f}', min_area=min_area,
                                        output=os.path.join(output_folder, f'detection_{f}_postprocessing'))

        elif year != first_year:
            # merge previous detection
            merge_previous_detection.merge_prev_detection(polygon=os.path.join(temp_folder, f'area_filter_{f}.shp'),
                                                          output=f'past_detection_{year}')

            # difference previous
            difference_previous_detection.diff_prev_detection(
                polygon=os.path.join(temp_folder, f'area_filter_{f}.shp'), erase_poly=f'past_detection_{year}',
                output=f'diff_previous_{f}')

            # Dissolve polygons and multipart to single part before area filtering
            dissolve_poly.fun_poly_dissolve(polygon=f'diff_previous_{f}', output=f'dissolve_{f}')

            # Closing
            buffer.buffer_vect(polygon=f'dissolve_{f}', buffer_dist="-1 Meters", output=f'closing1_{f}')
            buffer.buffer_vect(polygon=f'closing1_{f}', buffer_dist="1 Meters", output=f'closing2_{f}')

            # Opening
            buffer.buffer_vect(polygon=f'closing2_{f}', buffer_dist="1 Meters", output=f'opening1_{f}')
            buffer.buffer_vect(polygon=f'opening1_{f}', buffer_dist="-1 Meters", output=f'opening2_{f}')

            # for all years but the first, save (first year is saved previously)
            area_filter.fun_area_filter(polygon=f'dissolve_{f}',
                                        min_area=min_area,
                                        output=os.path.join(output_folder, f'detection_{f}_postprocessing'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
