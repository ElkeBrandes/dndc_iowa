# in this script, the raster layer N_loss_reduction that includes the N loss reduction from
# the status quo (2012-2015 in corn/sy) and the medium yielding (10,000 kg ha-1) switchgrass integration
# (2006-2015, switchgrass in areas < US$ -150 ha-1 and > 60 kg ha-1) is clipped to
# single counties (Butler, Greene, and Delaware) to be able to zoom into the pattern of subfield switchgrass areas
# and reduction amounts

print("Running script ...")

import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

# make a feature layer from the county selected from the county feature class
in_features = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb\\Counties"
out_layer = "IA023_Butler"
fips_select = "IA023"
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)

# clip the subfield N loss reduction raster to the selected county boundaries
in_raster = "N_loss_reduction"
clip_features = out_layer
out_raster = "N_loss_reduction_IA023"
#arcpy.Clip_management(in_raster, "#", out_raster, clip_features, "#", "ClippingGeometry")

# make a feature layer from the county selected from the county feature class
in_features = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb\\Counties"
out_layer = "IA055_Delaware"
fips_select = "IA055"
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)

# clip the subfield N loss reduction raster to the selected county boundaries
#in_raster = "N_loss_reduction"
#clip_features = out_layer
#out_raster = "N_loss_reduction_IA055"
#arcpy.Clip_management(in_raster, "#", out_raster, clip_features, "#", "ClippingGeometry")

# make a feature layer from the county selected from the county feature class
#in_features = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb\\Counties"
#out_layer = "IA073_Greene"
#fips_select = "IA073"
#where_clause = '"fips"' + " = '" + str(fips_select) + "'"
#arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)

# clip the subfield N loss reduction raster to the selected county boundaries
#in_raster = "N_loss_reduction"
#clip_features = out_layer
#out_raster = "N_loss_reduction_IA073"
#arcpy.Clip_management(in_raster, "#", out_raster, clip_features, "#", "ClippingGeometry") 
