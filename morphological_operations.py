import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def morph_op(raster, number_cells, zone_set):
    """
    Perform morphological operations on raster: closing followed by opening
    :param str raster: The input raster for which the identified zones are to be expanded. It must be of integer type
    :param int number_cells: The number of cells to expand each specified zone by
    :param list zone_set: The list of zone values to expand
    :return: Raster after the morphological operations of closing and opening
    """
    print('Morphological operations')

    # Execute Closing to remove holes
    expand_closing = Expand(raster, number_cells, zone_set)
    shrink_closing = Shrink(expand_closing, number_cells, zone_set)

    # Execute Opening to remove thin connections and small protrusions
    shrink_opening = Shrink(shrink_closing, number_cells, zone_set)
    expand_opening = Expand(shrink_opening, number_cells, zone_set)

    return expand_opening

