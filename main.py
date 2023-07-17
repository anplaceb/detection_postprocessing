import os
import forest_mask
import area_filter_raster
import morphological_operations
import raster_to_polygon
import agri_areas
import local_spatial_overlapping
import difference_previous_detection

# Parameters
in_folder = r"D:\wsf-sat\methods\detection\gee"
output_folder = r"D:\wsf-sat\methods\postprocessing\nbr_threshold_gee"
temp_list = ["0_tree_mask", "1_morphological_operations", "2_raster_to_polygon",
             "3_area_filter", "4_postprocessing_polygon"]

# Create temp folder and sub-folders inside
temp_folder = os.path.join(output_folder, "temp")
if not os.path.isdir(temp_folder):
    os.mkdir(temp_folder)

[os.mkdir(os.path.join(temp_folder, name)) for name in temp_list if not os.path.isdir(os.path.join(temp_folder, name))]


def main(name):
    print(in_folder)
    # apply forest mask
    forest_mask.apply_forest_mask()

    # morphological operations
    morphological_operations.morphological_operations()

    # raster to polygon
    raster_to_polygon.raster2poly()

    # area filter
    area_filter_raster.fun_area_filter_raster()

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
