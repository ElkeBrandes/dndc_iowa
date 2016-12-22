# in this script, the raster layer N_loss_reduction that includes the N loss reduction from
# the status quo (2012-2015 in corn/soy) and the medium yielding (10,000 kg ha-1) switchgrass integration
# (2006-2015, switchgrass in areas < US$ -150 ha-1 and > 60 kg ha-1) is clipped to
# the North Racoon River watershed to be able to zoom into the pattern of subfield switchgrass areas
# and reduction amounts

print("Running script ...")

import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

# import the required watershed shapefile into the file geodatabase

in_features = "C:/Users/ebrandes/Documents/dndc/shapefiles/wbdhu12_a_07100006.shp"
out_path = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"
out_name = "HUC12_07100006"
arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)

# make a feature layer from the HUC12 watershed selected from the watershed feature class
in_features = "HUC12_07100006"
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

# clip the subfield N loss reduction raster to the selected watershed boundaries
in_raster = "N_loss_reduction"
clip_features = "NorthRacoonRiverOne"
out_raster = "N_loss_reduction_NRW"
arcpy.Clip_management(in_raster, "#", out_raster, clip_features, "0", "ClippingGeometry")
