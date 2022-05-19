#******************************CREATED BY ANTHONY DAVID MARANO******************************
import arcpy




#******************************ROOF CONCEALMENT******************************

#Identify buildings by built-up areas within one feature class.
arcpy.Identity_analysis('StructureSrf', 'SettlementSrf',r'memory\Identity')

#Calculate statistics for mean area of buildings and to get count of total building count for each built-up area.
arcpy.Statistics_analysis(r'memory\Identity', r'memory\RCStats', [['AreaSqKm','Mean'],['FID_StructureSrf','Count']],'FID_SettlementSrf')

#Join statistics to built-up area to do calculations on each area.
arcpy.JoinField_management('SettlementSrf', 'OBJECTID', r'memory\RCStats', 'FID_SettlementSrf', [['MEAN_AreaSqKm'],['COUNT_FID_StructureSrf']])

#Add fields to calculate roof coverage and then roof concealment. Data type as doubles for precision.
arcpy.AddField_management('SettlementSrf', 'rCover', 'DOUBLE')
arcpy.AddField_management('SettlementSrf', 'rConc', 'DOUBLE')

#Calculate roof coverage per FM 5-33.
arcpy.CalculateField_management('SettlementSrf', 'rCover', '((!MEAN_AreaSqKm! * !COUNT_FID_StructureSrf! / !AreaSqKm!) * 100)', 'PYTHON3')

#Calculate roof concealment per FM 5-33.
arcpy.CalculateField_management('SettlementSrf', 'rConc', 'Reclass(!rCover!)', 'PYTHON3', '''
def Reclass(rCover):
    if rCover > 40:
        return 4
    elif rCover >=20:
        return 3
    else:
        return 2''')
arcpy.Dissolve_management('SettlementSrf', 'Roof_Concealment', 'rConc')




#******************************VEGETATION CONCEALMENT******************************

#Add fields for vegetation concealment.
arcpy.AddField_management('VegetationSrf', 'vConc', 'LONG')

#Calculate vegetation concealment per FM 5-33.
arcpy.CalculateField_management('VegetationSrf', 'vConc', 'Reclass(!DMT!)', 'PYTHON3', '''
def Reclass(DMT):
    if DMT >= 75:
        return 4
    elif DMT >= 50:
        return 3
    elif DMT >= 25:
        return 2
    elif DMT >= 0:
        return 1
    else:
        return -999''')



#******************************UNION******************************

#Combine features that overlap to do final weighted analysis.
arcpy.Union_analysis(['SettlementSrf', 'VegetationSrf'], 'uConc')

#Add field for final concealment weight.
arcpy.AddField_management('uConc', 'sumConc', 'Long')
arcpy.AddField_management('uConc', 'Concealment', 'Long')

#Calculate sum of concealment weights.
arcpy.CalculateField_management('uConc', 'sumConc', '!rConc! + !vConc!', 'PYTHON3')

#Calculate final concealment weight based off of my own decision.
arcpy.CalculateField_management('uConc', 'Concealment', 'Reclass(!rConc!, !vConc!, !sumConc!)', 'PYTHON3', '''
def Reclass(r,v,sum):
    if sum > 6:
        return sum + 7
    elif max(r,v) == 4:
        while min(r,v) >= 0:
            return min(r,v) + 11
    elif sum > 4:
        return sum + 4
    elif max(r,v) == 3:
        while min(r,v) >= 0:
            return min(r,v) + 7
    elif sum > 2:
        return sum + 2
    elif max(r,v) == 2:
        while min(r,v) >=0:
            return min(r,v) + 2
    elif sum > 0:
        return sum
    else:
        return -999''')




#******************************DISSOLVE******************************

#Dissolve uConc by final concealment.
arcpy.Dissolve_management('uConc', 'Concealment_Analysis', 'Concealment')


                        
                    
