import arcpy
from arcpy import env
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

featureClass = "ia_clumu_2016_single"
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system is " + str(spatialRef.Name) +".")
print("Fields in feature class:")

# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name
