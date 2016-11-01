

import sys
print "Running script against: {}".format(sys.version)

# the arguments noted below as sys.argv[1] and sys.argv[2] are passed in the cmd script "SubfieldDNDC01_reproject_join.cmd".
# They refer to the two files, the Iowa subfield feature class and the txt file containing the
# attributes (profit and DNDC data)

import arcpy
from arcpy import env
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

print("Reprojecting feature class " + str(sys.argv[1]) + " ...")

# reproject the feature class to NAD 83 UTM Zone 15N
# the feature class used here has already a field called
# cluid_mukey that will be used as unique identifyer for the join.
in_dataset = sys.argv[1]
out_dataset = str(in_dataset) + "_Projected"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system is " + str(spatialRef.Name) +".")
print("Fields in feature class:")

# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name

print("Saving table " + str(sys.argv[2]) + " to Geodatabase...")     
# import txt file into database
in_table = "C:/Users/ebrandes/Documents/dndc/tables/05_dndc_clumu_cgsb_swg.txt"
out_path = "C:/Users/ebrandes/Documents/ia_clumu/ia_clumu.gdb"
out_name = "ProfitDNDC"
TableToTable_conversion(in_table, out_path, out_name)


print("Joining with profit and DNDC data ...")

# join with the imported table data
in_feature_class = featureClass
in_field = "cluid_mukey" 
join_table = out_name
join_field = "cluid_mukey"
field_list = ["fips", "mukey", "clumuha	mean_profit_ha", "ave_no3_leach_ha_cgsb", "ave_no3_leach_ha_swg_7500",
              "ave_no3_leach_ha_swg_10000", "ave_no3_leach_ha_swg_12500"]  

arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field_list)

# repair Geometry of feature class:
print("Repairing feature class geometry ...")
arcpy.RepairGeometry_management(in_feature_class)

# if MultipartToSinglepart does not work:
# e.g. ExecuteError: ERROR 000072: Cannot process feature with OID 822481:
# see script SubfieldSwg01delete_split_IDLE.py for a work-around.


print("Splitting multipart features ...")
# there are multipart polygons in the feature class that consist of one record (one cluid_mukey) but multiple polygons.
# Since we have to look at each polygon individually for its size and position in relation to others, we need to
# split all multipart polygons into singlepart polygons.
# The result is that there are duplicate records for some of the cluid_mukey records.
in_feature_class = featureClass
out_feature_class = str(in_dataset) + "_single"
arcpy.MultipartToSinglepart_management(in_feature_class, out_feature_class)
print("")
print("Done. Yippie!")





