""" Spatial merge of (sentinel) tiles."""

import os
import arcpy

arcpy.env.overwriteOutput = True

# Paths
input_folder = r"D:\wsf-sat\temp\test"
output_folder = r"D:\wsf-sat\temp\output"
temp_folder = os.path.join(output_folder, "temp", "0_merge")

# Create temp folder and sub-folders inside
if not os.path.isdir(temp_folder):
    print(f"{temp_folder} gibt es nicht")
    os.makedirs(temp_folder)

# List files
input_list = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.shp')]
print(f'input files: {input_list}')

# Merge
merge = arcpy.Merge_management(inputs=input_list,
                               output=os.path.join(temp_folder, 'merge.shp'))

# Dissolve
arcpy.Dissolve_management(in_features=merge,
                          out_feature_class=os.path.join(output_folder, 'merge_dissolve.shp'),
                          multi_part="SINGLE_PART")

