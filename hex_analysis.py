import numpy as np
import pandas as pd
from numba import jit

## hardcoded data
MC_planet_harvest = [6.9,6.9*1.05,6.9*1.1] # 2,3,4 range with apex
MC_field_harvest = 2.5 # prospect inc
MF_harvest = [4.5,4.25,4] # 1,2,3 range
HD_harvest = 6.5

ind_dict = {1:'1 range',
            2:'2 range',
            3:'3 range',
            4:'4 range',
            5:'5 range'}

## Functions
def read_map_data(file):
    '''
    Read map data from file into memory.
    Input: file path (string)
    Output: pandas DataFrame object
    '''
    
    data = pd.read_table(file,sep='\t',header=None,names=['X','Y','Name','Type','Metal','Gas','Crystal','Labor'],index_col=['X','Y'])
    
    return data

def get_distance(point1, point2):
    '''
    Returns the distance between two points on a hex grid
    point1 = (x1, y1)
    point2 = (x2, y2)
    '''
    return ( abs(point1[0]-point2[0]) + abs(point1[0]+point1[1]-point2[0]-point2[1]) + abs(point1[1]-point2[1]) )/2

def get_coords_within_radius(center, radius):
    '''
    Returns a list of coordinates within a given radius of the center point in a hex grid
    '''
    (xc,yc) = center
#    center = (xc,yc)
    
    coords_list = [center]
    r = 1
    while r <= radius:
        xmax = xc + r
        xmin = xc - r
        ymax = yc + r
        ymin = yc - r
        # Vertices at this radius, starting west and going clockwise
        vertices = [(xmax,yc),(xc,ymax),(xmin,ymax),(xmin,yc),(xc,ymin),(xmax,ymin)]
        # For radius 1, the vertices constitute the entire ring, so add them to the list and we're done
        if r == 1:
            coords_list.extend(vertices)
        
        else:
            # Find all the hexes connecting each vertex
            # Loop through each vertex pair
            for i in range(6):
                p1 = np.array(vertices[i-1],dtype=int)
                p2 = np.array(vertices[i],dtype=int)
                p12 = p2-p1 # vector pointing from vertex 1 to 2
                p12sign = np.sign(p12)
                # Step along edge
                for j in range(r):
                    coords_list.append(tuple(p1 + j*p12sign))
                # end edge loop
            # end vertex loop
            
        r += 1
    # end radius loop
    
    return coords_list

def get_features_in_hexes(map_data,coord_list):
    '''
    Returns all the features present in the coordinates provided
    '''
    return map_data[map_data.index.isin(coord_list)]

def total_planets_moons(features):
    '''
    Total resources and labor from planets and moons in feature list
    '''
    f = features[features['Type'] == 'Planet'].merge(features[features['Type'] == 'Moon'],how='outer')
    return f.sum(axis=0,numeric_only=True)
    
def total_fields(features):
    '''
    Total resources and labor from fields in feature list
    '''
    f = features[features['Type'] == 'Field']
    return f.sum(axis=0,numeric_only=True)

def total_all(features):
    '''
    Total resources and labor from planets, moons, and fields in feature list
    '''
    f = features[features['Type'] != 'Special']
    return f.sum(axis=0,numeric_only=True)

def total_special(features):
    '''
    Total resources and labor from special hexes added to station harvest
    '''
    f = features[features['Type'] == 'Special'].merge(features[features['Type'] == 'Other'],how='outer')
    return f

def moon_value(features):
    '''
    Point value of moons toward HSA/CSA
    Note, doesn't perform any distance checks, make sure to only feed features
    extracted from radius 1
    '''
    moons = features[features['Type'] == 'Moon']['Name']
    pts = 0
    for m in moons:
        if 'Small' in m:
            pts += 1
        elif 'Large' in m:
            pts += 3
        else:
            pts += 2
    
    return pts

def analyze_hex_value(map_data,center):
    '''
    Returns the harvest value of: 
        MC (2,3,4,4+prospect)
        MF (1,2,3)
        HD (2,3,4)
        Station base harvest (4,5)
        Special hexes in range (4,5)
        Moon point total for HSA/CSA
    '''
    # Get features at each range
    features = []
    for i in range(5):
        features.append(get_features_in_hexes(map_data,get_coords_within_radius(center,i+1)))
#        features.append(get_features_in_hexes(map_data,get_coords_within_radius(center[0],center[1],i+1)))
    
    # Field values
    fields = [total_fields(f) for f in features]
    planets_moons = [total_planets_moons(f) for f in features]
    harvest = [total_all(f) for f in features]
    special = [total_special(f) for f in features[3:5]]
    
    # Outpost values
    MF_123 = [MF_harvest[i]*fields[i] for i in range(0,3)]
    MC_234p = [MC_planet_harvest[i-1]*planets_moons[i][['Metal','Gas','Crystal']] for i in range(1,4)]
    for i in range(0,3):
        MC_234p.append(MC_234p[i]+MC_field_harvest*fields[i+1][['Metal','Gas','Crystal']])
    HD_234 = [HD_harvest*harvest[i][['Labor']] for i in range(1,4)]
    # Station harvest
    station_harvest_45 = [harvest[i] for i in range(3,5)]
    # Moons
    moon_pts = moon_value(features[0])
    
    print('Hex at [{:d},{:d}] analyzed'.format(int(center[0]),int(center[1])))
    
    return MF_123,MC_234p,HD_234,station_harvest_45,special,moon_pts


## Classes to facilitate storage and analysis of results
class hex_analysis(object):
    
    def __init__(self,center,map_data):
        
        self.xy = center
        
        MF_123,MC_234p,HD_234,station_harvest_45,special,moon_pts = analyze_hex_value(map_data,center)
        
        # Save outpost data
        self.MF = {'1 range':MF_123[0],
                   '2 range':MF_123[1],
                   '3 range':MF_123[2]}
        self.MC = {'2 range':MC_234p[0],
                   '3 range':MC_234p[1],
                   '4 range':MC_234p[2],
                   '2 range+Prospect':MC_234p[3],
                   '3 range+Prospect':MC_234p[4],
                   '4 range+Prospect':MC_234p[5]}
        self.HD = {'2 range':HD_234[0],
                   '3 range':HD_234[1],
                   '4 range':HD_234[2]}
        self.moons = moon_pts
        self.base_harvest = {'4 range':station_harvest_45[0],
                             '5 range':station_harvest_45[1]}
        self.special_hexes = {'4 range':special[0],
                              '5 range':special[1]}
        
        self.contained_hexes = {'4 range':get_coords_within_radius(center,4),
                                '5 range':get_coords_within_radius(center,5)}
#        self.contained_hexes = {'4 range':get_coords_within_radius(center[0],center[1],4),
#                                '5 range':get_coords_within_radius(center[0],center[1],5)}
        self.features = {'4 range':get_features_in_hexes(map_data,self.contained_hexes['4 range']),
                         '5 range':get_features_in_hexes(map_data,self.contained_hexes['5 range'])}
        self.empty_hexes = {'4 range':[h for h in self.contained_hexes['4 range'] if h not in self.features['4 range'].index],
                            '5 range':[h for h in self.contained_hexes['5 range'] if h not in self.features['5 range'].index]}
    
