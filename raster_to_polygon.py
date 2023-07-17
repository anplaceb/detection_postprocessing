
def raster2poly():
    print('Raster to polygon')

    # Extract value 1 (damage)
    print("Extract value 1")
    extract_damage = ExtractByAttributes(outShrink_op, "Value = {}".format(value_damage))
    save_function(extract_damage, temp_folder, temp_list[2], temp_list[2] + "_" + f)

    shp_final_path_name = os.path.splitext(raster_final_path_name)[0] + '.shp'
    out = arcpy.RasterToPolygon_conversion(in_raster=raster_damaged_class,
                                           out_polygon_features=shp_final_path_name,
                                           simplify="NO_SIMPLIFY",
                                           raster_field="Value",
                                           create_multipart_features="SINGLE_OUTER_PART",
                                           max_vertices_per_feature="")