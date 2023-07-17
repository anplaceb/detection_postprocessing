import os
import forest_mask
import area_filter
import morphological_operations
import raster_to_polygon
import agri_areas
import local_spatial_overlapping
import difference_previous_detection

import arcpy
arcpy.env.overwriteOutput = True

# Parameters
in_folder = r"D:\wsf-sat\methods\detection\gee"
output_folder = r"D:\wsf-sat\methods\postprocessing\test"
temp_folder = os.path.join(output_folder, "temp")
temp_list = ["0_tree_mask", "1_morphological_operations", "2_raster_to_polygon",
             "3_area_filter", "4_postprocessing_polygon"]
tree_mask = r"D:\wsf-sat\data\forestmask\fnews\V5_TCD_2015_Germany_10m_S2Al_32632_Mdlm_TCD50_2bit_FADSL_mmu25_2_0_TCD2018_WM_V5_2_0.tif"
# downloaded from https://atlas.thuenen.de/layers/fnews_holzbodenmaske_2018_32632:geonode:fnews_holzbodenmaske_2018_32632

# Create temp folder and sub-folders inside
if not os.path.isdir(temp_folder):
    os.mkdir(temp_folder)

[os.mkdir(os.path.join(temp_folder, name)) for name in temp_list if not os.path.isdir(os.path.join(temp_folder, name))]

# List files


input_list = [file for file in os.listdir(in_folder) if file.endswith('.tif')]
print(f'input files: {input_list}')


def main(name):
    for f in input_list:
        print(f'Input file is {f}')

        # apply forest mask
        detection_tree_mask = forest_mask.apply_forest_mask(raster=os.path.join(in_folder, f), tree_mask=tree_mask)
        detection_tree_mask.save(os.path.join(output_folder, temp_folder, temp_list[0], f'{temp_list[0]}_{f}'))

        # morphological operations
        morphological = morphological_operations.morph_op(raster=detection_tree_mask, number_cells=1, zone_set=[1])
        morphological.save(os.path.join(output_folder, temp_folder, temp_list[1], f'{temp_list[1]}_{f}'))

        # raster to polygon
        raster_to_polygon.raster2poly()

        # area filter
        area_filter.fun_area_filter()

        # agri area
        agri_areas.agri_areas()

        # if local mlocal spatial overlapping
        local_spatial_overlapping.spatial_overlapping()

        # difference previous
        difference_previous_detection.diff_prev_detection()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
