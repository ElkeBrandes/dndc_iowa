# in this script, the feature class containing subfield areas (single polygons) and several joined attributes
# related to N loss is clipped to the delineation of a certain county. The county feature class is located in 
# a different geodatabase, but can still be used to clip the subfield feature class in the work directory.
# We just have to make sure to include the path to the county feature class.

print("Running script ...")
print("")
import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

# enter the fips of the county that should be selected
fips_select = "IA013"

# make a feature layer from the county selected from the county feature class
in_features = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb\\Counties"
out_layer = str(fips_select) + "_layer"
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)


print("Clipping subfield feature class to county feature class ...")
print("")

in_features = "ia_clumu_2016_single"
clip_features = out_layer
out_feature_class = "clumu_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# list the fields and types of the clipped feature class

field_list = arcpy.ListFields(out_feature_class)

for field in field_list:
    print("{0} is of type {1}"
          .format(field.name, field.type))

# there are a lot of null values in the joined data, for those polygons that were not in
# corn and/or soybeans from 2012 to 2015. I can delete them before doing further
# calculations to avoid errors later on.

print("Deleting polygons with <Null> values ...")
print("")

feature_class = out_feature_class
area_field = "SHAPE_Area"
value_field_1 = "ave_no3_leach_change_perc_10000_12"
value_field_2 = "ave_no3_leach_change_perc_10000_2"
where_clause = '"' + value_field_1 + '" IS NULL'

with arcpy.da.UpdateCursor(feature_class, (value_field_1, value_field_2), where_clause) as cursor:
    for row in cursor:
        cursor.deleteRow()

