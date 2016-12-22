# in this script, the raster layer N_loss_reduction that includes the N loss reduction from
# the status quo (2012-2015 in corn/soy) and the medium yielding (10,000 kg ha-1) switchgrass integration
# (2006-2015, switchgrass in areas < US$ -150 ha-1 and > 60 kg ha-1) is clipped to
# the North Racoon River watershed to be able to zoom into the pattern of subfield switchgrass areas
# and reduction amounts

print("Running script ...")
print("")
import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

print("Importing watershed shapefile ...")
print("")
# import the required watershed shapefile into the file geodatabase
in_features = "C:/Users/ebrandes/Documents/geodata/shapefiles/wbdhu12_a_07100006.shp"
out_path = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"
out_name = "HUC12_07100006"
arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)

print("Reprojecting watershed feature class ...")
print("")
# reproject the feature class
in_dataset = "HUC12_07100006"
out_dataset = "HUC12_07100006_NAD83"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system is " + str(spatialRef.Name) +".")

print("Selecting impared watersheds from the North Racoon River and dissolving into one feature ...")
print("")
# make a feature layer from the HUC12 watershed selected from the watershed feature class
in_features = out_dataset
out_layer = "NorthRacoonRiver"
where_clause = '"HUC12" IN' + "('071000060101', '071000060102', '071000060103', '071000060201', '071000060202', '071000060203', \
'071000060204', '071000060205', '071000060206', '071000060207', '071000060208', '071000060301', '071000060302', \
'071000060303', '071000060304', '071000060305', '071000060306', '071000060307', '071000060308', '071000060309', '071000060310', \
'071000060403', '071000060801')"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)

# dissolve the features in the feature layer to one feature
in_features = "NorthRacoonRiver"
out_feature_class = "NorthRacoonRiverOne"
arcpy.Dissolve_management(in_features, out_feature_class)

print("Clipping N loss raster to watershed ...")
print("")
# clip the subfield N loss reduction raster to the selected watershed boundaries
in_raster = "N_loss_reduction"
clip_features = "NorthRacoonRiverOne"
out_raster = "N_loss_reduction_NRW"
arcpy.Clip_management(in_raster, "#", out_raster, clip_features, "#", "ClippingGeometry")

print("Importing water body and river feature classes ...")
print("")
# import other features into the database:
# water bodies
in_features = "C:/Users/ebrandes/Documents/geodata/dtl_wat.gdb/dtl_wat"
out_path = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"
out_name = "Waterbody"
arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)
# rivers
in_features = "C:/Users/ebrandes/Documents/geodata/dtl_riv.gdb/dtl_riv"
out_path = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"
out_name = "Rivers"
arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)

print("Reprojecting water body and river feature classes ...")
print("")
# reproject the feature classes
in_dataset = "Waterbody"
out_dataset = "Waterbody_NAD83"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system of " + str(out_dataset) + " is " + str(spatialRef.Name) +".")
print("")

# reproject the feature classes
in_dataset = "Rivers"
out_dataset = "Rivers_NAD83"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system of " + str(out_dataset) + " is " + str(spatialRef.Name) +".")
print("")

print("Clipping water body and river feature classes to watershed boundaries ...")
print("")
# clip feature classes to watershed boundaries
in_features = "Waterbody_NAD83"
clip_features = "NorthRacoonRiverOne"
out_feature_class = "Waterbody_NRW"
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# clip feature classes to watershed boundaries
in_features = "Rivers_NAD83"
clip_features = "NorthRacoonRiverOne"
out_feature_class = "Rivers_NRW"
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

print("All done!")
