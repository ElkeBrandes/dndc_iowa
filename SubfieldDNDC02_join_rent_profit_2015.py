

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

# starting with the feature class ia_clumu_2016_single (that I joined mean profit and no3 leaching
# to by running script SubfieldDNDC01reproject_join_mean_profit_no3.py, I join the cash rents and profit
# calculated for 2015.





# check the spatial reference of the feature class to be used to join the data:
featureClass = "ia_clumu_2016_single"
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system is " + str(spatialRef.Name) +".")
print("")
print("Fields in feature class:")
print("")
# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name

print("")
print("Saving table containing attributes to Geodatabase...")     
# import txt file into database (txt file was exported from PostgreSQL database)
in_table = "C:/Users/ebrandes/Documents/dndc/tables/clumu_rent_profit_2015.txt"
out_path = "C:/Users/ebrandes/Documents/ia_clumu/ia_clumu.gdb"
out_name = "RentProfit2015"
arcpy.TableToTable_conversion(in_table, out_path, out_name)

print("")
print("Joining with profit and DNDC data ...")

# join with the imported table data
in_feature_class = featureClass
in_field = "cluid_mukey" 
join_table = out_name
join_field = "cluid_mukey"
field_list = ["clu_cash_rent_csr2", "profit_csr2"]  

arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field_list)

print("")
print("Done. Yippie!")




