import pandas as pd
import numpy as np
import re

import hex_analysis as ha

## Main function
if __name__ == '__main__':
    
    # Input controls
    check_radius = 8
    top_n = 7
    
    # Import pre-analyzed data
    data_folder = './map_analysis/Homefront/'
    
    HD_data = pd.read_csv(data_folder+'HD_4range.csv',index_col=['X','Y'])
    MC_data = pd.read_csv(data_folder+'MC_4range_prospect.csv',index_col=['X','Y'])
    MC2_data = pd.read_csv(data_folder+'MC_4range.csv',index_col=['X','Y'])
    MF_data = pd.read_csv(data_folder+'MF_3range.csv',index_col=['X','Y'])
    moon_data = pd.read_csv(data_folder+'HSA_moons.csv',index_col='(X,Y)')
    
    # Load map data
    map_file = './map_data/Homefront.dat'
    out_dir = './map_analysis/Homefront/'
    map_data = ha.read_map_data(map_file)
    
    ## USER INPUT - locations to check. This can be a list of tuples to check multiple spots at once
    locs = [(-172,128)]
#    locs = [(-149,219),
#(-174,69), 
#(-209,199),
#(161,-201),
#(226,-91), 
#(46,169),  
#(-149,-81),
#(-114,-51),
#(1,-81),   
#(-59,-161),
#(-79,199), 
#(-174,129),
#(221,-141),
#(36,-191), 
#(201,-161),
#(-184,-31),
#(-164,149),
#(66,109),  
#(96,49),   
#(161,-61), 
#(141,79),  
#(-179,39), 
#(-4,109),  
#(-64,-91), 
#(141,-141),
#(-89,99),  
#(-14,189), 
#(196,-31)]
    
#    print('Moon loc, MF #1 val, MF #1 loc, MF #2 val, MF #2 loc')
    for loc in locs:
        hexes_in_range = ha.get_coords_within_radius(loc,check_radius)
        MF_vals = {}
        MF_totals = {}
        MC_vals = {}
        MC_totals = {}
        MC2_vals = {}
        MC2_totals = {}
        for spot in hexes_in_range:
            if spot in MF_data.index:
                MF_vals[spot] = MF_data.loc[spot]
                MF_totals[spot] = MF_vals[spot]['Total RSS']
            if spot in MC_data.index:
                MC_vals[spot] = MC_data.loc[spot]
                MC_totals[spot] = MC_vals[spot]['Total RSS']
            if spot in MC_data.index:
                MC2_vals[spot] = MC2_data.loc[spot]
                MC2_totals[spot] = MC2_vals[spot]['Total RSS']
        
        MF_total_values = list(MF_totals.values())
        MF_total_keys = list(MF_totals.keys())
        MF_sorted_inds = np.argsort(MF_total_values)
        MC_total_values = list(MC_totals.values())
        MC_total_keys = list(MC_totals.keys())
        MC_sorted_inds = np.argsort(MC_total_values)
        MC2_total_values = list(MC2_totals.values())
        MC2_total_keys = list(MC2_totals.keys())
        MC2_sorted_inds = np.argsort(MC2_total_values)
        
#        print('({},{}), {}, ({},{}), {}, ({},{})'.format(loc[0],loc[1],
#              MF_total_values[MF_sorted_inds[-1]],MF_total_keys[MF_sorted_inds[-1]][0],MF_total_keys[MF_sorted_inds[-1]][1],
#              MF_total_values[MF_sorted_inds[-2]],MF_total_keys[MF_sorted_inds[-2]][0],MF_total_keys[MF_sorted_inds[-2]][1]))
#        print('({},{}), {:.0f}, ({},{}), {:.0f}, ({},{})'.format(loc[0],loc[1],
#              MC_total_values[MC_sorted_inds[-1]],MC_total_keys[MC_sorted_inds[-1]][0],MC_total_keys[MC_sorted_inds[-1]][1],
#              MC_total_values[MC_sorted_inds[-2]],MC_total_keys[MC_sorted_inds[-2]][0],MC_total_keys[MC_sorted_inds[-2]][1]))
        print('Centered at hex ({},{})'.format(loc[0],loc[1]))
        for i in range(top_n):
            print('MF spot #{}: {} RSS at ({}, {})'.format(i+1,MF_total_values[MF_sorted_inds[-(i+1)]],MF_total_keys[MF_sorted_inds[-(i+1)]][0],MF_total_keys[MF_sorted_inds[-(i+1)]][1]))
        
        for i in range(top_n):
            print('MC spot w/ Prospect #{}: {} RSS at ({}, {})'.format(i+1,MC_total_values[MC_sorted_inds[-(i+1)]],MC_total_keys[MC_sorted_inds[-(i+1)]][0],MC_total_keys[MC_sorted_inds[-(i+1)]][1]))
        
        for i in range(top_n):
            print('MC spot #{}: {} RSS at ({}, {})'.format(i+1,MC2_total_values[MC2_sorted_inds[-(i+1)]],MC2_total_keys[MC2_sorted_inds[-(i+1)]][0],MC2_total_keys[MC2_sorted_inds[-(i+1)]][1]))