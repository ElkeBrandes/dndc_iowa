# in this script, the feature class containing subfield areas (single polygons) and several joined attributes
# related to N loss is clipped to
# the North Racoon River watershed to then calculate the average N loss reduction with switchgrass integration
# in that watershed.
# using the prepared feature "NorthRacoonRiverOne" from script "SubfieldDNDC05_clip_watershed.py"

print("Running script ...")
print("")
import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

print("Clipping subfield feature class to watershed feature class ...")
print("")

in_features = "ia_clumu_2016_single"
clip_features = "NorthRacoonRiverOne"
out_feature_class = "clumu_NRW"
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
value_field = "ave_n_loss_change_perc_10000"
where_clause = '"' + value_field + '" IS NULL'

with arcpy.da.UpdateCursor(feature_class, (value_field,), where_clause) as cursor:
    for row in cursor:
        cursor.deleteRow()


print("Calculating area weighted average of percent N loss reduction ...")
print("")

# using the data access module (da) I run the cursor through the field data and calculate
# area weighted average

num = 0
denom = 0
with arcpy.da.SearchCursor(feature_class, (area_field, value_field)) as cursor:
    for row in cursor:
        product = (row[0]*row[1])
        num += product 
        denom += row[0]

weighted_mean = round(num / denom, 2)
print("Area weighted mean N loss reduction for the North Racoon River Watershed is "
      + str(abs(weighted_mean)) + " %.")
        

print("Calculating area in switchgrass in the watershed ...")
print("")

n_loss_field = "ave_n_loss_change_10000"
total_area = 0
swg_area = 0
with arcpy.da.SearchCursor(feature_class, (area_field, n_loss_field)) as cursor:
    for row in cursor:
        total_area += row[0]
        if row[1] < 0: # filtering for negative values indicating N loss reduction
            swg_area += row[0]
swg_perc = swg_area / total_area
print("Area in switchgrass is " + str(swg_perc) + " %.")
       

