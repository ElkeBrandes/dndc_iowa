import sys

import arcpy
from arcpy import env
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

featureClass = "ia_clumu_2016_single"
# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name
print(" ")
print("deleting fields...")
print(" ")
in_table = featureClass
drop_field = ["mean_profit_ha",
              "ave_no3_leach_ha_cgsb",
              "ave_nh3_vol_ha_cgsb",
              "ave_no3_leach_change_perc_10000_1",
              "ave_no3_leach_change_perc_10000_2",
              "mean_profit_ha_1",
              "ave_no3_leach_ha_cgsb_1",
              "ave_nh3_vol_ha_cgsb_1",
              "ave_no3_leach_change_perc_10000_12",
              "ave_no3_leach_change_perc_10000_23"]
arcpy.DeleteField_management(in_table, drop_field)

featureClass = "ia_clumu_2016_single"
# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name
print(" ")    
print("done.")
