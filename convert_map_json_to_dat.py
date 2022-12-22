import json

# Load map json file
map_json_file = './map_data/Crossfire #9.json'
with open(map_json_file,'r') as file:
    map_dict = json.load(file)

# Load conversion from ContentID to hex type
with open('./map_data/CELL_DEFINITIONS.json','r') as file:
    raw_types = json.load(file)
# Convert to be more easily indexable
type_dict = {}
for ii in raw_types:
    if 'HarvestValue' in ii.keys():
        type_dict[ii['Id']] = {'Name':ii['Name'],'Type':ii['Type'],'HarvestValue':ii['HarvestValue']}
    else:
        type_dict[ii['Id']] = {'Name':ii['Name'],'Type':ii['Type']}

types = {1:'Planet', 2:'Field', 3:'Moon', 4:'Star', 5:'Special'}

def indDict(d,key):
    if key in d.keys():
        return d[key]
    else:
        return 0

# Blocks of the map are stored in 'Templates'
output_file = './map_data/Crossfire #9.dat'
with open(output_file,'w') as file:
    for tt in map_dict['Templates']:
        for hh in tt['Hexes']:
            if 'HarvestValue' in type_dict[hh['ContentID']].keys():
                file.write('{x:d}\t{y:d}\t{name:s}\t{typ:s}\t{m:d}\t{g:d}\t{c:d}\t{L:d}\n'.format(
                        x=hh['Position']['Q'],
                        y=hh['Position']['R'],
                        name=type_dict[hh['ContentID']]['Name'],
                        typ=types[type_dict[hh['ContentID']]['Type']],
                        m=indDict(type_dict[hh['ContentID']]['HarvestValue'],'MR'),
                        g=indDict(type_dict[hh['ContentID']]['HarvestValue'],'GR'),
                        c=indDict(type_dict[hh['ContentID']]['HarvestValue'],'CR'),
                        L=indDict(type_dict[hh['ContentID']]['HarvestValue'],'LQ')))
