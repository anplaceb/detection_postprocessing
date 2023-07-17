import os
import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")


def apply_forest_mask(raster, tree_mask):
    print('Apply forest mask')
    raster_tree_mask = Raster(raster) * tree_mask
    return raster_tree_mask

