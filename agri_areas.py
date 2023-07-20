import arcpy


def agri_areas(polygon, agri, output):
    print('Remove detection from agriculture areas')
    arcpy.PairwiseErase_analysis(polygon, agri, output)
