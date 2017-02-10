# this script can be used to join data from a txt file to the attribute table of a feature class.

# I calculated total N loss (sum of NO3 leaching and NH3 volatilization) in PostgreSQL and exported it into
# the tables folder on the VM. The below script is modified from the script SubfieldDNDC02join_rent_profit_2015
# only in changing the table and field input names

import sys
print "Running script against: {}".format(sys.version)
import arcpy
from arcpy import env

# variables assigned in this script:
# path of txt file location (it should not change usually, therefore I don't pass it with the cmd script)
table_path = "C:/Users/ebrandes/Documents/dndc/tables/"
# path of the working directory where the imported table should be saved
work_path = "C:/Users/ebrandes/Documents/ia_clumu/ia_clumu.gdb"
# the field name of the join field (I use the same for both join fields)
join_field = "cluid_mukey"

# arguments passed in the cmd script:
# sys.argv[1] is the clumu feature class in the database "ia_clumu_2016_single"
# sys.argv[2] is the name of the txt file to be joined
# sys.argv[3] is the name of the table in the gdb
# sys.argv[4] is the name of the newly joined field

# the arguments noted below as sys.argv[1] and sys.argv[2] are passed in the cmd script "SubfieldDNDC01_reproject_join.cmd".
# They refer to the two files, the Iowa subfield feature class and the txt file containing the
# attributes (profit and DNDC data)

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = work_path

# check the spatial reference of the feature class to be used to join the data:
featureClass = sys.argv[1]
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
in_table = str(table_path) + str(sys.argv[2])
out_path = work_path
out_name = sys.argv[3]
arcpy.TableToTable_conversion(in_table, out_path, out_name)

print("")
print("Joining with attribute data ...")

# join with the imported table data
in_feature_class = featureClass
in_field = join_field # same as join_field assigned above
join_table = out_name
field = sys.argv[4]

arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field)

print("")
print("Done. Yippie!")





