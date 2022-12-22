import pandas as pd
import time

import hex_analysis as ha

#from joblib import Parallel, delayed


## Main function
if __name__ == '__main__':
    
    t_start = time.time()
    
    # Load map data
    map_file = './map_data/Homefront.dat'
    out_dir = './map_analysis/Homefront/'
    map_data = ha.read_map_data(map_file)
    
    # Generate list of all empty hexes were stations/outposts can be placed
    map_size = 350
    all_hexes = ha.get_coords_within_radius((0,0),map_size)
#    all_hexes = ha.get_coords_within_radius(0,0,map_size)
    empty_hexes = []
    for h in all_hexes:
        if not (h in map_data.index):
            empty_hexes.append(h)
    
    # Analyze the harvest values of each hex
    hex_vals = {}
    for h in empty_hexes:
        hex_vals[h] = ha.hex_analysis(h,map_data)
#        print('Hex at [{:d},{:d}] analyzed'.format(int(h[0]),int(h[1])))
    
    # Get global best spots
    MF_dict = {}
    MC_dict = {}
    MC_dict_noP = {}
    HD_dict = {}
    moon_dict = {}
    for h,an in hex_vals.items():
        MF_dict[h] = an.MF['3 range']
        MC_dict[h] = an.MC['4 range+Prospect']
        MC_dict_noP[h] = an.MC['4 range']
        HD_dict[h] = an.HD['4 range']
        moon_dict[h] = an.moons
    
    MF_df = pd.DataFrame.from_dict(data=MF_dict,orient='index')
    MF_df.insert(loc=4,column='Total RSS',value=MF_df[['Metal','Gas','Crystal']].sum(axis=1))
    MF_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC_df = pd.DataFrame.from_dict(data=MC_dict,orient='index')
    MC_df.insert(loc=3,column='Total RSS',value=MC_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    MC2_df = pd.DataFrame.from_dict(data=MC_dict_noP,orient='index')
    MC2_df.insert(loc=3,column='Total RSS',value=MC2_df[['Metal','Gas','Crystal']].sum(axis=1))
    MC2_df.sort_values(by='Total RSS',axis=0,ascending=False,inplace=True)
    
    HD_df = pd.DataFrame.from_dict(data=HD_dict,orient='index',columns=['Labor'])
    HD_df.sort_values(by='Labor',axis=0,ascending=False,inplace=True)
    
    moon_df = pd.DataFrame.from_dict(data=moon_dict,orient='index',columns=['Moon Points'])
    moon_df.sort_values(by='Moon Points',axis=0,ascending=False,inplace=True)
    
    MF_df.to_csv(out_dir+'MF_3range.csv',index_label=['X','Y'])
    MC_df.to_csv(out_dir+'MC_4range_prospect.csv',index_label=['X','Y'])
    MC2_df.to_csv(out_dir+'MC_4range.csv',index_label=['X','Y'])
    HD_df.to_csv(out_dir+'HD_4range.csv',index_label=['X','Y'])
    moon_df.to_csv(out_dir+'HSA_moons.csv',index_label=['(X,Y)'])
    
    
    print('Runtime: {} minutes'.format((time.time()-t_start)/60))
        