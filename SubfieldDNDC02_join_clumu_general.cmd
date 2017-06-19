:: arguments:
 
:: sys.argv[1] is the clumu feature class in the database "ia_clumu_2016_single"
:: sys.argv[2] is the name of the txt file to be joined
:: sys.argv[3] is the name of the table in the gdb
:: sys.argv[4] is the name of the newly joined field or field list if > 1 field is joined. Format: "Field" or ["Field1", "Field2"]



C:\Python27\ArcGISx6410.3\python.exe C:\Users\ebrandes\Documents\DNDC\dndc_iowa\SubfieldDNDC02_join_clumu_general.py "ia_clumu_2016_single" "dndc_clumu_profit_dndc.txt" "NO3_leach_change" ["mean_profit_ha", "ave_no3_leach_ha_cgsb", "ave_nh3_vol_ha_cgsb", "ave_no3_leach_change_perc_10000_1", "ave_no3_leach_change_perc_10000_2"]
