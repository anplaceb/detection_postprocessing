import forest_mask
import area_filter_raster
import morphological_operations
import raster_to_polygon
import agri_areas
import local_spatial_overlapping
import difference_previous_detection


def main(name):
    # apply forest mask
    forest_mask.apply_forest_mask()

    # morphological operations
    morphological_operations.morphological_operations()

    # area filter
    area_filter_raster.fun_area_filter_raster()

    # raster to polygon
    raster_to_polygon.raster2poly()

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
