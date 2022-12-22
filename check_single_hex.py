import pandas as pd
import numpy as np
import hex_analysis as ha

## Main function
if __name__ == '__main__':
    
    # Load map data
    map_file = './map_data/Homefront.dat'
    out_dir = './map_analysis/Homefront/'
    map_data = ha.read_map_data(map_file)
    
    ## USER INPUTS
    top_n = 8 # How many locations to list
    loc = (29,-2) # Center of search
    check_radius = 4 # How far from loc to search
    
    
    # Generate list of all empty hexes were stations/outposts can be placed
    all_hexes = ha.get_coords_within_radius(loc,check_radius)
    empty_hexes = []
    for h in all_hexes:
        if not (h in map_data.index):
            empty_hexes.append(h)
    
    # Analyze the harvest values of each hex
    hex_vals = {}
    for h in empty_hexes:
        hex_vals[h] = ha.hex_analysis(h,map_data)
    
    # Analyze all hexes in range
    MF1_dict = {}
    MF2_dict = {}
    MF3_dict = {}
    MC2_dict = {}
    MC3_dict = {}
    MC4_dict = {}
    MC2_dict_noP = {}
    MC3_dict_noP = {}
    MC4_dict_noP = {}
    HD_dict = {}
    moon_dict = {}
    for h,an in hex_vals.items():
        MF1_dict[h] = an.MF['1 range']
        MF2_dict[h] = an.MF['2 range']
        MF3_dict[h] = an.MF['3 range']
        MC2_dict[h] = an.MC['2 range+Prospect']
        MC3_dict[h] = an.MC['3 range+Prospect']
        MC4_dict[h] = an.MC['4 range+Prospect']
        MC2_dict_noP[h] = an.MC['2 range']
        MC3_dict_noP[h] = an.MC['3 range']
        MC4_dict_noP[h] = an.MC['4 range']
        HD_dict[h] = an.HD['4 range']
        moon_dict[h] = an.moons
    
    # Sort best spots
    MF1_df = pd.DataFrame.from_dict(data=MF1_dict,orient='index')
    MF1_df.insert(loc=4,column='Total RSS',value=MF1_df[['Metal','Gas','Crystal']].sum(axis=1))
    MF1_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MF2_df = pd.DataFrame.from_dict(data=MF2_dict,orient='index')
    MF2_df.insert(loc=4,column='Total RSS',value=MF2_df[['Metal','Gas','Crystal']].sum(axis=1))
    MF2_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MF3_df = pd.DataFrame.from_dict(data=MF3_dict,orient='index')
    MF3_df.insert(loc=4,column='Total RSS',value=MF3_df[['Metal','Gas','Crystal']].sum(axis=1))
    MF3_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC2_df = pd.DataFrame.from_dict(data=MC2_dict,orient='index')
    MC2_df.insert(loc=3,column='Total RSS',value=MC2_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC2_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC3_df = pd.DataFrame.from_dict(data=MC3_dict,orient='index')
    MC3_df.insert(loc=3,column='Total RSS',value=MC3_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC3_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC4_df = pd.DataFrame.from_dict(data=MC4_dict,orient='index')
    MC4_df.insert(loc=3,column='Total RSS',value=MC4_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC4_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC2np_df = pd.DataFrame.from_dict(data=MC2_dict_noP,orient='index')
    MC2np_df.insert(loc=3,column='Total RSS',value=MC2np_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC2np_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC3np_df = pd.DataFrame.from_dict(data=MC3_dict_noP,orient='index')
    MC3np_df.insert(loc=3,column='Total RSS',value=MC3np_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC3np_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC4np_df = pd.DataFrame.from_dict(data=MC4_dict_noP,orient='index')
    MC4np_df.insert(loc=3,column='Total RSS',value=MC4np_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC4np_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    HD_df = pd.DataFrame.from_dict(data=HD_dict,orient='index',columns=['Labor'])
    HD_df.sort_values(by='Labor',axis=0,ascending=False,inplace=True)
    
    moon_df = pd.DataFrame.from_dict(data=moon_dict,orient='index',columns=['Moon Points'])
    moon_df.sort_values(by='Moon Points',axis=0,ascending=False,inplace=True)
    
    # Print results
    for i in range(top_n):
        print('MF3 spot #{}: {} RSS at ({}, {})'.format(i+1,MF3_df.iloc[i]['Total RSS'],MF3_df.index[i][0],MF3_df.index[i][1]))
    for i in range(top_n):
        print('MF2 spot #{}: {} RSS at ({}, {})'.format(i+1,MF2_df.iloc[i]['Total RSS'],MF2_df.index[i][0],MF2_df.index[i][1]))
    for i in range(top_n):
        print('MF1 spot #{}: {} RSS at ({}, {})'.format(i+1,MF1_df.iloc[i]['Total RSS'],MF1_df.index[i][0],MF1_df.index[i][1]))
    
    for i in range(top_n):
        print('MC4 spot  #{}: {} RSS at ({}, {})'.format(i+1,MC4np_df.iloc[i]['Total RSS'],MC4np_df.index[i][0],MC4np_df.index[i][1]))
    for i in range(top_n):
        print('MC3 spot #{}: {} RSS at ({}, {})'.format(i+1,MC3np_df.iloc[i]['Total RSS'],MC3np_df.index[i][0],MC3np_df.index[i][1]))
    for i in range(top_n):
        print('MC2 spot #{}: {} RSS at ({}, {})'.format(i+1,MC2np_df.iloc[i]['Total RSS'],MC2np_df.index[i][0],MC2np_df.index[i][1]))
    
    for i in range(top_n):
        print('MC4 spot w/ Prospect #{}: {} RSS at ({}, {})'.format(i+1,MC4_df.iloc[i]['Total RSS'],MC4_df.index[i][0],MC4_df.index[i][1]))
    for i in range(top_n):
        print('MC3 spot w/ Prospect #{}: {} RSS at ({}, {})'.format(i+1,MC3_df.iloc[i]['Total RSS'],MC3_df.index[i][0],MC3_df.index[i][1]))
    for i in range(top_n):
        print('MC2 spot w/ Prospect #{}: {} RSS at ({}, {})'.format(i+1,MC2_df.iloc[i]['Total RSS'],MC2_df.index[i][0],MC2_df.index[i][1]))
    