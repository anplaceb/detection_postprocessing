import os
import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def apply_forest_mask(raster, tree_mask):
    """
    Apply tree mask to the input image
    :param str raster: raster with damage detection
    :param str tree_mask: Tree mask with value 1 where trees
    :return: The input raster clipped to the tree mask
    """
    print('Apply forest mask')
    raster_tree_mask = Raster(raster) * tree_mask
    return raster_tree_mask

