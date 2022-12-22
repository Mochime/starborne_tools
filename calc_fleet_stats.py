import re
import math

# Ship base stats
corvette_fp = 60.
corvette_hp = 150.
patrol_fp = 80.
patrol_hp = 200.
scout_fp = 70.
scout_hp = 160.
destroyer_fp = 300.
destroyer_hp = 750.
frigate_fp = 400.
frigate_hp = 1000.
recon_fp = 350.
recon_hp = 800.
gunship_fp = 400.
gunship_hp = 1100.
gunship_bombing = 80.
carrier_fp = 2000.
carrier_hp = 5000.
dreadnought_fp = 1800.
dreadnought_hp = 4500.
dreadnought_bombing = 100.

#------------------------------------------

def parse_report(report_text):
    # This function extracts building names and levels from a single spy report.
    # Can accept either a direct copy from in-game, or a copy from the Discord
    # channel.
    # The output is the total HP of all the buildings
    
    # First determine where the report is copied from
    if report_text.find('/goto ') > -1:
        discord = True
    else:
        discord = False
    
    # Extract the text pertaining to fleets
    if discord:
        try:
            fleet_text = report_text.split('Fleets\n')[1].split('Hangar\n')[0]
        except:
            fleet_text = report_text.split('Fleets 1\n')[1].split('Hangar\n')[0]
    else:
        fleet_text = report_text.split('Fleets: \n')[1].split('Hangar: \n')[0]
    
    # Eliminate ships in queue from Tianchao reports
    fleet_text = fleet_text.split('Ship Queue')[0]
    
    corvette_search = re.findall('([0-9]+) Corvette',fleet_text)
    patrol_search = re.findall('([0-9]+) Patrol Ship',fleet_text)
    scout_search = re.findall('([0-9]+) Scout',fleet_text)
    destroyer_search = re.findall('([0-9]+) Destroyer',fleet_text)
    frigate_search = re.findall('([0-9]+) Frigate',fleet_text)
    recon_search = re.findall('([0-9]+) Recon',fleet_text)
    gunship_search = re.findall('([0-9]+) Gunship',fleet_text)
    carrier_search = re.findall('([0-9]+) Carrier',fleet_text)
    dreadnought_search = re.findall('([0-9]+) Dreadnought',fleet_text)
    
    FP = 0.0
    HP = 0.0
    scout_FP = 0.0
    scout_HP = 0.0
    bombing = 0.0
    
    # Total corvette stats
    for fleet in corvette_search:
        fleet_fp = float(fleet)*(corvette_fp+\
                   6.*fleet_lvl+\
                   0.8*cadet_school_lvl+\
                   1.0*federal_armory_lvl+\
                   0.8*campaign_directorate_lvl+\
                   light_card_fp[card_quality]+\
                   magna_exercitus_fp['light']+\
                   nakamura_fp['light'])*\
                   (1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_hp = float(fleet)*(corvette_hp+\
                   4.*cadet_school_lvl+\
                   2.5*federal_armory_lvl+\
                   4.*campaign_directorate_lvl+\
                   light_card_hp[card_quality]+\
                   magna_exercitus_hp['light']+\
                   nakamura_hp['light'])*\
                   (1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        FP += fleet_fp
        HP += fleet_hp
    
    # Total patrol stats
    for fleet in patrol_search:
        fleet_fp = float(fleet)*(patrol_fp+\
                   4.*fleet_lvl+\
                   0.8*cadet_school_lvl+\
                   1.0*federal_armory_lvl+\
                   0.8*campaign_directorate_lvl+\
                   light_card_fp[card_quality]+\
                   magna_exercitus_fp['light']+\
                   nakamura_fp['light'])*\
                   (1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_hp = float(fleet)*(patrol_hp+\
                   10.*fleet_lvl+\
                   4.*cadet_school_lvl+\
                   2.5*federal_armory_lvl+\
                   4.*campaign_directorate_lvl+\
                   light_card_hp[card_quality]+\
                   magna_exercitus_hp['light']+\
                   nakamura_hp['light'])*\
                   (1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        FP += fleet_fp
        HP += fleet_hp
    
    # Total scout stats
    for fleet in scout_search:
        fleet_fp = float(fleet)*(scout_fp+\
                   3.5*fleet_lvl+\
                   0.8*scout_command_lvl+\
                   1.0*federal_armory_lvl+\
                   0.8*campaign_directorate_lvl+\
                   light_card_fp[card_quality]+\
                   magna_exercitus_fp['light']+\
                   nakamura_fp['light'])
        
        fleet_hp = float(fleet)*(scout_hp+\
                   8.75*fleet_lvl+\
                   4.*scout_command_lvl+\
                   2.5*federal_armory_lvl+\
                   4.*campaign_directorate_lvl+\
                   light_card_hp[card_quality]+\
                   magna_exercitus_hp['light']+\
                   nakamura_hp['light'])
        
        FP += fleet_fp*(1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        HP += fleet_hp*(1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        scout_FP += (fleet_fp + float(fleet)*(0.8*iot_lvl))*(1.+policy_mod_fp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        scout_HP += (fleet_hp + float(fleet)*(4.*iot_lvl))*(1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
    
    # Total destroyer stats
    for fleet in destroyer_search:
        fleet_fp = float(fleet)*(destroyer_fp+\
                   30.*fleet_lvl+\
                   4.*naval_academy_lvl+\
                   5.*federal_armory_lvl+\
                   4.*campaign_directorate_lvl+\
                   heavy_card_fp[card_quality]+\
                   magna_exercitus_fp['heavy']+\
                   nakamura_fp['heavy'])*\
                   (1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_hp = float(fleet)*(destroyer_hp+\
                   10.*naval_academy_lvl+\
                   12.5*federal_armory_lvl+\
                   20.*campaign_directorate_lvl+\
                   heavy_card_hp[card_quality]+\
                   magna_exercitus_hp['heavy']+\
                   nakamura_hp['heavy'])*\
                   (1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_bombing = float(fleet)*policy_bombing
        
        FP += fleet_fp
        HP += fleet_hp
        bombing += fleet_bombing
    
    # Total frigate stats
    for fleet in frigate_search:
        fleet_fp = float(fleet)*(frigate_fp+\
                   20.*fleet_lvl+\
                   4.*naval_academy_lvl+\
                   5.*federal_armory_lvl+\
                   4.*campaign_directorate_lvl+\
                   heavy_card_fp[card_quality]+\
                   magna_exercitus_fp['heavy']+\
                   nakamura_fp['heavy'])*\
                   (1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_hp = float(fleet)*(frigate_hp+\
                   50.*fleet_lvl+\
                   10.*naval_academy_lvl+\
                   12.5*federal_armory_lvl+\
                   20.*campaign_directorate_lvl+\
                   heavy_card_hp[card_quality]+\
                   magna_exercitus_hp['heavy']+\
                   nakamura_hp['heavy'])*\
                   (1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_bombing = float(fleet)*policy_bombing
        
        FP += fleet_fp
        HP += fleet_hp
        bombing += fleet_bombing
    
    # Total recon stats
    for fleet in recon_search:
        fleet_fp = float(fleet)*(recon_fp+\
                   17.5*fleet_lvl+\
                   4.*strategic_division_lvl+\
                   5.*federal_armory_lvl+\
                   4.*campaign_directorate_lvl+\
                   heavy_card_fp[card_quality]+\
                   magna_exercitus_fp['heavy']+\
                   nakamura_fp['heavy'])
        
        fleet_hp = float(fleet)*(recon_hp+\
                   43.75*fleet_lvl+\
                   10.*strategic_division_lvl+\
                   12.5*federal_armory_lvl+\
                   20.*campaign_directorate_lvl+\
                   heavy_card_hp[card_quality]+\
                   magna_exercitus_hp['heavy']+\
                   nakamura_hp['heavy'])
        
        FP += fleet_fp*(1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        HP += fleet_hp*(1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        scout_FP += (fleet_fp + float(fleet)*(4.*iot_lvl))*(1.+policy_mod_fp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        scout_HP += (fleet_hp + float(fleet)*(10.*iot_lvl))*(1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
    
    # Total gunship stats
    for fleet in gunship_search:
        fleet_fp = float(fleet)*(gunship_fp+\
                   20.*fleet_lvl+\
                   5.*federal_armory_lvl+\
                   4.*campaign_directorate_lvl+\
                   heavy_card_fp[card_quality]+\
                   magna_exercitus_fp['heavy']+\
                   nakamura_fp['heavy'])*\
                   (1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_hp = float(fleet)*(gunship_hp+\
                   50.*fleet_lvl+\
                   10.*war_council_lvl+\
                   12.5*federal_armory_lvl+\
                   20.*campaign_directorate_lvl+\
                   heavy_card_hp[card_quality]+\
                   magna_exercitus_hp['heavy']+\
                   nakamura_hp['heavy'])*\
                   (1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_bombing = float(fleet)*(gunship_bombing+\
                        8.*fleet_lvl+\
                        8.*war_council_lvl+\
                        gunship_card_bombing+\
                        morrell_bombing['heavy']+\
                        policy_bombing)
        
        FP += fleet_fp
        HP += fleet_hp
        bombing += fleet_bombing
    
    # Total carrier stats
    for fleet in carrier_search:
        fleet_fp = float(fleet)*(carrier_fp+\
                   100.*fleet_lvl+\
                   40.*war_council_lvl+\
                   25.*federal_armory_lvl+\
                   20.*campaign_directorate_lvl+\
                   capital_card_fp[card_quality]+\
                   magna_exercitus_fp['capital']+\
                   nakamura_fp['capital'])*\
                   (1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_hp = float(fleet)*(carrier_hp+\
                   250.*fleet_lvl+\
                   100.*war_council_lvl+\
                   62.5*federal_armory_lvl+\
                   100.*campaign_directorate_lvl+\
                   capital_card_hp[card_quality]+\
                   magna_exercitus_hp['capital']+\
                   nakamura_hp['capital'])*\
                   (1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        FP += fleet_fp
        HP += fleet_hp
    
    # Total dreadnought stats
    for fleet in dreadnought_search:
        fleet_fp = float(fleet)*(dreadnought_fp+\
                   180.*fleet_lvl+\
                   36.*war_council_lvl+\
                   25.*federal_armory_lvl+\
                   20.*campaign_directorate_lvl+\
                   capital_card_fp[card_quality]+\
                   magna_exercitus_fp['capital']+\
                   nakamura_fp['capital'])*\
                   (1.+policy_mod_fp+card_percent_mod[card_quality]+doctrine_percent_mod+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_hp = float(fleet)*(dreadnought_hp+\
                   62.5*federal_armory_lvl+\
                   100.*campaign_directorate_lvl+\
                   capital_card_hp[card_quality]+\
                   magna_exercitus_hp['capital']+\
                   nakamura_hp['capital'])*\
                   (1.+policy_mod_hp+card_percent_mod[card_quality]+.02*nanocoater_count+alliance_percent_bonus)
        
        fleet_bombing = float(fleet)*(dreadnought_bombing+\
                        10.*fleet_lvl+\
                        2.*war_council_lvl+\
                        dreadnought_card_bombing+\
                        morrell_bombing['capital'])
        
        FP += fleet_fp
        HP += fleet_hp
        bombing += fleet_bombing
    
    return FP,HP,scout_FP,scout_HP,bombing


#--------------------------------------------
    
# Paste the spy report(s) into this file
report_file_name = './spy_data/reports.txt'

#------------------------------------------------------------------------------
## USER INPUTS - CHANGE BASED ON THE KNOWLEDGE AVAILABLE TO YOU
# Stat buff controls
fleet_lvl = 3 -1 #keep the -1 here because no bonus at lvl 1
federal_armory_lvl = 0
nanocoater_count = 0
alliance_percent_bonus = 0.0
war_council_lvl = 10
naval_academy_lvl = 10
cadet_school_lvl = 10
strategic_division_lvl = 10
scout_command_lvl = 10
iot_lvl = 10
campaign_directorate_lvl = 0
policy_mod_fp = .0
policy_mod_hp = .0
policy_bombing = 10.
doctrine_percent_mod = 0.
magna_exercitus_fp = {'light':5.,'heavy':25.,'capital':125.}
magna_exercitus_hp = {'light':10,'heavy':50,'capital':250}
#magna_exercitus_fp = {'light':0.,'heavy':0.,'capital':0.}
#magna_exercitus_hp = {'light':0.,'heavy':0.,'capital':0.}
#nakamura_fp = {'light':3.,'heavy':15.,'capital':75.}
#nakamura_hp = {'light':7.5,'heavy':37.5,'capital':187.5}
nakamura_fp = {'light':0.,'heavy':0.,'capital':0.}
nakamura_hp = {'light':0.,'heavy':0.,'capital':0.}
morrell_bombing = {'heavy':10.,'capital':50.}
# END USER INPUTS
#------------------------------------------------------------------------------

light_card_fp = {'common':10.+2.,'rare':20.+2.,'epic':30.+2.,'legendary':40.+2.}
heavy_card_fp = {'common':50.+10.,'rare':100.+10.,'epic':150.+10.,'legendary':200.+10.}
capital_card_fp = {'common':250.+50.,'rare':500+50.,'epic':750.+50.,'legendary':1000.+50.}
light_card_hp = {'common':25+5.,'rare':50.+5.,'epic':75.+5.,'legendary':100.+5.}
heavy_card_hp = {'common':125.+25.,'rare':250.+25.,'epic':375.+25.,'legendary':500.+25.}
capital_card_hp = {'common':625.+125.,'rare':1250.+125.,'epic':1875.+125.,'legendary':2500.+125.}
gunship_card_bombing = 120.
dreadnought_card_bombing = 75.
card_percent_mod = {'common':0.04,'rare':0.08,'epic':0.12,'legendary':.16}



with open(report_file_name) as file:
    file_text = file.read()

split_by_report = file_text.split('py Report on hex ')[1:]

for report in split_by_report:
    name = re.search('\(-?[0-9]+,-?[0-9]+\) (?P<station_name>.*) completed ',report).groupdict()['station_name']
    print('Station name: {}'.format(name))
    for card_quality in ['common','rare','epic','legendary']:
        FP,HP,scout_FP,scout_HP,bombing = parse_report(report)
        
        print('With all {} cards:\nTotal FP: {}\nTotal HP: {}\nSab FP: {}\nSab HP: {}\nBombing: {}\n'.format(card_quality,math.ceil(FP),math.ceil(HP),math.ceil(scout_FP),math.ceil(scout_HP),math.ceil(bombing)))