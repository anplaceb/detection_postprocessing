import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def morph_op(raster, number_cells, zone_set):
    print('Morphological operations')

    # Execute Closing to remove holes
    expand_closing = Expand(raster, number_cells, zone_set)
    shrink_closing = Shrink(expand_closing, number_cells, zone_set)

    # Execute Opening to remove thin connections and small protrusions
    shrink_opening = Shrink(shrink_closing, number_cells, zone_set)
    expand_opening = Expand(shrink_opening, number_cells, zone_set)

    return expand_opening

