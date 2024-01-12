import requests


class SummonerOverviewStatistics:
    def __init__(self, summoner_name, number_of_matches, total_damage_all_matches, total_placement_all_matches, total_players_eliminated_all_matches, total_levels_all_matches):
        self.summoner_name: str = summoner_name
        self.number_of_matches: int = number_of_matches
        # Accumulated statistics -> looped over and added to when going through each match retrieved.
        self.total_damage_all_matches: float = total_levels_all_matches
        self.total_placement_all_matches: float = total_placement_all_matches
        self.total_players_eliminated_all_matches: float = total_players_eliminated_all_matches
        self.total_levels_all_matches: float = total_levels_all_matches

    def get_tuple(self):
        return iter((self.summoner_name, self.total_damage_all_matches / self.number_of_matches, self.total_placement_all_matches / self.number_of_matches, self.total_players_eliminated_all_matches / self.number_of_matches, self.total_levels_all_matches / self.number_of_matches))



def calculateStats(api_key: str, my_region: str, summoner_names: str, match_count: int):
    results = [] # Will store average statistics for each summoner -> will be returned (and charted) after calculations are complete.
    for summoner_name in summoner_names:
        # Path used to pull dataset from Riot's API and convert to JSON.
        api_url = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + summoner_name + '?api_key=' + api_key
        full_summoner_info = requests.get(api_url)

        # print("full_summoner_info", full_summoner_info)
        # for num in full_summoner_info:
        #     print(num)

        tft_ids = full_summoner_info.json()
        if "puuid" and "id" in tft_ids:
            puuid = tft_ids['puuid']
            summoner_id = tft_ids['id']

        print("puuid", puuid, "summoner_id", summoner_id)


        # Use Summoner ID to pull general summoner info (e.g. rank, wins/losses) and convert to JSON.
        summoner_info_url = 'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/' + summoner_id + '?api_key=' + api_key
        tft_summoner_info = requests.get(summoner_info_url)
        tft_summoner_info_json = tft_summoner_info.json()

        print("tft_summoner_info_json", tft_summoner_info_json)

        # # Use PUUID to pull match IDs and convert to JSON.
        match_id_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?' + 'start=0' + '&count=' + match_count + '&api_key=' + api_key
        match_ids_full = requests.get(match_id_url)
        match_ids = match_ids_full.json()
        print("match_ids", match_ids)

        # Create an object for cur_summoner to store accumulated statistics.
        cur_summoner = SummonerOverviewStatistics(summoner_name, len(match_ids), 0, 0, 0, 0)

        # Using the latest x match ids for the selected player - pull statistics for those matches and accumulate for this summoner.
        for match_id in match_ids:
            individual_match_history_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/' + match_id + '?api_key=' + api_key
            individual_match_history = requests.get(individual_match_history_url)
            match_history = individual_match_history.json()
        #     Find the placement count of that summoner's PUUID in the match_history, then lookup and return info from that segment (to arrive at the specified individual's info).
            if "metadata" in match_history.keys():
                basic_match_info = match_history["metadata"]
                if "participants" in basic_match_info.keys():
                    all_opponents_ids = basic_match_info["participants"]
                    summoner_puuid_index = all_opponents_ids.index(puuid)

        #     Now we have the index for the individual in question, within the match in question. Look up and store this info now.
            if "info" in match_history.keys() and "participants" in match_history["info"].keys():
                specific_individual_match_info = match_history["info"]["participants"][summoner_puuid_index]

        #     For now, we will collect 1) Placement 2) Level 3) Players Eliminated 4) Total Damage To Players
            if "placement" in specific_individual_match_info.keys() and "level" in specific_individual_match_info.keys() and "players_eliminated" in specific_individual_match_info.keys() and "total_damage_to_players" in specific_individual_match_info.keys():
                placement = specific_individual_match_info["placement"]
                final_level = specific_individual_match_info["level"]
                players_eliminated = specific_individual_match_info["players_eliminated"]
                total_damage_to_players = specific_individual_match_info["total_damage_to_players"]

        #     Add the statistics from this match to the accumulated statistics for this summoner.
            cur_summoner.total_damage_all_matches += total_damage_to_players
            cur_summoner.total_placement_all_matches += placement
            cur_summoner.total_players_eliminated_all_matches += players_eliminated
            cur_summoner.total_levels_all_matches += final_level

        # Retrieving summary statistics (for one summoner) and storing in sqlite3. Per match averages are appened to results.
        results.append(cur_summoner.get_tuple())

    print("results", results)
    return results