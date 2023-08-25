"""Postprocessing"""

import os
import re
import forest_mask
import morphological_operations
import raster_to_polygon
import agri_areas
import area_filter
import merge_previous_detection
import difference_previous_detection
import arcpy

arcpy.env.overwriteOutput = True

# Paths input output
input_folder = r"D:\wsf-sat\methods\threshold_analysis\02_thresholds\m15"
output_folder = r"D:\wsf-sat\methods\threshold_analysis\03_postprocessing\m15"
temp_folder = os.path.join(output_folder, "temp")
temp_list = ["0_tree_mask", "1_morpho_op", "2_raster2poly", "3_agri_erase", "4_area_filter", "5_merge_past",
             "6_diff_previous"]

# Tree mask and agriculture areas
tree_mask = r"D:\wsf-sat\data\forestmask\fnews\V5_TCD_2015_Germany_10m_S2Al_32632_Mdlm_TCD50_2bit_FADSL_mmu25_2_0_TCD2018_WM_V5_2_0.tif"
# downloaded from https://atlas.thuenen.de/layers/fnews_holzbodenmaske_2018_32632:geonode:fnews_holzbodenmaske_2018_32632
agri = r"D:\wsf-sat\data\agri_areas\Agrar_NDS_2023.shp"
# downloaded from https://sla.niedersachsen.de/landentwicklung/LEA/  Agrarfoerderung -> Feldbloecke

# Create temp folder and sub-folders inside
if not os.path.isdir(temp_folder):
    os.mkdir(temp_folder)

[os.mkdir(os.path.join(temp_folder, name)) for name in temp_list if not os.path.isdir(os.path.join(temp_folder, name))]

# List files
input_list = [file for file in os.listdir(input_folder) if file.endswith('.tif')]
print(f'input files: {input_list}')

# search for first year of detection
first_year = re.findall(r"(?<!\d)\d{4}(?!\d)", input_list[0])[0]
# first element of the list is first year, regex to isolate year from the file name
print(f'First year:{first_year}')
def main(name):
    for f_tif in input_list:
        print(f'Postprocessing file {f_tif}')
        year = re.findall(r'(?<!\d)\d{4}(?!\d)', f_tif)[0]  # returns list with 1 element, [0] to unlist
        print(f'Year: {year}')
        f_shp = f'{os.path.splitext(f_tif)[0]}.shp'

        # apply forest mask
        detection_tree_mask = forest_mask.apply_forest_mask(raster=os.path.join(input_folder, f_tif), tree_mask=tree_mask)
        detection_tree_mask.save(os.path.join(output_folder, temp_folder, temp_list[0], f'{temp_list[0]}_{f_tif}'))

        # morphological operations
        morphological = morphological_operations.morph_op(raster=detection_tree_mask, number_cells=1, zone_set=[1])
        morphological.save(os.path.join(output_folder, temp_folder, temp_list[1], f'{temp_list[1]}_{f_tif}'))

        # raster to polygon
        raster_to_polygon.raster2poly(raster=morphological, value_damage=1, year=year,
                                      output=os.path.join(output_folder, temp_folder, temp_list[2],
                                                          f'{temp_list[2]}_{f_shp}'))

        # remove detection from agriculture areas
        agri_areas.agri_areas(polygon=os.path.join(output_folder, temp_folder, temp_list[2], f'{temp_list[2]}_{f_shp}'),
                              agri=agri,
                              output=os.path.join(output_folder, temp_folder, temp_list[3], f'{temp_list[3]}_{f_shp}'))

        # area filter now and at the last step to avoid removing correct detections in the next step where previous
        # detected areas are removed from the present year
        area_filter.fun_area_filter(polygon=os.path.join(output_folder, temp_folder, temp_list[3],
                                                         f'{temp_list[3]}_{os.path.splitext(f_shp)[0]}.dbf'),
                                    min_area=0.25, output=os.path.join(output_folder, temp_folder, temp_list[4],
                                                                       f'{temp_list[4]}_{f_shp}'))
        # if detection of the first year save to final results because the next steps (removing previous detection)
        # are not necessary
        if year == first_year:
            print('Year {year} is first year')
            area_filter.fun_area_filter(polygon=os.path.join(output_folder, temp_folder, temp_list[3],
                                                             f'{temp_list[3]}_{os.path.splitext(f_shp)[0]}.dbf'),
                                        min_area=0.25, output=os.path.join(output_folder,
                                                                           f'detection_{f_shp}_postprocessing'))

        elif year != first_year:
            # merge previous detection
            merge_previous_detection.merge_prev_detection(polygon=os.path.join(output_folder, temp_folder, temp_list[4],
                                                                               f'{temp_list[4]}_{f_shp}'),
                                                          output=os.path.join(output_folder, temp_folder, temp_list[5]))

            # difference previous
            difference_previous_detection.diff_prev_detection(polygon=os.path.join(output_folder, temp_folder, temp_list[4],
                                                                                   f'{temp_list[4]}_{f_shp}'),
                                                              past_files_path=
                                                              os.path.join(output_folder, temp_folder, temp_list[5]),
                                                              output=
                                                              os.path.join(output_folder, temp_folder, temp_list[6],
                                                                           f'{temp_list[6]}_{f_shp}'))
            # area filter again
            area_filter.fun_area_filter(polygon=os.path.join(output_folder, temp_folder, temp_list[6],
                                                             f'{temp_list[6]}_{os.path.splitext(f_shp)[0]}.dbf'),
                                        min_area=0.25, output=os.path.join(output_folder, temp_folder, temp_list[4],
                                                                           f'{temp_list[4]}_{f_shp}'))

        # for all years but the first, save (first year is saved previously)
        if year != first_year:
            area_filter.fun_area_filter(polygon=os.path.join(output_folder, temp_folder, temp_list[6],
                                                             f'{temp_list[6]}_{f_shp}'),
                                        min_area=0.25,
                                        output=os.path.join(output_folder, f'detection_{f_shp}_postprocessing'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

