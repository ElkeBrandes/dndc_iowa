# in this script, the feature class containing subfield areas (single polygons) and several joined attributes
# related to N loss is used to select low leaching soils and their adjacent, normally leaching soils.
# Unlike in the previous version I am not selecting certain counties but run the analysis on the whole Iowa area.

print("Running script ...")
print("")
import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

print("List attribute data in original feature class ...")
print("")

in_features = "ia_clumu_2016_single"

# list the fields and types of the clipped feature class

field_list = arcpy.ListFields(in_features)

for field in field_list:
    print("{0} is of type {1}"
          .format(field.name, field.type))

# there are a lot of null values in the joined data, for those polygons that were not in
# corn and/or soybeans from 2012 to 2015, or nitrate leaching was not modelled. I can delete
# them before doing further calculations to avoid errors later on.

print("Deleting polygons with <Null> values ...")
print("")

area_field = "SHAPE_Area"
value_field_1 = "ave_no3_leach_change_perc_10000_12"
value_field_2 = "ave_no3_leach_change_perc_10000_2"
where_clause = '"' + value_field_1 + '" IS NULL'

with arcpy.da.UpdateCursor(in_features, (value_field_1, value_field_2), where_clause) as cursor:
    for row in cursor:
        cursor.deleteRow()
        
print("")    
print("Creating feature layer with low leaching polygons...")
print("")
# make a feature layer of all polygons that show < 0.1 kg/ha nitrate leaching
out_layer = "low_leach_polygons"
where_clause = '"ave_no3_leach_ha_cgsb" < 0.1'
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)

# make a feature class from the layer "low_leach_polygons"
in_feature = "low_leach_polygons"
out_feature = "low_leach_polygons_fc"
arcpy.CopyFeatures_management(in_feature, out_feature)

print("Dissolving low leaching polygons...")
print("")
# dissolve the selected cluid_mukey polygons in the feature layer, resulting in a feature class
in_feature = out_layer
out_feature_class = "low_leach_dissolved"
arcpy.Dissolve_management(in_features, out_feature_class, "", "","SINGLE_PART", "DISSOLVE_LINES")

print("Creating feature layer with not low leaching polygons...")
print("")
# create a layer that contains all the polygons that do not belong to the low leaching cohort
out_layer = "high_leach_polygons"
where_clause = '"ave_no3_leach_ha_cgsb" >= 0.1'
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)

print("Selecting adjacent polygons...")
print("")
# find adjacent cluid_mukey polygons in the shapefile: create a selection of the "all_polygons" layer:
in_layer = "high_leach_polygons" 
select_layer = "low_leach_dissolved"
arcpy.SelectLayerByLocation_management(in_layer, "BOUNDARY_TOUCHES", select_layer)



print("Creating feature layer with adjacent polygons leaching > 20kg/ha...")
print("")
# from this selection, make a feature layer that contains only the polygons of typical nitrate leaching (> 20 kg/ha)
in_layer = "high_leach_polygons" 
out_layer = "norm_leach_polygons"
where_clause = '"ave_no3_leach_ha_cgsb" > 20'
arcpy.MakeFeatureLayer_management(in_layer, out_layer, where_clause)

# make a feature class from the layer "norm_leach_polygons"
in_feature = "norm_leach_polygons"
out_feature = "norm_leach_polygons_fc"
arcpy.CopyFeatures_management(in_feature, out_feature)

print("Export attribute tables...")
print("")
# export attribute tables from the feature classes "norm_leach_polygons_fc" and "low_leach_polygons_fc"
Input_Feature_Class = "low_leach_polygons_fc"
Value_Fields = ["OBJECTID", "fips", "mukey", "cluid_mukey", "ave_no3_leach_ha_cgsb", "SHAPE_area"]
Delimiter = "SPACE"
Output_ASCII_File = "C:/Users/ebrandes/Documents/dndc/tables/low_leach_polygons.txt"
arcpy.ExportXYv_stats(Input_Feature_Class, Value_Fields, Delimiter, Output_ASCII_File, "ADD_FIELD_NAMES")

Input_Feature_Class = "norm_leach_polygons_fc"
Output_ASCII_File = "C:/Users/ebrandes/Documents/dndc/tables/norm_leach_polygons.txt"
arcpy.ExportXYv_stats(Input_Feature_Class, Value_Fields, Delimiter, Output_ASCII_File, "ADD_FIELD_NAMES")


# arcpy.Append_management(inputs, target)

print("Clean up...")
print("")
# clean up in memory layer
arcpy.Delete_management("low_leach_polygons")
arcpy.Delete_management("norm_leach_polygons")

# clean up interim feature classes
arcpy.Delete_management("low_leach_dissolved")
#arcpy.Delete_management("low_leach_polygons_fc")
#arcpy.Delete_management("norm_leach_polygons_fc")

print("All done!")
print("")

