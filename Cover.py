import arcpy




#******************************ROOF COVER******************************

#Identify buildings by built-up areas within one feature class.
arcpy.Identity_analysis('StructureSrf', 'SettlementSrf',r'memory\Identity')

#Calculate statistics for mean area of buildings and to get count of total building count for each built-up area.
arcpy.Statistics_analysis(r'memory\Identity', r'memory\RCStats', [['AreaSqKm','Mean'],['FID_StructureSrf','Count']],'FID_SettlementSrf')

#Join statistics to built-up area to do calculations on each area.
arcpy.JoinField_management('SettlementSrf', 'OBJECTID', r'memory\RCStats', 'FID_SettlementSrf', [['MEAN_AreaSqKm'],['COUNT_FID_StructureSrf']])

#Add fields to calculate roof coverage and then roof cover. Data type as doubles for precision.
arcpy.AddField_management('SettlementSrf', 'rCover', 'DOUBLE')
arcpy.AddField_management('SettlementSrf', 'rConc', 'DOUBLE')

#Calculate roof coverage per FM 5-33.
arcpy.CalculateField_management('SettlementSrf', 'rCvg', '((!MEAN_AreaSqKm! * !COUNT_FID_StructureSrf! / !AreaSqKm!) * 100)', 'PYTHON3')

#Calculate roof cover per FM 5-33.
arcpy.CalculateField_management('SettlementSrf', 'rCover', 'Reclass(!rCover!)', 'PYTHON3', '''
def Reclass(rCover):
    if rCvg > 40:
        return 3
    elif rCvg >=20:
        return 2
    else:
        return 1''')
arcpy.Dissolve_management('SettlementSrf', 'Roof_Concealment', 'rConc')




#******************************VEGETATION COVER******************************

#Add field for vegetation cover.
arcpy.AddField_management('VegetationSrf', 'vCover', 'LONG')

#Calculate vegetation concealment per FM 5-33.
arcpy.CalculateField_management('VegetationSrf', 'vCover', 'Reclass(!DMT!)', 'PYTHON3', '''
def Reclass(DMT):
    if DMT >= 50:
        return 3
    elif DMT < 50 and DMT >0:
        return 2    
    else:
        return -999''')

#******************************Slope Cover******************************

#Add field for slope cover.
arcpy.AddField_management('PhysiographySrf','Slope_Cover','DOUBLE')

#Calculate slope cover per FM 5-33.
arcpy.CalculateField_management('PhysiographySrf', 'Slope_Cover', 'Reclass(!Upper!, !Lower!)', 'PYTHON3', '''
def Reclass(L,U):
    if L > 30:
        return 3
    elif L > 10:
        return 2
    else:
        return 1''')



                
#******************************UNION******************************

#Combine features that overlap to do final weighted analysis.
arcpy.Union_analysis(['SettlementSrf', 'VegetationSrf', 'PhysiographySrf'], 'uCover')

#Add field for final concealment weight.
arcpy.Addfield_management('uCover', 'sumCover', 'Long')
arcpy.AddField_management('uCover', 'Cover', 'Long')

#Calculate final concealment weight based off of my own decision.
arcpy.CalculateField_management('uCover', 'Cover', 'Reclass(!rCover!, !vCover!, !sCover!, !sumCover!)' , 'PYTHON3', '''
def Reclass(r,v,s,sum):
    if sum > 

Reclass(!rCover!,!vCover!,!sCover!,!sumCover!)

def Reclass(r,v,s,sum):
 if sum > 6:
    return sum + 3
 elif max(r,v,s) == 3:
    return 9
 elif sum > 3:
    return sum + 3
 elif max(r,v,s) == 2:
    return 5
 elif sum > 0:
    return sum + 3
 elif max(r,v,s) == 1:
    return 1
arcpy.CalculateField_management('uConc','Cover','Reclass(!rConc!,!vConc!,!sConc!,!sumConc!)','PYTHON3','''
def Reclass(r,v,s,sum):
 if sum > 6:
    return sum
 elif max(r,v,s) == 3 and statistics.median(r,v,s) == 3:
    while min(r,v,s) >= 0:
        return min(r,v,s)
 elif max(r,v,s) == 3 and statistics.median(r,v,s) == 2:
    while min(r,v,s) >= 0:
        return min(r,v,s)
 elif max(r,v,s) == 3:
    while min(r,v,s) >= 0:
        return min(r,v,s)
 elif sum > 4:
    return sum
 elif max(r,v,s) == 2 and statistics.median(r,v,s) == 2:
    while min(r,v,s) >= 0:
        return min(r,v,s)
 elif max(r,v,s) == 2 and statistics.median(r,v,s) == 1:
    while min(r,v,s) >= 0:
        return min(r,v,s)
 elif max(r,v,s) == 2:
    return max(r,v,s)
 elif sum > 0:
    return sum
 else:
    return -999''')


#******************************DISSOLVE******************************

#Dissolve uConc by final concealment.
arcpy.Dissolve_management('uCover', 'Cover_Analysis', 'Cover')
                
