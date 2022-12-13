import requests
import pandas as pd
import numpy as np
# import altair as alt

from dataclasses import dataclass
from typing import List, Type

@dataclass
class MatchStatistics:
    """Data container storing statistical information about a summoner, and one or more TFT matches.""" 
    summoner_name: str
    placement: float
    final_level: float
    players_eliminated: float
    total_damage_to_players: float

results: List[Type[MatchStatistics]] = []

data = {
    "Summoner Name": [],
    "Average Damage":[],
    "Average Placement": [],
    "Average Players Eliminated":[],
    "Average Final Level":[]
}

def calculateStats(api_key: str, my_region: str, summoner_names: str, match_count: int):

    for summoner_name in summoner_names:

        # Path used to pull dataset from Riot's API and convert to JSON.
        api_url = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + summoner_name + '?api_key=' + api_key

        full_summoner_info = requests.get(api_url)
        tft_ids = full_summoner_info.json()
        puuid = tft_ids['puuid']
        summoner_id = tft_ids['id']

        # Use Summoner ID to pull general summoner info (e.g. rank, wins/losses) and convert to JSON.
        summoner_info_url = 'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/' + summoner_id + '?api_key=' + api_key
        tft_summoner_info = requests.get(summoner_info_url)
        tft_ids = tft_summoner_info.json()

        # # Use PUUID to pull match IDs and convert to JSON.
        match_id_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?' + 'start=0' + '&count=' + match_count + '&api_key=' + api_key
        match_ids_full = requests.get(match_id_url)
        match_ids = match_ids_full.json()

        number_of_matches = len(match_ids)
        total_damage_all_matches = 0
        total_placement_all_matches = 0
        total_players_eliminated_all_matches = 0
        total_levels_all_matches = 0

        # Now we have latest x match ids for the selected player (default 20) - we can use this to pull match info for those games.
        for match_id in match_ids:

            individual_match_history_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/' + match_id + '?api_key=' + api_key
            individual_match_history = requests.get(individual_match_history_url)
            match_history = individual_match_history.json()
            # Find the placement count of that summoner's PUUID in the match_history, then lookup and return info from that segemnt (to arrive at the specified individual's info).
            basic_match_info = match_history["metadata"]
            all_opponents_ids = basic_match_info["participants"]
            summoner_puuid_index = all_opponents_ids.index(puuid)

            # Now we have the correct index for the individual in question, within the single game in question. We want to look up and store this info now.
            specific_individual_match_info = match_history["info"]["participants"][summoner_puuid_index]

            # For now, we will collect 1) Placement 2) Level 3) Players Eliminated 4) Total Damage To Players, and 5) Augments Used
            placement = specific_individual_match_info["placement"]
            final_level = specific_individual_match_info["level"]
            players_eliminated = specific_individual_match_info["players_eliminated"]
            total_damage_to_players = specific_individual_match_info["total_damage_to_players"]
            # augments_used = specific_individual_match_info["augments"] # This will need to be processed to alter the string for viewing. Not yet included in final output.

            # Add individual match statistics statistics to summary stats to be averaged (by player for all of their matches within range)
            total_damage_all_matches += total_damage_to_players
            total_placement_all_matches += placement
            total_players_eliminated_all_matches += players_eliminated
            total_levels_all_matches += final_level

        # Calculate averages for all relevant statistics for this summoner - within range of x matches.
        average_placement = total_placement_all_matches / number_of_matches
        average_damage = total_damage_all_matches / number_of_matches
        average_players_eliminated = total_players_eliminated_all_matches / number_of_matches
        average_final_level = total_levels_all_matches / number_of_matches

        # Create classes for each summoner's average statistics, for easy retrieval.
        # Need to determine how this class can be used for optimizations.
        curSummoner = MatchStatistics(summoner_name, average_placement, average_final_level, average_players_eliminated, average_damage)
        results.append(curSummoner)

        # Append all summary statistics to dataset - once we complete this process for every summoner, we will return the dataset for final processing.
        for key, val in [("Summoner Name", summoner_name), ("Average Damage", average_damage), ("Average Placement", average_placement), ("Average Players Eliminated", average_players_eliminated), ("Average Final Level", average_final_level)]:
            x = data[key]
            x.append(val)
            data[key] = x

    # print(results)
    # return results
    print(data)
    return data
