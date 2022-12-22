# starborne_tools

This is a collection of assorted analysis and calculation tools for the online game Starborne. Most are simple Python scripts intended for a user with at least basic Python knowledge. Inputs are mostly accomplished by simply editing the code directly. Outputs are printed to the console.

List of tools:
- calc_fleet_stats.py: Calculates approximate total fleet stats from spy reports pasted into 'spy_data/reports.txt'. Controls for stat buffs should be modified by the user using their best knowledge of what the enemy has (e.g. Campaign Directorate level, Nanocoater count, policy buffs, supply building levels, other alliance percentage buffs, etc.).

- find_best_spots.py: Compiles and ranks the total outpost values of every open hex on a map. Requires an associated .dat file for the map (I usually copy from Lotpe's spreadsheet and save as as an ASCII file). This script can take 6+ hours to run, but only needs to be done once per map. Outputs a .csv file listing 3-range MF, 4-range MC (with and without Prospect Inc), 4-range HD, and HSA/CSA moon values for every hex.

- find_best_in_range.py: Requires find_best_spots.py to have been run first. Finds the top outpost spots within range of a specified hex. Mainly useful for finding the best MF/MC spots for a given moon or station spot.

- check_single_hex.py: Checks all outpost values (not just max range-carded) within range of a specified hex. This does NOT require find_best_spots.py to have been run. The user may wish to alter the print statements to extract different information.

- travel_time.py: Calculates travel times and arrival times for a given speed and distance.
