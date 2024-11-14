import time
import requests
from datetime import datetime
import players

def fetch_item(patch):
    url = f"https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/item.json"
    response = requests.get(url)
    item_data = response.json()

    # Mapping item_id to a dictionary with 'name', 'status', and 'gold' (total cost)
    item_mapping = {
        int(item_id): {
            'name': item_info['name'],
            'status': 'completed' if 'into' not in item_info else 'component',
            'gold': item_info['gold']['total']  # Get the total gold cost
        } 
        for item_id, item_info in item_data['data'].items()
    }

    # Map 0 to 'None' with a status of 'none' and gold cost of 0
    item_mapping[0] = {'name': 'None', 'status': 'none', 'gold': 0}
    
    return item_mapping

#fetches rune mapping
def fetch_rune(patch):

    url = f"https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/runesReforged.json"
    

    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch runes data. Status code: {response.status_code}")
        return None
    
    
    rune_data = response.json()
    rune_mappings = {}
    

    for tree in rune_data:
        for slot in tree['slots']:
            for rune in slot['runes']:
                rune_mappings[rune['id']] = rune['name']
    rune_mappings[5005] = "Attack Speed"
    rune_mappings[5008] = "Adaptive Force"
    rune_mappings[5001] = "Health Growth"
    rune_mappings[5011] = "Health"
    rune_mappings[5007] = "Ability Haste"
    rune_mappings[5010] = "Movement Speed"
    rune_mappings[5013] = "Tenacity"
    return rune_mappings

def fetch_patch():
    patch_url = f'https://ddragon.leagueoflegends.com/api/versions.json'
    response = requests.get(patch_url)
    data = response.json()
    return data[0]

def get_timeline(region, match_code, api_key, puuid, item_map, item0, item1, item2, item3, item4, item5):
    timeline_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_code}/timeline?api_key={api_key}"
    time.sleep(1)
    response = requests.get(timeline_url)
    print(response.status_code)
    data = response.json()
    item_list = []
    component_list = []
    sup_id = None
    final_items = [item0, item1, item2, item3, item4, item5]
    if 3869 in [item0, item1, item2, item3, item4, item5]:
        sup_id = 3869
    elif 3870 in [item0, item1, item2, item3, item4, item5]:
        sup_id = 3870
    elif 3871 in [item0, item1, item2, item3, item4, item5]:
        sup_id = 3871
    elif 3876 in [item0, item1, item2, item3, item4, item5]:
        sup_id = 3876
    elif 3877 in [item0, item1, item2, item3, item4, item5]:
        sup_id = 3877
    for x, player in enumerate(data['metadata']['participants']):
        if player == puuid:
            participantid = x + 1
            break
    for x in range(len(data['info']['frames'])):
        for item in data['info']['frames'][x]['events']:
            if item['type'] == 'ITEM_PURCHASED':
                if item['participantId'] == participantid:
                    item_id = item['itemId']
                    if item_id in final_items:
                        if item_map[item_id]['status'] == 'completed' and item_map[item_id]['gold'] > 900:
                            item_list.append(item_id)  # Add completed items to item_list
                        else:
                            component_list.append(item_id)  # Add components to component_list
                        final_items = [item for item in final_items if item != item_id]
                    elif item_id == "3865":
                        if sup_id is None:
                            item_list.append(item_id)
                        else:
                            item_list.append(sup_id)
    full_list = item_list + component_list
    final_list = []
    for x in range(6):
        if x < len(full_list):
            final_list.append(full_list[x])
        else:
            final_list.append(0)
    return final_list[0], final_list[1], final_list[2], final_list[3], final_list[4], final_list[5]



#fetches specific match data 
def fetch_match_data(match_id, puuid, region, item_map, rune_map, dict_update, api_key):
    true_region = region
    if region in ['BR1', 'LA1', 'LA2', 'NA1', 'OC1']:
        region = 'americas'
    elif region in ['JP1', 'KR']:
        region = 'asia'
    elif region in ['EUW1', 'EUN1', 'RU', 'TR1', 'ME1']:
        region = 'europe'
    else:
        region = 'sea'
    #api url request link to riot
    specific_match_api_url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}'
    #actual request
    response = requests.get(specific_match_api_url)
    print(f"Fetching Match Specific Data: {match_id}")
    print(response.status_code)
    data = response.json()
    
    timestamp = data['info']['gameEndTimestamp']
    timestamp = timestamp / 1000.0
    timestamp = datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    gameduration = data['info']['gameDuration']
    if gameduration <= 300:
        return None
    if data['info']['participants'][0]['win'] == True:
        result = 'Blue'
    else:
        result = 'Red'
    for player in data['info']['participants']:
        try:
            if player['puuid'] == puuid:
                summoner_champ = player['championName']
                if summoner_champ not in dict_update:
                    dict_update[summoner_champ] = {
                        'items': [],
                        'runes': [],
                        'matchups': []
                    }
                summoner_allin = player['allInPings']
                summoner_assistme = player['assistMePings']
                summoner_pings = player['basicPings']
                summoner_commandping = player['commandPings']
                summoner_dangerping = player['dangerPings']
                summoner_missingping = player['enemyMissingPings']
                summoner_visionping = player['enemyVisionPings']
                summoner_backping = player['getBackPings']
                summoner_holdping = player['holdPings']
                summoner_needvisionping = player['needVisionPings']
                summoner_onmywayping = player['onMyWayPings']
                summoner_pushpings = player['pushPings']
                summoner_supportitem = player['challenges']['completeSupportQuestInTime']
                summoner_controlward = player['challenges']['controlWardsPlaced']
                summoner_damagepermin = round(player['challenges']['damagePerMinute'], 0)
                summoner_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                summoner_dodgeclose = player['challenges']['dodgeSkillShotsSmallWindow']
                summoner_healshield = player['challenges']['effectiveHealAndShielding']
                summoner_cc = player['challenges']['enemyChampionImmobilizations']
                summoner_earlyturrets = player['challenges']['kTurretsDestroyedBeforePlatesFall']
                summoner_kda = round(player['challenges']['kda'], 2)
                summoner_kp = round(player['challenges']['killParticipation'], 2)
                summoner_killsunderturret = player['challenges']['killsNearEnemyTurret']
                summoner_knockintoteamkill = player['challenges']['knockEnemyIntoTeamAndKill']
                summoner_earlyskillshots = player['challenges']['landSkillShotsEarlyGame']
                summoner_minion10 = player['challenges']['laneMinionsFirst10Minutes']
                summoner_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                summoner_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                summoner_rift = player['challenges']['riftHeraldTakedowns']
                summoner_scuttle = player['challenges']['scuttleCrabKills']
                summoner_totaldodge = player['challenges']['skillshotsDodged']
                summoner_totalland = player['challenges']['skillshotsHit']
                summoner_solokill = player['challenges']['soloKills']
                summoner_wards = player['challenges']['stealthWardsPlaced']
                summoner_baron = player['challenges']['teamBaronKills']
                summoner_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                summoner_plates = player['challenges']['turretPlatesTaken']
                summoner_turrets = player['challenges']['turretTakedowns']
                summoner_visionadvantage = round(player['challenges']['visionScoreAdvantageLaneOpponent'], 2)
                summoner_visionscorepermin = round(player['challenges']['visionScorePerMinute'], 2)
                summoner_lvl = player['champLevel']
                summoner_exp = player['champExperience']
                summoner_damagebuilding = player['damageDealtToBuildings']
                summoner_damageobj = player['damageDealtToTurrets']
                summoner_deaths = player['deaths']
                summoner_drag = player['dragonKills']
                summoner_surrender = player['gameEndedInEarlySurrender']
                summoner_lane = player['teamPosition']
                summoner_item0 = player['item0']
                summoner_item1 = player['item1']
                summoner_item2 = player['item2']
                summoner_item3 = player['item3']
                summoner_item4 = player['item4']
                summoner_item5 = player['item5']
                summoner_item6 = player['item6']
                if summoner_item0 not in dict_update[summoner_champ]['items'] and item_map[summoner_item0]['status'] == 'completed' and item_map[summoner_item0]['gold'] > 900:
                    dict_update[summoner_champ]['items'].append(item_map[summoner_item0]['name'])
                if summoner_item1 not in dict_update[summoner_champ]['items'] and item_map[summoner_item1]['status'] == 'completed' and item_map[summoner_item1]['gold'] > 900:
                    dict_update[summoner_champ]['items'].append(item_map[summoner_item1]['name'])
                if summoner_item2 not in dict_update[summoner_champ]['items'] and item_map[summoner_item2]['status'] == 'completed' and item_map[summoner_item2]['gold'] > 900:
                    dict_update[summoner_champ]['items'].append(item_map[summoner_item2]['name'])
                if summoner_item3 not in dict_update[summoner_champ]['items'] and item_map[summoner_item3]['status'] == 'completed' and item_map[summoner_item3]['gold'] > 900:
                    dict_update[summoner_champ]['items'].append(item_map[summoner_item3]['name'])
                if summoner_item4 not in dict_update[summoner_champ]['items'] and item_map[summoner_item4]['status'] == 'completed' and item_map[summoner_item4]['gold'] > 900:
                    dict_update[summoner_champ]['items'].append(item_map[summoner_item4]['name'])
                if summoner_item5 not in dict_update[summoner_champ]['items'] and item_map[summoner_item5]['status'] == 'completed' and item_map[summoner_item5]['gold'] > 900:
                    dict_update[summoner_champ]['items'].append(item_map[summoner_item5]['name'])
                summoner_kills = player['kills']
                summoner_magictaken = player['magicDamageTaken']
                summoner_magicdmg = player['magicDamageDealtToChampions']
                summoner_physicaltaken = player['physicalDamageTaken']
                summoner_physicaldmg = player['physicalDamageDealtToChampions']
                summoner_totaldmg = player['totalDamageDealtToChampions']
                summoner_totaltaken = player['totalDamageTaken']
                summoner_truetaken = player['trueDamageTaken']
                summoner_truedmg = player['trueDamageDealtToChampions']
                summoner_q = player['spell1Casts']
                summoner_w = player['spell2Casts']
                summoner_e = player['spell3Casts']
                summoner_r = player['spell4Casts']
                summoner_spell1casts = player['summoner1Casts']
                summoner_spell1 = player['summoner1Id']
                summoner_spell2casts = player['summoner2Casts']
                summoner_spell2 = player['summoner2Id']
                summoner_team = player['teamId']
                summoner_ccing = player['timeCCingOthers']
                summoner_visionscore = player['visionScore']
                summoner_wardskilled = player['wardsKilled']
                summoner_result = player['win']
                summoner_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                if summoner_rune0 not in dict_update[summoner_champ]['runes']:
                    dict_update[summoner_champ]['runes'].append(rune_map[summoner_rune0])
                summoner_rune01 = player['perks']['styles'][0]['selections'][0]['var1']
                summoner_rune02 = player['perks']['styles'][0]['selections'][0]['var2']
                summoner_rune03 = player['perks']['styles'][0]['selections'][0]['var3']
                summoner_rune1 = player['perks']['styles'][0]['selections'][1]['perk']
                if summoner_rune1 not in dict_update[summoner_champ]['runes']:
                    dict_update[summoner_champ]['runes'].append(rune_map[summoner_rune1])
                summoner_rune11 = player['perks']['styles'][0]['selections'][1]['var1']
                summoner_rune12 = player['perks']['styles'][0]['selections'][1]['var2']
                summoner_rune13 = player['perks']['styles'][0]['selections'][1]['var3']
                summoner_rune2 = player['perks']['styles'][0]['selections'][2]['perk']
                if summoner_rune2 not in dict_update[summoner_champ]['runes']:
                    dict_update[summoner_champ]['runes'].append(rune_map[summoner_rune2])
                summoner_rune21 = player['perks']['styles'][0]['selections'][2]['var1']
                summoner_rune22 = player['perks']['styles'][0]['selections'][2]['var2']
                summoner_rune23 = player['perks']['styles'][0]['selections'][2]['var3']
                summoner_rune3 = player['perks']['styles'][0]['selections'][3]['perk']
                if summoner_rune3 not in dict_update[summoner_champ]['runes']:
                    dict_update[summoner_champ]['runes'].append(rune_map[summoner_rune3])
                summoner_rune31 = player['perks']['styles'][0]['selections'][3]['var1']
                summoner_rune32 = player['perks']['styles'][0]['selections'][3]['var2']
                summoner_rune33 = player['perks']['styles'][0]['selections'][3]['var3']
                summoner_rune4 = player['perks']['styles'][1]['selections'][0]['perk']
                if summoner_rune4 not in dict_update[summoner_champ]['runes']:
                    dict_update[summoner_champ]['runes'].append(rune_map[summoner_rune4])
                summoner_rune41 = player['perks']['styles'][0]['selections'][0]['var1']
                summoner_rune42 = player['perks']['styles'][0]['selections'][0]['var2']
                summoner_rune43 = player['perks']['styles'][0]['selections'][0]['var3']
                summoner_rune5 = player['perks']['styles'][1]['selections'][1]['perk']
                if summoner_rune5 not in dict_update[summoner_champ]['runes']:
                    dict_update[summoner_champ]['runes'].append(rune_map[summoner_rune5])
                summoner_rune51 = player['perks']['styles'][0]['selections'][1]['var1']
                summoner_rune52 = player['perks']['styles'][0]['selections'][1]['var2']
                summoner_rune53 = player['perks']['styles'][0]['selections'][1]['var3']
                summoner_rune8 = player['perks']['statPerks']['defense']
                summoner_rune7 = player['perks']['statPerks']['flex']
                summoner_rune6 = player['perks']['statPerks']['offense']
                summoner_totalhealing = player['totalHeal']
                summoner_healteam = player['totalHealsOnTeammates']
                summoner_shield = player['totalDamageShieldedOnTeammates']
                summoner_minions = player['totalMinionsKilled']
                summoner_champid = player['championId']
                summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5 = get_timeline(region, match_id, api_key, puuid, item_map, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5)
            if player['teamPosition'] == 'TOP' and player['teamId'] == 100:
                bluetop_id = player['summonerId']
                bluetop_ign = player['riotIdGameName']
                bluetop_tag = player['riotIdTagline']
                bluetop_kills = player['kills']
                bluetop_deaths = player['deaths']
                bluetop_assists = player['assists']
                bluetop_kp = round(player['challenges']['killParticipation'], 2)
                bluetop_kda = round(player['challenges']['kda'], 2)
                bluetop_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                bluetop_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                bluetop_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                bluetop_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                bluetop_dmg = player['totalDamageDealtToChampions']
                bluetop_taken = player['totalDamageTaken']
                bluetop_magictaken = player['magicDamageTaken']
                bluetop_magicdmg = player['magicDamageDealtToChampions']
                bluetop_physicaltaken = player['physicalDamageTaken']
                bluetop_physicaldmg = player['physicalDamageDealtToChampions']
                bluetop_truetaken = player['trueDamageTaken']
                bluetop_truedmg = player['trueDamageDealtToChampions']
                bluetop_vision = player['visionScore']
                bluetop_summoner1 = player['summoner1Id']
                bluetop_summoner2 = player['summoner2Id']
                bluetop_minions = player['totalMinionsKilled']
                bluetop_champ = player['championName']
                bluetop_item0 = player['item0']
                bluetop_item1 = player['item1']
                bluetop_item2 = player['item2']
                bluetop_item3 = player['item3']
                bluetop_item4 = player['item4']
                bluetop_item5 = player['item5']
                bluetop_item6 = player['item6']
                bluetop_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                bluetop_puuid = player['puuid']
                bluetop_level = player['champLevel']
                bluetop_champid = player['championId']
                rank_details = players.fetch_rank(true_region, bluetop_id, api_key)
                bluetop_rank = rank_details[0]
                bluetop_tier = rank_details[1]
                bluetop_lp = rank_details[2]
                bluetop_item0, bluetop_item1, bluetop_item2, bluetop_item3, bluetop_item4, bluetop_item5 = get_timeline(region, match_id, api_key, bluetop_puuid, item_map, bluetop_item0, bluetop_item1, bluetop_item2, bluetop_item3, bluetop_item4, bluetop_item5)
            elif player['teamPosition'] == 'TOP' and player['teamId'] == 200:
                redtop_id = player['summonerId']
                redtop_ign = player['riotIdGameName']
                redtop_tag = player['riotIdTagline']
                redtop_kills = player['kills']
                redtop_deaths = player['deaths']
                redtop_assists = player['assists']
                redtop_kp = round(player['challenges']['killParticipation'], 2)
                redtop_kda = round(player['challenges']['kda'], 2)
                redtop_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                redtop_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                redtop_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                redtop_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                redtop_dmg = player['totalDamageDealtToChampions']
                redtop_taken = player['totalDamageTaken']
                redtop_magictaken = player['magicDamageTaken']
                redtop_magicdmg = player['magicDamageDealtToChampions']
                redtop_physicaltaken = player['physicalDamageTaken']
                redtop_physicaldmg = player['physicalDamageDealtToChampions']
                redtop_truetaken = player['trueDamageTaken']
                redtop_truedmg = player['trueDamageDealtToChampions']
                redtop_vision = player['visionScore']
                redtop_summoner1 = player['summoner1Id']
                redtop_summoner2 = player['summoner2Id']
                redtop_minions = player['totalMinionsKilled']
                redtop_champ = player['championName']
                redtop_item0 = player['item0']
                redtop_item1 = player['item1']
                redtop_item2= player['item2']
                redtop_item3 = player['item3']
                redtop_item4 = player['item4']
                redtop_item5 = player['item5']
                redtop_item6 = player['item6']
                redtop_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                redtop_puuid = player['puuid']
                redtop_level = player['champLevel']
                redtop_champid = player['championId']
                rank_details = players.fetch_rank(true_region, redtop_id, api_key)
                redtop_rank = rank_details[0]
                redtop_tier = rank_details[1]
                redtop_lp = rank_details[2]
                redtop_item0, redtop_item1, redtop_item2, redtop_item3, redtop_item4, redtop_item5 = get_timeline(region, match_id, api_key, redtop_puuid, item_map, redtop_item0, redtop_item1, redtop_item2, redtop_item3, redtop_item4, redtop_item5)
            elif player['teamPosition'] == 'JUNGLE' and player['teamId'] == 100:
                bluejg_id = player['summonerId']
                bluejg_ign = player['riotIdGameName']
                bluejg_tag = player['riotIdTagline']
                bluejg_kills = player['kills']
                bluejg_deaths = player['deaths']
                bluejg_assists = player['assists']
                bluejg_kp = round(player['challenges']['killParticipation'], 2)
                bluejg_kda = round(player['challenges']['kda'], 2)
                bluejg_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                bluejg_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                bluejg_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                bluejg_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                bluejg_dmg = player['totalDamageDealtToChampions']
                bluejg_taken = player['totalDamageTaken']
                bluejg_magictaken = player['magicDamageTaken']
                bluejg_magicdmg = player['magicDamageDealtToChampions']
                bluejg_physicaltaken = player['physicalDamageTaken']
                bluejg_physicaldmg = player['physicalDamageDealtToChampions']
                bluejg_truetaken = player['trueDamageTaken']
                bluejg_truedmg = player['trueDamageDealtToChampions']
                bluejg_vision = player['visionScore']
                bluejg_summoner1 = player['summoner1Id']
                bluejg_summoner2 = player['summoner2Id']
                bluejg_minions = player['totalMinionsKilled']
                bluejg_champ = player['championName']
                bluejg_item0 = player['item0']
                bluejg_item1 = player['item1']
                bluejg_item2 = player['item2']
                bluejg_item3 = player['item3']
                bluejg_item4 = player['item4']
                bluejg_item5 = player['item5']
                bluejg_item6 = player['item6']
                bluejg_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                bluejg_puuid = player['puuid']
                bluejg_level = player['champLevel']
                bluejg_champid = player['championId']
                rank_details = players.fetch_rank(true_region, bluejg_id, api_key)
                bluejg_rank = rank_details[0]
                bluejg_tier = rank_details[1]
                bluejg_lp = rank_details[2]
                bluejg_item0, bluejg_item1, bluejg_item2, bluejg_item3, bluejg_item4, bluejg_item5 = get_timeline(region, match_id, api_key, bluejg_puuid, item_map, bluejg_item0, bluejg_item1, bluejg_item2, bluejg_item3, bluejg_item4, bluejg_item5)
            elif player['teamPosition'] == 'JUNGLE' and player['teamId'] == 200:
                redjg_id = player['summonerId']
                redjg_ign = player['riotIdGameName']
                redjg_tag = player['riotIdTagline']
                redjg_kills = player['kills']
                redjg_deaths = player['deaths']
                redjg_assists = player['assists']
                redjg_kp = round(player['challenges']['killParticipation'], 2)
                redjg_kda = round(player['challenges']['kda'], 2)
                redjg_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                redjg_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                redjg_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                redjg_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                redjg_dmg = player['totalDamageDealtToChampions']
                redjg_taken = player['totalDamageTaken']
                redjg_magictaken = player['magicDamageTaken']
                redjg_magicdmg = player['magicDamageDealtToChampions']
                redjg_physicaltaken = player['physicalDamageTaken']
                redjg_physicaldmg = player['physicalDamageDealtToChampions']
                redjg_truetaken = player['trueDamageTaken']
                redjg_truedmg = player['trueDamageDealtToChampions']
                redjg_vision = player['visionScore']
                redjg_summoner1 = player['summoner1Id']
                redjg_summoner2 = player['summoner2Id']
                redjg_minions = player['totalMinionsKilled']
                redjg_champ = player['championName']
                redjg_item0 = player['item0']
                redjg_item1 = player['item1']
                redjg_item2 = player['item2']
                redjg_item3 = player['item3']
                redjg_item4 = player['item4']
                redjg_item5 = player['item5']
                redjg_item6 = player['item6']
                redjg_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                redjg_puuid = player['puuid']
                redjg_level = player['champLevel']
                redjg_champid = player['championId']
                rank_details = players.fetch_rank(true_region, redjg_id, api_key)
                redjg_rank = rank_details[0]
                redjg_tier = rank_details[1]
                redjg_lp = rank_details[2]
                redjg_item0, redjg_item1, redjg_item2, redjg_item3, redjg_item4, redjg_item5 = get_timeline(region, match_id, api_key, redjg_puuid, item_map, redjg_item0, redjg_item1, redjg_item2, redjg_item3, redjg_item4, redjg_item5)
            elif player['teamPosition'] == 'MIDDLE' and player['teamId'] == 100:
                bluemid_id = player['summonerId']
                bluemid_ign = player['riotIdGameName']
                bluemid_tag = player['riotIdTagline']
                bluemid_kills = player['kills']
                bluemid_deaths = player['deaths']
                bluemid_assists = player['assists']
                bluemid_kp = round(player['challenges']['killParticipation'], 2)
                bluemid_kda = round(player['challenges']['kda'], 2)
                bluemid_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                bluemid_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                bluemid_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                bluemid_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                bluemid_dmg = player['totalDamageDealtToChampions']
                bluemid_taken = player['totalDamageTaken']
                bluemid_magictaken = player['magicDamageTaken']
                bluemid_magicdmg = player['magicDamageDealtToChampions']
                bluemid_physicaltaken = player['physicalDamageTaken']
                bluemid_physicaldmg = player['physicalDamageDealtToChampions']
                bluemid_truetaken = player['trueDamageTaken']
                bluemid_truedmg = player['trueDamageDealtToChampions']
                bluemid_vision = player['visionScore']
                bluemid_summoner1 = player['summoner1Id']
                bluemid_summoner2 = player['summoner2Id']
                bluemid_minions = player['totalMinionsKilled']
                bluemid_champ = player['championName']
                bluemid_item0 = player['item0']
                bluemid_item1 = player['item1']
                bluemid_item2 = player['item2']
                bluemid_item3 = player['item3']
                bluemid_item4 = player['item4']
                bluemid_item5 = player['item5']
                bluemid_item6 = player['item6']
                bluemid_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                bluemid_puuid = player['puuid']
                bluemid_level = player['champLevel']
                bluemid_champid = player['championId']
                rank_details = players.fetch_rank(true_region, bluemid_id, api_key)
                bluemid_rank = rank_details[0]
                bluemid_tier = rank_details[1]
                bluemid_lp = rank_details[2]
                bluemid_item0, bluemid_item1, bluemid_item2, bluemid_item3, bluemid_item4, bluemid_item5 = get_timeline(region, match_id, api_key, bluemid_puuid, item_map, bluemid_item0, bluemid_item1, bluemid_item2, bluemid_item3, bluemid_item4, bluemid_item5)
            elif player['teamPosition'] == 'MIDDLE' and player['teamId'] == 200:
                redmid_id = player['summonerId']
                redmid_ign = player['riotIdGameName']
                redmid_tag = player['riotIdTagline']
                redmid_kills = player['kills']
                redmid_deaths = player['deaths']
                redmid_assists = player['assists']
                redmid_kp = round(player['challenges']['killParticipation'], 2)
                redmid_kda = round(player['challenges']['kda'], 2)
                redmid_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                redmid_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                redmid_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                redmid_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                redmid_dmg = player['totalDamageDealtToChampions']
                redmid_taken = player['totalDamageTaken']
                redmid_magictaken = player['magicDamageTaken']
                redmid_magicdmg = player['magicDamageDealtToChampions']
                redmid_physicaltaken = player['physicalDamageTaken']
                redmid_physicaldmg = player['physicalDamageDealtToChampions']
                redmid_truetaken = player['trueDamageTaken']
                redmid_truedmg = player['trueDamageDealtToChampions']
                redmid_vision = player['visionScore']
                redmid_summoner1 = player['summoner1Id']
                redmid_summoner2 = player['summoner2Id']
                redmid_minions = player['totalMinionsKilled']
                redmid_champ = player['championName']
                redmid_item0 = player['item0']
                redmid_item1 = player['item1']
                redmid_item2 = player['item2']
                redmid_item3 = player['item3']
                redmid_item4 = player['item4']
                redmid_item5 = player['item5']
                redmid_item6 = player['item6']
                redmid_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                redmid_puuid = player['puuid']
                redmid_level = player['champLevel']
                redmid_champid = player['championId']
                rank_details = players.fetch_rank(true_region, redmid_id, api_key)
                redmid_rank = rank_details[0]
                redmid_tier = rank_details[1]
                redmid_lp = rank_details[2]
                redmid_item0, redmid_item1, redmid_item2, redmid_item3, redmid_item4, redmid_item5 = get_timeline(region, match_id, api_key, redmid_puuid, item_map, redmid_item0, redmid_item1, redmid_item2, redmid_item3, redmid_item4, redmid_item5)
            elif player['teamPosition'] == 'BOTTOM' and player['teamId'] == 100:
                bluebot_id = player['summonerId']
                bluebot_ign = player['riotIdGameName']
                bluebot_tag = player['riotIdTagline']
                bluebot_kills = player['kills']
                bluebot_deaths = player['deaths']
                bluebot_assists = player['assists']
                bluebot_kp = round(player['challenges']['killParticipation'], 2)
                bluebot_kda = round(player['challenges']['kda'], 2)
                bluebot_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                bluebot_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                bluebot_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                bluebot_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                bluebot_dmg = player['totalDamageDealtToChampions']
                bluebot_taken = player['totalDamageTaken']
                bluebot_magictaken = player['magicDamageTaken']
                bluebot_magicdmg = player['magicDamageDealtToChampions']
                bluebot_physicaltaken = player['physicalDamageTaken']
                bluebot_physicaldmg = player['physicalDamageDealtToChampions']
                bluebot_truetaken = player['trueDamageTaken']
                bluebot_truedmg = player['trueDamageDealtToChampions']
                bluebot_vision = player['visionScore']
                bluebot_summoner1 = player['summoner1Id']
                bluebot_summoner2 = player['summoner2Id']
                bluebot_minions = player['totalMinionsKilled']
                bluebot_champ = player['championName']
                bluebot_item0 = player['item0']
                bluebot_item1 = player['item1']
                bluebot_item2 = player['item2']
                bluebot_item3 = player['item3']
                bluebot_item4 = player['item4']
                bluebot_item5 = player['item5']
                bluebot_item6 = player['item6']
                bluebot_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                bluebot_puuid = player['puuid']
                bluebot_level = player['champLevel']
                bluebot_champid = player['championId']
                rank_details = players.fetch_rank(true_region, bluebot_id, api_key)
                bluebot_rank = rank_details[0]
                bluebot_tier = rank_details[1]
                bluebot_lp = rank_details[2]
                bluebot_item0, bluebot_item1, bluebot_item2, bluebot_item3, bluebot_item4, bluebot_item5 = get_timeline(region, match_id, api_key, bluebot_puuid, item_map, bluebot_item0, bluebot_item1, bluebot_item2, bluebot_item3, bluebot_item4, bluebot_item5)
            elif player['teamPosition'] == 'BOTTOM' and player['teamId'] == 200:
                redbot_id = player['summonerId']
                redbot_ign = player['riotIdGameName']
                redbot_tag = player['riotIdTagline']
                redbot_kills = player['kills']
                redbot_deaths = player['deaths']
                redbot_assists = player['assists']
                redbot_kp = round(player['challenges']['killParticipation'], 2)
                redbot_kda = round(player['challenges']['kda'], 2)
                redbot_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                redbot_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                redbot_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                redbot_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                redbot_dmg = player['totalDamageDealtToChampions']
                redbot_taken = player['totalDamageTaken']
                redbot_magictaken = player['magicDamageTaken']
                redbot_magicdmg = player['magicDamageDealtToChampions']
                redbot_physicaltaken = player['physicalDamageTaken']
                redbot_physicaldmg = player['physicalDamageDealtToChampions']
                redbot_truetaken = player['trueDamageTaken']
                redbot_truedmg = player['trueDamageDealtToChampions']
                redbot_vision = player['visionScore']
                redbot_summoner1 = player['summoner1Id']
                redbot_summoner2 = player['summoner2Id']
                redbot_minions = player['totalMinionsKilled']
                redbot_champ = player['championName']
                redbot_item0 = player['item0']
                redbot_item1 = player['item1']
                redbot_item2 = player['item2']
                redbot_item3 = player['item3']
                redbot_item4 = player['item4']
                redbot_item5 = player['item5']
                redbot_item6 = player['item6']
                redbot_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                redbot_puuid = player['puuid']
                redbot_level = player['champLevel']
                redbot_champid = player['championId']
                rank_details = players.fetch_rank(true_region, redbot_id, api_key)
                redbot_rank = rank_details[0]
                redbot_tier = rank_details[1]
                redbot_lp = rank_details[2]
                redbot_item0, redbot_item1, redbot_item2, redbot_item3, redbot_item4, redbot_item5 = get_timeline(region, match_id, api_key, redbot_puuid, item_map, redbot_item0, redbot_item1, redbot_item2, redbot_item3, redbot_item4, redbot_item5)
            elif player['teamPosition'] == 'UTILITY' and player['teamId'] == 100:
                bluesup_id = player['summonerId']
                bluesup_ign = player['riotIdGameName']
                bluesup_tag = player['riotIdTagline']
                bluesup_kills = player['kills']
                bluesup_deaths = player['deaths']
                bluesup_assists = player['assists']
                bluesup_kp = round(player['challenges']['killParticipation'], 2)
                bluesup_kda = round(player['challenges']['kda'], 2)
                bluesup_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                bluesup_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                bluesup_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                bluesup_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                bluesup_dmg = player['totalDamageDealtToChampions']
                bluesup_taken = player['totalDamageTaken']
                bluesup_magictaken = player['magicDamageTaken']
                bluesup_magicdmg = player['magicDamageDealtToChampions']
                bluesup_physicaltaken = player['physicalDamageTaken']
                bluesup_physicaldmg = player['physicalDamageDealtToChampions']
                bluesup_truetaken = player['trueDamageTaken']
                bluesup_truedmg = player['trueDamageDealtToChampions']
                bluesup_vision = player['visionScore']
                bluesup_summoner1 = player['summoner1Id']
                bluesup_summoner2 = player['summoner2Id']
                bluesup_minions = player['totalMinionsKilled']
                bluesup_champ = player['championName']
                bluesup_item0 = player['item0']
                bluesup_item1 = player['item1']
                bluesup_item2 = player['item2']
                bluesup_item3 = player['item3']
                bluesup_item4 = player['item4']
                bluesup_item5 = player['item5']
                bluesup_item6 = player['item6']
                bluesup_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                bluesup_puuid = player['puuid']
                bluesup_level = player['champLevel']
                bluesup_champid = player['championId']
                rank_details = players.fetch_rank(true_region, bluesup_id, api_key)
                bluesup_rank = rank_details[0]
                bluesup_tier = rank_details[1]
                bluesup_lp = rank_details[2]
                bluesup_item0, bluesup_item1, bluesup_item2, bluesup_item3, bluesup_item4, bluesup_item5 = get_timeline(region, match_id, api_key, bluesup_puuid, item_map, bluesup_item0, bluesup_item1, bluesup_item2, bluesup_item3, bluesup_item4, bluesup_item5)
            elif player['teamPosition'] == 'UTILITY' and player['teamId'] == 200:
                redsup_id = player['summonerId']
                redsup_ign = player['riotIdGameName']
                redsup_tag = player['riotIdTagline']
                redsup_kills = player['kills']
                redsup_deaths = player['deaths']
                redsup_assists = player['assists']
                redsup_kp = round(player['challenges']['killParticipation'], 2)
                redsup_kda = round(player['challenges']['kda'], 2)
                redsup_maxcs = player['challenges']['maxCsAdvantageOnLaneOpponent']
                redsup_maxlvl = player['challenges']['maxLevelLeadLaneOpponent']
                redsup_damagepercent = round(player['challenges']['teamDamagePercentage'], 2)
                redsup_damagetaken = round(player['challenges']['damageTakenOnTeamPercentage'], 2)
                redsup_dmg = player['totalDamageDealtToChampions']
                redsup_taken = player['totalDamageTaken']
                redsup_magictaken = player['magicDamageTaken']
                redsup_magicdmg = player['magicDamageDealtToChampions']
                redsup_physicaltaken = player['physicalDamageTaken']
                redsup_physicaldmg = player['physicalDamageDealtToChampions']
                redsup_truetaken = player['trueDamageTaken']
                redsup_truedmg = player['trueDamageDealtToChampions']
                redsup_vision = player['visionScore']
                redsup_summoner1 = player['summoner1Id']
                redsup_summoner2 = player['summoner2Id']
                redsup_minions = player['totalMinionsKilled']
                redsup_champ = player['championName']
                redsup_item0 = player['item0']
                redsup_item1 = player['item1']
                redsup_item2 = player['item2']
                redsup_item3 = player['item3']
                redsup_item4 = player['item4']
                redsup_item5 = player['item5']
                redsup_item6 = player['item6']
                redsup_rune0 = player['perks']['styles'][0]['selections'][0]['perk']
                redsup_puuid = player['puuid']
                redsup_level = player['champLevel']
                redsup_champid = player['championId']
                rank_details = players.fetch_rank(true_region, redsup_id, api_key)
                redsup_rank = rank_details[0]
                redsup_tier = rank_details[1]
                redsup_lp = rank_details[2]
                redsup_item0, redsup_item1, redsup_item2, redsup_item3, redsup_item4, redsup_item5 = get_timeline(region, match_id, api_key, redsup_puuid, item_map, redsup_item0, redsup_item1, redsup_item2, redsup_item3, redsup_item4, redsup_item5)
            else:
                return None
        except KeyError as e:
            print(f"KeyError encountered: {e}. Skipping match.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}. Skipping match.")
            return None
    if summoner_lane == "TOP" and bluetop_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(bluetop_champ)
    elif summoner_lane == "TOP" and redtop_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(redtop_champ)
    elif summoner_lane == "JUNGLE" and bluejg_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(bluejg_champ)
    elif summoner_lane == "JUNGLE" and redjg_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(redjg_champ)
    elif summoner_lane == "MIDDLE" and bluemid_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(bluemid_champ)
    elif summoner_lane == "MIDDLE" and redmid_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(redmid_champ)
    elif summoner_lane == "BOTTOM" and bluebot_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(bluebot_champ)
    elif summoner_lane == "BOTTOM" and redbot_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(redbot_champ)
    elif summoner_lane == "UTILITY" and bluesup_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(bluesup_champ)
    elif summoner_lane == "UTILITY" and redsup_champ != summoner_champ:
        dict_update[summoner_champ]['matchups'].append(redsup_champ)
    summoner_data = {
        "summoner_AllInPings": summoner_allin,
        "summoner_AssistMePings": summoner_assistme,
        "summoner_Pings": summoner_pings,
        "summoner_CommandPings": summoner_commandping,
        "summoner_DangerPing": summoner_dangerping,
        "summoner_MissingPing": summoner_missingping,
        "summoner_VisionPing": summoner_visionping,
        "summoner_BackPing": summoner_backping,
        "summoner_HoldPing": summoner_holdping,
        "summoner_NeedVisionPing": summoner_needvisionping,
        "summoner_OnMyWayPing": summoner_onmywayping,
        "summoner_PushPings": summoner_pushpings,
        "summoner_SupportItem": summoner_supportitem,
        "summoner_ControlWard": summoner_controlward,
        "summoner_DamagePerMin": summoner_damagepermin,
        "summoner_DamageTaken": summoner_damagetaken,
        "summoner_DodgeClose": summoner_dodgeclose,
        "summoner_HealShield": summoner_healshield,
        "summoner_CC": summoner_cc,
        "summoner_EarlyTurretsBeforePlates": summoner_earlyturrets,
        "summoner_KDA": summoner_kda,
        "summoner_KP": summoner_kp,
        "summoner_KillsUnderTurret": summoner_killsunderturret,
        "summoner_KnockIntoTeamKill": summoner_knockintoteamkill,
        "summoner_EarlySkillShots": summoner_earlyskillshots,
        "summoner_Minions10": summoner_minion10,
        "summoner_MaxCSAdvantage": summoner_maxcs,
        "summoner_MaxLevelLead": summoner_maxlvl,
        "summoner_RiftHeraldTakedown": summoner_rift,
        "summoner_ScuttleCrabs": summoner_scuttle,
        "summoner_TotalDodges": summoner_totaldodge,
        "summoner_TotalLand": summoner_totalland,
        "summoner_SoloKill": summoner_solokill,
        "summoner_Wards": summoner_wards,
        "summoner_Baron": summoner_baron,
        "summoner_DamagePercent": summoner_damagepercent,
        "summoner_Plates": summoner_plates,
        "summoner_Turrets": summoner_turrets,
        "summoner_VisionAdvantange": summoner_visionadvantage,
        "summoner_VisionScorePerMin": summoner_visionscorepermin,
        "summoner_Level": summoner_lvl,
        "summoner_Exp": summoner_exp,
        "summoner_DamageBuilding": summoner_damagebuilding,
        "summoner_DamageObj": summoner_damageobj,
        "summoner_Deaths": summoner_deaths,
        "summoner_Dragon": summoner_drag,
        "summoner_Surrender": summoner_surrender,
        "summoner_Kills": summoner_kills,
        "summoner_MagicTaken": summoner_magictaken,
        "summoner_MagicDmg": summoner_magicdmg,
        "summoner_PhysicalTaken": summoner_physicaltaken,
        "summoner_PhysicalDmg": summoner_physicaldmg,
        "summoner_TotalDmg": summoner_totaldmg,
        "summoner_TotalTaken": summoner_totaltaken,
        "summoner_TrueDmg": summoner_truedmg,
        "summoner_TrueTaken": summoner_truetaken,
        "summoner_Q": summoner_q,
        "summoner_W": summoner_w,
        "summoner_E": summoner_e,
        "summoner_R": summoner_r,
        "summoner_Spell1": summoner_spell1,
        "summoner_Spell1Casts": summoner_spell1casts,
        "summoner_Spell2": summoner_spell2,
        "summoner_Spell2Casts": summoner_spell2casts,
        "summoner_Team": summoner_team,
        "summoner_CCing": summoner_ccing,
        "summoner_VisionScore": summoner_visionscore,
        "summoner_WardsKilled": summoner_wardskilled,
        "summoner_TotalHealing": summoner_totalhealing,
        "summoner_HealTeam": summoner_healteam,
        "summoner_Shield": summoner_shield,
        "summoner_Minions": summoner_minions,
        "summoner_ChampId": summoner_champid,
        "summoner_Rune6": rune_map[summoner_rune6],
        "summoner_Rune7": rune_map[summoner_rune7],
        "summoner_Rune8": rune_map[summoner_rune8],
        "summoner_Rune01": summoner_rune01,
        "summoner_Rune02": summoner_rune02,
        "summoner_Rune03": summoner_rune03,
        "summoner_Rune11": summoner_rune11,
        "summoner_Rune12": summoner_rune12,
        "summoner_Rune13": summoner_rune13,
        "summoner_Rune21": summoner_rune21,
        "summoner_Rune22": summoner_rune22,
        "summoner_Rune23": summoner_rune23,
        "summoner_Rune31": summoner_rune31,
        "summoner_Rune32": summoner_rune32,
        "summoner_Rune33": summoner_rune33,
        "summoner_Rune41": summoner_rune41,
        "summoner_Rune42": summoner_rune42,
        "summoner_Rune43": summoner_rune43,
        "summoner_Rune51": summoner_rune51,
        "summoner_Rune52": summoner_rune52,
        "summoner_Rune53": summoner_rune53,
        "summoner_Item0Id": summoner_item0,
        "summoner_Item1Id": summoner_item1,
        "summoner_Item2Id": summoner_item2,
        "summoner_Item3Id": summoner_item3,
        "summoner_Item4Id": summoner_item4,
        "summoner_Item5Id": summoner_item5,
        "summoner_Item6Id": summoner_item6
    }
    bluetop_data = {
        "bluetop_ID": bluetop_id,
        "bluetop_PUUID": bluetop_puuid,
        "bluetop_IGN": bluetop_ign,
        "bluetop_Tag": bluetop_tag,
        "bluetop_Kills": bluetop_kills,
        "bluetop_deaths": bluetop_deaths,
        "bluetop_assists": bluetop_assists,
        "bluetop_KP": bluetop_kp,
        "bluetop_KDA": bluetop_kda,
        "bluetop_MaxCS": bluetop_maxcs,
        "bluetop_MaxLvl": bluetop_maxlvl,
        "bluetop_DamagePercent": bluetop_damagepercent,
        "bluetop_TakenPercent": bluetop_damagetaken,
        "bluetop_MagicTaken": bluetop_magictaken,
        "bluetop_MagicDMG": bluetop_magicdmg,
        "bluetop_PhysicalTaken": bluetop_physicaltaken,
        "bluetop_PhysicalDMG": bluetop_physicaldmg,
        "bluetop_TrueTaken": bluetop_truetaken,
        "bluetop_TrueDMG": bluetop_truedmg,
        "bluetop_DMG": bluetop_dmg,
        "bluetop_Taken": bluetop_taken,
        "bluetop_VisionScore": bluetop_vision,
        "bluetop_Summoner1": bluetop_summoner1,
        "bluetop_Summoner2": bluetop_summoner2,
        "bluetop_Minions": bluetop_minions,
        "bluetop_Rank": bluetop_rank,
        "bluetop_Tier": bluetop_tier,
        "bluetop_lp": bluetop_lp,
        "bluetop_Item0": item_map[bluetop_item0]['name'],
        "bluetop_Item1": item_map[bluetop_item1]['name'],
        "bluetop_Item2": item_map[bluetop_item2]['name'],
        "bluetop_Item3": item_map[bluetop_item3]['name'],
        "bluetop_Item4": item_map[bluetop_item4]['name'],
        "bluetop_Item5": item_map[bluetop_item5]['name'],
        "bluetop_Item6": item_map[bluetop_item6]['name'],
        "bluetop_Item0Id": bluetop_item0,
        "bluetop_Item1Id": bluetop_item1,
        "bluetop_Item2Id": bluetop_item2,
        "bluetop_Item3Id": bluetop_item3,
        "bluetop_Item4Id": bluetop_item4,
        "bluetop_Item5Id": bluetop_item5,
        "bluetop_Item6Id": bluetop_item6,
        "bluetop_ChampLvl": bluetop_level,
        "bluetop_ChampId": bluetop_champid,
        "bluetop_Rune0": rune_map[bluetop_rune0]
    }
    redtop_data = {
        "redtop_ID": redtop_id,
        "redtop_PUUID": redtop_puuid,
        "redtop_IGN": redtop_ign,
        "redtop_Tag": redtop_tag,
        "redtop_Kills": redtop_kills,
        "redtop_deaths": redtop_deaths,
        "redtop_assists": redtop_assists,
        "redtop_KP": redtop_kp,
        "redtop_KDA": redtop_kda,
        "redtop_MaxCS": redtop_maxcs,
        "redtop_MaxLvl": redtop_maxlvl,
        "redtop_DamagePercent": redtop_damagepercent,
        "redtop_TakenPercent": redtop_damagetaken,
        "redtop_MagicTaken": redtop_magictaken,
        "redtop_MagicDMG": redtop_magicdmg,
        "redtop_PhysicalTaken": redtop_physicaltaken,
        "redtop_PhysicalDMG": redtop_physicaldmg,
        "redtop_TrueTaken": redtop_truetaken,
        "redtop_TrueDMG": redtop_truedmg,
        "redtop_DMG": redtop_dmg,
        "redtop_Taken": redtop_taken,
        "redtop_VisionScore": redtop_vision,
        "redtop_Summoner1": redtop_summoner1,
        "redtop_Summoner2": redtop_summoner2,
        "redtop_Minions": redtop_minions,
        "redtop_Rank": redtop_rank,
        "redtop_Tier": redtop_tier,
        "redtop_lp": redtop_lp,
        "redtop_Item0": item_map[redtop_item0]['name'],
        "redtop_Item1": item_map[redtop_item1]['name'],
        "redtop_Item2": item_map[redtop_item2]['name'],
        "redtop_Item3": item_map[redtop_item3]['name'],
        "redtop_Item4": item_map[redtop_item4]['name'],
        "redtop_Item5": item_map[redtop_item5]['name'],
        "redtop_Item6": item_map[redtop_item6]['name'],
        "redtop_Item0Id": redtop_item0,
        "redtop_Item1Id": redtop_item1,
        "redtop_Item2Id": redtop_item2,
        "redtop_Item3Id": redtop_item3,
        "redtop_Item4Id": redtop_item4,
        "redtop_Item5Id": redtop_item5,
        "redtop_Item6Id": redtop_item6,
        "redtop_ChampLvl": redtop_level,
        "redtop_ChampId": redtop_champid,
        "redtop_Rune0": rune_map[redtop_rune0]
    }
    bluejg_data = {
        "bluejg_ID": bluejg_id,
        "bluejg_PUUID": bluejg_puuid,
        "bluejg_IGN": bluejg_ign,
        "bluejg_Tag": bluejg_tag,
        "bluejg_Kills": bluejg_kills,
        "bluejg_deaths": bluejg_deaths,
        "bluejg_assists": bluejg_assists,
        "bluejg_KP": bluejg_kp,
        "bluejg_KDA": bluejg_kda,
        "bluejg_MaxCS": bluejg_maxcs,
        "bluejg_MaxLvl": bluejg_maxlvl,
        "bluejg_DamagePercent": bluejg_damagepercent,
        "bluejg_TakenPercent": bluejg_damagetaken,
        "bluejg_MagicTaken": bluejg_magictaken,
        "bluejg_MagicDMG": bluejg_magicdmg,
        "bluejg_PhysicalTaken": bluejg_physicaltaken,
        "bluejg_PhysicalDMG": bluejg_physicaldmg,
        "bluejg_TrueTaken": bluejg_truetaken,
        "bluejg_TrueDMG": bluejg_truedmg,
        "bluejg_DMG": bluejg_dmg,
        "bluejg_Taken": bluejg_taken,
        "bluejg_VisionScore": bluejg_vision,
        "bluejg_Summoner1": bluejg_summoner1,
        "bluejg_Summoner2": bluejg_summoner2,
        "bluejg_Minions": bluejg_minions,
        "bluejg_Rank": bluejg_rank,
        "bluejg_Tier": bluejg_tier,
        "bluejg_lp": bluejg_lp,
        "bluejg_Item0": item_map[bluejg_item0]['name'],
        "bluejg_Item1": item_map[bluejg_item1]['name'],
        "bluejg_Item2": item_map[bluejg_item2]['name'],
        "bluejg_Item3": item_map[bluejg_item3]['name'],
        "bluejg_Item4": item_map[bluejg_item4]['name'],
        "bluejg_Item5": item_map[bluejg_item5]['name'],
        "bluejg_Item6": item_map[bluejg_item6]['name'],
        "bluejg_Item0Id": bluejg_item0,
        "bluejg_Item1Id": bluejg_item1,
        "bluejg_Item2Id": bluejg_item2,
        "bluejg_Item3Id": bluejg_item3,
        "bluejg_Item4Id": bluejg_item4,
        "bluejg_Item5Id": bluejg_item5,
        "bluejg_Item6Id": bluejg_item6,
        "bluejg_ChampLvl": bluejg_level,
        "bluejg_ChampId": bluejg_champid,
        "bluejg_Rune0": rune_map[bluejg_rune0]
    }
    redjg_data = {
        "redjg_ID": redjg_id,
        "redjg_PUUID": redjg_puuid,
        "redjg_IGN": redjg_ign,
        "redjg_Tag": redjg_tag,
        "redjg_Kills": redjg_kills,
        "redjg_deaths": redjg_deaths,
        "redjg_assists": redjg_assists,
        "redjg_KP": redjg_kp,
        "redjg_KDA": redjg_kda,
        "redjg_MaxCS": redjg_maxcs,
        "redjg_MaxLvl": redjg_maxlvl,
        "redjg_DamagePercent": redjg_damagepercent,
        "redjg_TakenPercent": redjg_damagetaken,
        "redjg_MagicTaken": redjg_magictaken,
        "redjg_MagicDMG": redjg_magicdmg,
        "redjg_PhysicalTaken": redjg_physicaltaken,
        "redjg_PhysicalDMG": redjg_physicaldmg,
        "redjg_TrueTaken": redjg_truetaken,
        "redjg_TrueDMG": redjg_truedmg,
        "redjg_DMG": redjg_dmg,
        "redjg_Taken": redjg_taken,
        "redjg_VisionScore": redjg_vision,
        "redjg_Summoner1": redjg_summoner1,
        "redjg_Summoner2": redjg_summoner2,
        "redjg_Minions": redjg_minions,
        "redjg_Rank": redjg_rank,
        "redjg_Tier": redjg_tier,
        "redjg_lp": redjg_lp,
        "redjg_Item0": item_map[redjg_item0]['name'],
        "redjg_Item1": item_map[redjg_item1]['name'],
        "redjg_Item2": item_map[redjg_item2]['name'],
        "redjg_Item3": item_map[redjg_item3]['name'],
        "redjg_Item4": item_map[redjg_item4]['name'],
        "redjg_Item5": item_map[redjg_item5]['name'],
        "redjg_Item6": item_map[redjg_item6]['name'],
        "redjg_Item0Id": redjg_item0,
        "redjg_Item1Id": redjg_item1,
        "redjg_Item2Id": redjg_item2,
        "redjg_Item3Id": redjg_item3,
        "redjg_Item4Id": redjg_item4,
        "redjg_Item5Id": redjg_item5,
        "redjg_Item6Id": redjg_item6,
        "redjg_ChampLvl": redjg_level,
        "redjg_ChampId": redjg_champid,
        "redjg_Rune0": rune_map[redjg_rune0]
    }
    bluemid_data = {
        "bluemid_ID": bluemid_id,
        "bluemid_PUUID": bluemid_puuid,
        "bluemid_IGN": bluemid_ign,
        "bluemid_Tag": bluemid_tag,
        "bluemid_Kills": bluemid_kills,
        "bluemid_deaths": bluemid_deaths,
        "bluemid_assists": bluemid_assists,
        "bluemid_KP": bluemid_kp,
        "bluemid_KDA": bluemid_kda,
        "bluemid_MaxCS": bluemid_maxcs,
        "bluemid_MaxLvl": bluemid_maxlvl,
        "bluemid_DamagePercent": bluemid_damagepercent,
        "bluemid_TakenPercent": bluemid_damagetaken,
        "bluemid_MagicTaken": bluemid_magictaken,
        "bluemid_MagicDMG": bluemid_magicdmg,
        "bluemid_PhysicalTaken": bluemid_physicaltaken,
        "bluemid_PhysicalDMG": bluemid_physicaldmg,
        "bluemid_TrueTaken": bluemid_truetaken,
        "bluemid_TrueDMG": bluemid_truedmg,
        "bluemid_DMG": bluemid_dmg,
        "bluemid_Taken": bluemid_taken,
        "bluemid_VisionScore": bluemid_vision,
        "bluemid_Summoner1": bluemid_summoner1,
        "bluemid_Summoner2": bluemid_summoner2,
        "bluemid_Minions": bluemid_minions,
        "bluemid_Rank": bluemid_rank,
        "bluemid_Tier": bluemid_tier,
        "bluemid_lp": bluemid_lp,
        "bluemid_Item0": item_map[bluemid_item0]['name'],
        "bluemid_Item1": item_map[bluemid_item1]['name'],
        "bluemid_Item2": item_map[bluemid_item2]['name'],
        "bluemid_Item3": item_map[bluemid_item3]['name'],
        "bluemid_Item4": item_map[bluemid_item4]['name'],
        "bluemid_Item5": item_map[bluemid_item5]['name'],
        "bluemid_Item6": item_map[bluemid_item6]['name'],
        "bluemid_Item0Id": bluemid_item0,
        "bluemid_Item1Id": bluemid_item1,
        "bluemid_Item2Id": bluemid_item2,
        "bluemid_Item3Id": bluemid_item3,
        "bluemid_Item4Id": bluemid_item4,
        "bluemid_Item5Id": bluemid_item5,
        "bluemid_Item6Id": bluemid_item6,
        "bluemid_ChampLvl": bluemid_level,
        "bluemid_ChampId": bluemid_champid,
        "bluemid_Rune0": rune_map[bluemid_rune0]
    }
    redmid_data = {
        "redmid_ID": redmid_id,
        "redmid_PUUID": redmid_puuid,
        "redmid_IGN": redmid_ign,
        "redmid_Tag": redmid_tag,
        "redmid_Kills": redmid_kills,
        "redmid_deaths": redmid_deaths,
        "redmid_assists": redmid_assists,
        "redmid_KP": redmid_kp,
        "redmid_KDA": redmid_kda,
        "redmid_MaxCS": redmid_maxcs,
        "redmid_MaxLvl": redmid_maxlvl,
        "redmid_DamagePercent": redmid_damagepercent,
        "redmid_TakenPercent": redmid_damagetaken,
        "redmid_MagicTaken": redmid_magictaken,
        "redmid_MagicDMG": redmid_magicdmg,
        "redmid_PhysicalTaken": redmid_physicaltaken,
        "redmid_PhysicalDMG": redmid_physicaldmg,
        "redmid_TrueTaken": redmid_truetaken,
        "redmid_TrueDMG": redmid_truedmg,
        "redmid_DMG": redmid_dmg,
        "redmid_Taken": redmid_taken,
        "redmid_VisionScore": redmid_vision,
        "redmid_Summoner1": redmid_summoner1,
        "redmid_Summoner2": redmid_summoner2,
        "redmid_Minions": redmid_minions,
        "redmid_Rank": redmid_rank,
        "redmid_Tier": redmid_tier,
        "redmid_lp": redmid_lp,
        "redmid_Item0": item_map[redmid_item0]['name'],
        "redmid_Item1": item_map[redmid_item1]['name'],
        "redmid_Item2": item_map[redmid_item2]['name'],
        "redmid_Item3": item_map[redmid_item3]['name'],
        "redmid_Item4": item_map[redmid_item4]['name'],
        "redmid_Item5": item_map[redmid_item5]['name'],
        "redmid_Item6": item_map[redmid_item6]['name'],
        "redmid_Item0Id": redmid_item0,
        "redmid_Item1Id": redmid_item1,
        "redmid_Item2Id": redmid_item2,
        "redmid_Item3Id": redmid_item3,
        "redmid_Item4Id": redmid_item4,
        "redmid_Item5Id": redmid_item5,
        "redmid_Item6Id": redmid_item6,
        "redmid_ChampLvl": redmid_level,
        "redmid_ChampId": redmid_champid,
        "redmid_Rune0": rune_map[redmid_rune0]
    }
    bluebot_data = {
        "bluebot_ID": bluebot_id,
        "bluebot_PUUID": bluebot_puuid,
        "bluebot_IGN": bluebot_ign,
        "bluebot_Tag": bluebot_tag,
        "bluebot_Kills": bluebot_kills,
        "bluebot_deaths": bluebot_deaths,
        "bluebot_assists": bluebot_assists,
        "bluebot_KP": bluebot_kp,
        "bluebot_KDA": bluebot_kda,
        "bluebot_MaxCS": bluebot_maxcs,
        "bluebot_MaxLvl": bluebot_maxlvl,
        "bluebot_DamagePercent": bluebot_damagepercent,
        "bluebot_TakenPercent": bluebot_damagetaken,
        "bluebot_MagicTaken": bluebot_magictaken,
        "bluebot_MagicDMG": bluebot_magicdmg,
        "bluebot_PhysicalTaken": bluebot_physicaltaken,
        "bluebot_PhysicalDMG": bluebot_physicaldmg,
        "bluebot_TrueTaken": bluebot_truetaken,
        "bluebot_TrueDMG": bluebot_truedmg,
        "bluebot_DMG": bluebot_dmg,
        "bluebot_Taken": bluebot_taken,
        "bluebot_VisionScore": bluebot_vision,
        "bluebot_Summoner1": bluebot_summoner1,
        "bluebot_Summoner2": bluebot_summoner2,
        "bluebot_Minions": bluebot_minions,
        "bluebot_Rank": bluebot_rank,
        "bluebot_Tier": bluebot_tier,
        "bluebot_lp": bluebot_lp,
        "bluebot_Item0": item_map[bluebot_item0]['name'],
        "bluebot_Item1": item_map[bluebot_item1]['name'],
        "bluebot_Item2": item_map[bluebot_item2]['name'],
        "bluebot_Item3": item_map[bluebot_item3]['name'],
        "bluebot_Item4": item_map[bluebot_item4]['name'],
        "bluebot_Item5": item_map[bluebot_item5]['name'],
        "bluebot_Item6": item_map[bluebot_item6]['name'],
        "bluebot_Item0Id": bluebot_item0,
        "bluebot_Item1Id": bluebot_item1,
        "bluebot_Item2Id": bluebot_item2,
        "bluebot_Item3Id": bluebot_item3,
        "bluebot_Item4Id": bluebot_item4,
        "bluebot_Item5Id": bluebot_item5,
        "bluebot_Item6Id": bluebot_item6,
        "bluebot_ChampLvl": bluebot_level,
        "bluebot_ChampId": bluebot_champid,
        "bluebot_Rune0": rune_map[bluebot_rune0]
    }
    redbot_data = {
        "redbot_ID": redbot_id,
        "redbot_PUUID": redbot_puuid,
        "redbot_IGN": redbot_ign,
        "redbot_Tag": redbot_tag,
        "redbot_Kills": redbot_kills,
        "redbot_deaths": redbot_deaths,
        "redbot_assists": redbot_assists,
        "redbot_KP": redbot_kp,
        "redbot_KDA": redbot_kda,
        "redbot_MaxCS": redbot_maxcs,
        "redbot_MaxLvl": redbot_maxlvl,
        "redbot_DamagePercent": redbot_damagepercent,
        "redbot_TakenPercent": redbot_damagetaken,
        "redbot_MagicTaken": redbot_magictaken,
        "redbot_MagicDMG": redbot_magicdmg,
        "redbot_PhysicalTaken": redbot_physicaltaken,
        "redbot_PhysicalDMG": redbot_physicaldmg,
        "redbot_TrueTaken": redbot_truetaken,
        "redbot_TrueDMG": redbot_truedmg,
        "redbot_DMG": redbot_dmg,
        "redbot_Taken": redbot_taken,
        "redbot_VisionScore": redbot_vision,
        "redbot_Summoner1": redbot_summoner1,
        "redbot_Summoner2": redbot_summoner2,
        "redbot_Minions": redbot_minions,
        "redbot_Rank": redbot_rank,
        "redbot_Tier": redbot_tier,
        "redbot_lp": redbot_lp,
        "redbot_Item0": item_map[redbot_item0]['name'],
        "redbot_Item1": item_map[redbot_item1]['name'],
        "redbot_Item2": item_map[redbot_item2]['name'],
        "redbot_Item3": item_map[redbot_item3]['name'],
        "redbot_Item4": item_map[redbot_item4]['name'],
        "redbot_Item5": item_map[redbot_item5]['name'],
        "redbot_Item6": item_map[redbot_item6]['name'],
        "redbot_Item0Id": redbot_item0,
        "redbot_Item1Id": redbot_item1,
        "redbot_Item2Id": redbot_item2,
        "redbot_Item3Id": redbot_item3,
        "redbot_Item4Id": redbot_item4,
        "redbot_Item5Id": redbot_item5,
        "redbot_Item6Id": redbot_item6,
        "redbot_ChampLvl": redbot_level,
        "redbot_ChampId": redbot_champid,
        "redbot_Rune0": rune_map[redbot_rune0]
    }
    bluesup_data = {
        "bluesup_ID": bluesup_id,
        "bluesup_PUUID": bluesup_puuid,
        "bluesup_IGN": bluesup_ign,
        "bluesup_Tag": bluesup_tag,
        "bluesup_Kills": bluesup_kills,
        "bluesup_deaths": bluesup_deaths,
        "bluesup_assists": bluesup_assists,
        "bluesup_KP": bluesup_kp,
        "bluesup_KDA": bluesup_kda,
        "bluesup_MaxCS": bluesup_maxcs,
        "bluesup_MaxLvl": bluesup_maxlvl,
        "bluesup_DamagePercent": bluesup_damagepercent,
        "bluesup_TakenPercent": bluesup_damagetaken,
        "bluesup_MagicTaken": bluesup_magictaken,
        "bluesup_MagicDMG": bluesup_magicdmg,
        "bluesup_PhysicalTaken": bluesup_physicaltaken,
        "bluesup_PhysicalDMG": bluesup_physicaldmg,
        "bluesup_TrueTaken": bluesup_truetaken,
        "bluesup_TrueDMG": bluesup_truedmg,
        "bluesup_DMG": bluesup_dmg,
        "bluesup_Taken": bluesup_taken,
        "bluesup_VisionScore": bluesup_vision,
        "bluesup_Summoner1": bluesup_summoner1,
        "bluesup_Summoner2": bluesup_summoner2,
        "bluesup_Minions": bluesup_minions,
        "bluesup_Rank": bluesup_rank,
        "bluesup_Tier": bluesup_tier,
        "bluesup_lp": bluesup_lp,
        "bluesup_Item0": item_map[bluesup_item0]['name'],
        "bluesup_Item1": item_map[bluesup_item1]['name'],
        "bluesup_Item2": item_map[bluesup_item2]['name'],
        "bluesup_Item3": item_map[bluesup_item3]['name'],
        "bluesup_Item4": item_map[bluesup_item4]['name'],
        "bluesup_Item5": item_map[bluesup_item5]['name'],
        "bluesup_Item6": item_map[bluesup_item6]['name'],
        "bluesup_Item0Id": bluesup_item0,
        "bluesup_Item1Id": bluesup_item1,
        "bluesup_Item2Id": bluesup_item2,
        "bluesup_Item3Id": bluesup_item3,
        "bluesup_Item4Id": bluesup_item4,
        "bluesup_Item5Id": bluesup_item5,
        "bluesup_Item6Id": bluesup_item6,
        "bluesup_ChampLvl": bluesup_level,
        "bluesup_ChampId": bluesup_champid,
        "bluesup_Rune0": rune_map[bluesup_rune0]
    }
    redsup_data = {
        "redsup_ID": redsup_id,
        "redsup_PUUID": redsup_puuid,
        "redsup_IGN": redsup_ign,
        "redsup_Tag": redsup_tag,
        "redsup_Kills": redsup_kills,
        "redsup_deaths": redsup_deaths,
        "redsup_assists": redsup_assists,
        "redsup_KP": redsup_kp,
        "redsup_KDA": redsup_kda,
        "redsup_MaxCS": redsup_maxcs,
        "redsup_MaxLvl": redsup_maxlvl,
        "redsup_DamagePercent": redsup_damagepercent,
        "redsup_TakenPercent": redsup_damagetaken,
        "redsup_MagicTaken": redsup_magictaken,
        "redsup_MagicDMG": redsup_magicdmg,
        "redsup_PhysicalTaken": redsup_physicaltaken,
        "redsup_PhysicalDMG": redsup_physicaldmg,
        "redsup_TrueTaken": redsup_truetaken,
        "redsup_TrueDMG": redsup_truedmg,
        "redsup_DMG": redsup_dmg,
        "redsup_Taken": redsup_taken,
        "redsup_VisionScore": redsup_vision,
        "redsup_Summoner1": redsup_summoner1,
        "redsup_Summoner2": redsup_summoner2,
        "redsup_Minions": redsup_minions,
        "redsup_Rank": redsup_rank,
        "redsup_Tier": redsup_tier,
        "redsup_lp": redsup_lp,
        "redsup_Item0": item_map[redsup_item0]['name'],
        "redsup_Item1": item_map[redsup_item1]['name'],
        "redsup_Item2": item_map[redsup_item2]['name'],
        "redsup_Item3": item_map[redsup_item3]['name'],
        "redsup_Item4": item_map[redsup_item4]['name'],
        "redsup_Item5": item_map[redsup_item5]['name'],
        "redsup_Item6": item_map[redsup_item6]['name'],
        "redsup_Item0Id": redsup_item0,
        "redsup_Item1Id": redsup_item1,
        "redsup_Item2Id": redsup_item2,
        "redsup_Item3Id": redsup_item3,
        "redsup_Item4Id": redsup_item4,
        "redsup_Item5Id": redsup_item5,
        "redsup_Item6Id": redsup_item6,
        "redsup_ChampLvl": redsup_level,
        "redsup_ChampId": redsup_champid,
        "redsup_Rune0": rune_map[redsup_rune0]
    }
    return (match_id, summoner_champ, summoner_lane, puuid, gameduration, item_map[summoner_item0]['name'], item_map[summoner_item1]['name'], item_map[summoner_item2]['name'], item_map[summoner_item3]['name'], item_map[summoner_item4]['name'], item_map[summoner_item5]['name'], item_map[summoner_item6]['name'], rune_map[summoner_rune0], rune_map[summoner_rune1], rune_map[summoner_rune2], rune_map[summoner_rune3], rune_map[summoner_rune4], rune_map[summoner_rune5], summoner_data, summoner_result,
            bluetop_champ, bluetop_data,
            redtop_champ, redtop_data,
            bluejg_champ, bluejg_data,
            redjg_champ, redjg_data,
            bluemid_champ, bluemid_data,
            redmid_champ, redmid_data,
            bluebot_champ, bluebot_data,
            redbot_champ, redbot_data,
            bluesup_champ, bluesup_data,
            redsup_champ, redsup_data)


#fetches matches of user
def fetch_matches(region, puuid, season_start, api_key):
    if region in ['BR1', 'LA1', 'LA2', 'NA1', 'OC1']:
        region = 'americas'
    elif region in ['JP1', 'KR']:
        region = 'asia'
    elif region in ['EUW1', 'EUN1', 'RU', 'TR1', 'ME1']:
        region = 'europe'
    else:
        region = 'sea'

    type_match = 'ranked'
    starting_index = 0
    matches_requested = 100
    all_matches = []
    while True:
        matches_api_url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={season_start}&type={type_match}&start={starting_index}&count={matches_requested}&api_key={api_key}'
        response = requests.get(matches_api_url)
        print("Fetching Matches")
        print(response.status_code)
        if response.status_code != 200:
            print(f"Error fetching matches: {response.status_code}")
            break
        bundled_matches = response.json()
        if not bundled_matches:
            break
            
        all_matches.extend(bundled_matches)
        

        starting_index += matches_requested

    return all_matches
