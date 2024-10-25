import time
import requests
from datetime import datetime
import players
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
def fetch_match_data(match_id, puuid, region, api_key):
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
    for count, player in enumerate(data['info']['participants']):
        try:
            if player['puuid'] == puuid:
                summoner_champ = player[count]['championName']
                summoner_allin = player[count]['allInPings']
                summoner_assistme = player[count]['assistmePings']
                summoner_pings = player[count]['basicPings']
                summoner_commandping = player[count]['commandPings']
                summoner_dangerping = player[count]['dangerPings']
                summoner_missingping = player[count]['missingPings']
                summoner_visionping = player[count]['enemyVisionPings']
                summoner_backping = player[count]['getBackPings']
                summoner_holdping = player[count]['holdPings']
                summoner_needvisionping = player[count]['needVisionPings']
                summoner_onmywayping = player[count]['onMyWayPings']
                summoner_pushpings = player[count]['pushPings']
                summoner_supportitem = player[count]['challenges']['completeSupportQuestInTime']
                summoner_controlward = player[count]['challenges']['controlWardsPlaced']
                summoner_damagepermin = round(player[count]['challenges']['damagePerMinute'], 0)
                summoner_damagetaken = round(player[count]['challenges']['damageTakenOnTeamPercentage'], 2)
                summoner_dodgeclose = player[count]['challenges']['dodgeSkillShotsSmallWindow']
                summoner_healshield = player[count]['challenges']['effectiveHealAndShielding']
                summoner_cc = player[count]['challenges']['enemyChampionImmobilizations']
                summoner_earlyturrets = player[count]['challenges']['kTurretsDestroyedBeforePlatesFall']
                summoner_kda = round(player[count]['challenges']['kda'], 2)
                summoner_kp = round(player[count]['challenges']['killParticipation'], 2)
                summoner_killsunderturret = player[count]['challenges']['killsNearEnemyTurret']
                summoner_knockintoteamkill = player[count]['challenges']['knockEnemyIntoTeamAndKill']
                summoner_earlyskillshots = player[count]['challenges']['landSkillShotsEarlyGame']
                summoner_minion10 = player[count]['challenges']['laneMinionsFirst10Minutes']
                summoner_maxcs = player[count]['challenges']['maxCsAdvantageOnLaneOpponent']
                summoner_maxlvl = player[count]['challenges']['maxLevelLeadLaneOpponent']
                summoner_rift = player[count]['challenges']['riftHeraldTakedowns']
                summoner_scuttle = player[count]['scuttleCrabKills']
                summoner_totaldodge = player[count]['challenges']['skillshotsDodged']
                summoner_totalland = player[count]['challenges']['skillshotsHit']
                summoner_solokill = player[count]['challenges']['soloKills']
                summoner_wards = player[count]['challenges']['stealthWardsPlaced']
                summoner_baron = player[count]['challenges']['teamBaronKills']
                summoner_damagepercent = round(player[count]['challenges']['teamDamagePercentage'], 2)
                summoner_plates = player[count]['challenges']['turretPlatesTaken']
                summoner_turrets = player[count]['challenges']['turretTakedowns']
                summoner_visionadvantage = round(player[count]['challenges']['visionScoreAdvantageLaneOpponent'], 2)
                summoner_visionscorepermin = round(player[count]['challenges']['visionScorePerMinute'], 2)
                summoner_lvl = player[count]['champLevel']
                summoner_exp = player[count]['champExperience']
                summoner_damagebuilding = player[count]['damageDealtToBuildings']
                summoner_damageobj = player[count]['damageDealtToTurrets']
                summoner_deaths = player[count]['deaths']
                summoner_drag = player[count]['dragonKills']
                summoner_surrender = player[count]['gameEndedInEarlySurrender']
                summoner_lane = player['teamPosition']
                summoner_item0 = player[count]['item0']
                summoner_item1 = player[count]['item1']
                summoner_item2 = player[count]['item2']
                summoner_item3 = player[count]['item3']
                summoner_item4 = player[count]['item4']
                summoner_item5 = player[count]['item5']
                summoner_item6 = player[count]['item6']
                summoner_kills = player[count]['kills']
                summoner_magictaken = player[count]['magicDamageTaken']
                summoner_magicdmg = player[count]['magicDamageDealtToChampions']
                summoner_physicaltaken = player[count]['physicalDamageTaken']
                summoner_physicaldmg = player[count]['physicalDamageDealtToChampions']
                summoner_totaldmg = player[count]['totalDamageDealtToChampions']
                summoner_totaltaken = player[count]['totalDamageTaken']
                summoner_truetaken = player[count]['trueDamageTaken']
                summoner_truedmg = player[count]['trueDamageDealtToChampions']
                summoner_q = player[count]['spell1Casts']
                summoner_w = player[count]['spell2Casts']
                summoner_e = player[count]['spell3Casts']
                summoner_r = player[count]['spell4Casts']
                summoner_spell1casts = player[count]['summoner1Casts']
                summoner_spell1 = player[count]['summoner1Id']
                summoner_spell2casts = player[count]['summoner2Casts']
                summoner_spell2 = player[count]['summoner2Id']
                summoner_team = player[count]['teamId']
                summoner_ccing = player[count]['timeCCingOtheres']
                summoner_visionscore = player[count]['visionScore']
                summoner_wardskilled = player[count]['wardsKilled']
                summoner_result = player['win']
                summoner_rune0 = player[count]['perks']['styles'][0]['selections'][0]['perk']
                summoner_rune1 = player[count]['perks']['styles'][0]['selections'][1]['perk']
                summoner_rune2 = player[count]['perks']['styles'][0]['selections'][2]['perk']
                summoner_rune3 = player[count]['perks']['styles'][0]['selections'][3]['perk']
                summoner_rune4 = player[count]['perks']['styles'][1]['selections'][0]['perk']
                summoner_rune5 = player[count]['perks']['styles'][1]['selections'][1]['perk']
                summoner_rune8 = player[count]['perks']['statPerks']['defense']
                summoner_rune7 = player[count]['perks']['statPerks']['flex']
                summoner_rune6 = player[count]['perks']['statPerks']['offense']
                summoner_totalhealing = player[count]['totalHeal']
                summoner_healteam = player[count]['totalHealsOnTeammates']
                summoner_shield = player[count]['totalDamageShieldedOnTeammates']
                summoner_minions = player[count]['totalMinionsKilled']
                bluetop_item0, bluetop_item1, bluetop_item2, bluetop_item3, bluetop_item4, bluetop_item5 = get_timeline(region, match_id, api_key, puuid, item_map, bluetop_item0, bluetop_item1, bluetop_item2, bluetop_item3, bluetop_item4, bluetop_item5)
            if player['teamPosition'] == 'TOP' and player['teamId'] == 100:
                bluetop_id = data['info']['participants'][count]['summonerId']
                bluetop_ign = player[count]['riotIdGameName']
                bluetop_tag = player[count]['riotIdTagline']
                bluetop_kills = player[count]['kills']
                bluetop_deaths = player[count]['deaths']
                bluetop_assists = player[count]['assists']
                bluetop_kp = round(player[count]['killParticipation'], 2)
                bluetop_kda = round(player[count]['kda'], 2)
                bluetop_dmg = player[count]['totalDamageDealtToChampions']
                bluetop_taken = player[count]['totalDamageTaken']
                bluetop_vision = player[count]['visionScore']
                bluetop_summoner1 = player[count]['summoner1Id']
                bluetop_summoner2 = player[count]['summoner2Id']
                bluetop_minions = player[count]['totalMinionsKilled']
                bluetop_champ = data['info']['participants'][count]['championName']
                bluetop_item0 = data['info']['participants'][count]['item0']
                bluetop_item1 = data['info']['participants'][count]['item1']
                bluetop_item2 = data['info']['participants'][count]['item2']
                bluetop_item3 = data['info']['participants'][count]['item3']
                bluetop_item4 = data['info']['participants'][count]['item4']
                bluetop_item5 = data['info']['participants'][count]['item5']
                bluetop_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, bluetop_id, api_key)
                bluetop_rank = rank_details[0]
                bluetop_tier = rank_details[1]
                bluetop_lp = rank_details[2]
                bluetop_item0, bluetop_item1, bluetop_item2, bluetop_item3, bluetop_item4, bluetop_item5 = get_timeline(region, match_id, api_key, puuid, item_map, bluetop_item0, bluetop_item1, bluetop_item2, bluetop_item3, bluetop_item4, bluetop_item5)
            elif player['teamPosition'] == 'TOP' and player['teamId'] == 200:
                redtop_id = data['info']['participants'][count]['summonerId']
                redtop_ign = player[count]['riotIdGameName']
                redtop_tag = player[count]['riotIdTagline']
                redtop_kills = player[count]['kills']
                redtop_deaths = player[count]['deaths']
                redtop_assists = player[count]['assists']
                redtop_kp = round(player[count]['killParticipation'], 2)
                redtop_kda = round(player[count]['kda'], 2)
                redtop_dmg = player[count]['totalDamageDealtToChampions']
                redtop_taken = player[count]['totalDamageTaken']
                redtop_vision = player[count]['visionScore']
                redtop_summoner1 = player[count]['summoner1Id']
                redtop_summoner2 = player[count]['summoner2Id']
                redtop_minions = player[count]['totalMinionsKilled']
                redtop_champ = data['info']['participants'][count]['championName']
                redtop_item0 = data['info']['participants'][count]['item0']
                redtop_item1 = data['info']['participants'][count]['item1']
                redtop_item2= data['info']['participants'][count]['item2']
                redtop_item3 = data['info']['participants'][count]['item3']
                redtop_item4 = data['info']['participants'][count]['item4']
                redtop_item5 = data['info']['participants'][count]['item5']
                redtop_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, redtop_id, api_key)
                redtop_rank = rank_details[0]
                redtop_tier = rank_details[1]
                redtop_lp = rank_details[2]
                redtop_item0, redtop_item1, redtop_item2, redtop_item3, redtop_item4, redtop_item5 = get_timeline(region, match_id, api_key, puuid, item_map, redtop_item0, redtop_item1, redtop_item2, redtop_item3, redtop_item4, redtop_item5)
            elif player['teamPosition'] == 'JUNGLE' and player['teamId'] == 100:
                bluejg_id = data['info']['participants'][count]['summonerId']
                bluejg_ign = player[count]['riotIdGameName']
                bluejg_tag = player[count]['riotIdTagline']
                bluejg_kills = player[count]['kills']
                bluejg_deaths = player[count]['deaths']
                bluejg_assists = player[count]['assists']
                bluejg_kp = round(player[count]['killParticipation'], 2)
                bluejg_kda = round(player[count]['kda'], 2)
                bluejg_dmg = player[count]['totalDamageDealtToChampions']
                bluejg_taken = player[count]['totalDamageTaken']
                bluejg_vision = player[count]['visionScore']
                bluejg_summoner1 = player[count]['summoner1Id']
                bluejg_summoner2 = player[count]['summoner2Id']
                bluejg_minions = player[count]['totalMinionsKilled']
                bluejg_champ = data['info']['participants'][count]['championName']
                bluejg_item0 = data['info']['participants'][count]['item0']
                bluejg_item1 = data['info']['participants'][count]['item1']
                bluejg_item2 = data['info']['participants'][count]['item2']
                bluejg_item3 = data['info']['participants'][count]['item3']
                bluejg_item4 = data['info']['participants'][count]['item4']
                bluejg_item5 = data['info']['participants'][count]['item5']
                bluejg_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, bluejg_id, api_key)
                bluejg_rank = rank_details[0]
                bluejg_tier = rank_details[1]
                bluejg_lp = rank_details[2]
                bluejg_item0, bluejg_item1, bluejg_item2, bluejg_item3, bluejg_item4, bluejg_item5 = get_timeline(region, match_id, api_key, puuid, item_map, bluejg_item0, bluejg_item1, bluejg_item2, bluejg_item3, bluejg_item4, bluejg_item5)
            elif player['teamPosition'] == 'JUNGLE' and player['teamId'] == 200:
                redjg_id = data['info']['participants'][count]['summonerId']
                redjg_ign = player[count]['riotIdGameName']
                redjg_tag = player[count]['riotIdTagline']
                redjg_kills = player[count]['kills']
                redjg_deaths = player[count]['deaths']
                redjg_assists = player[count]['assists']
                redjg_kp = round(player[count]['killParticipation'], 2)
                redjg_kda = round(player[count]['kda'], 2)
                redjg_dmg = player[count]['totalDamageDealtToChampions']
                redjg_taken = player[count]['totalDamageTaken']
                redjg_vision = player[count]['visionScore']
                redjg_summoner1 = player[count]['summoner1Id']
                redjg_summoner2 = player[count]['summoner2Id']
                redjg_minions = player[count]['totalMinionsKilled']
                redjg_champ = data['info']['participants'][count]['championName']
                redjg_item0 = data['info']['participants'][count]['item0']
                redjg_item1 = data['info']['participants'][count]['item1']
                redjg_item2 = data['info']['participants'][count]['item2']
                redjg_item3 = data['info']['participants'][count]['item3']
                redjg_item4 = data['info']['participants'][count]['item4']
                redjg_item5 = data['info']['participants'][count]['item5']
                redjg_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, redjg_id, api_key)
                redjg_rank = rank_details[0]
                redjg_tier = rank_details[1]
                redjg_lp = rank_details[2]
                redjg_item0, redjg_item1, redjg_item2, redjg_item3, redjg_item4, redjg_item5 = get_timeline(region, match_id, api_key, puuid, item_map, redjg_item0, redjg_item1, redjg_item2, redjg_item3, redjg_item4, redjg_item5)
            elif player['teamPosition'] == 'MIDDLE' and player['teamId'] == 100:
                bluemid_id = data['info']['participants'][count]['summonerId']
                bluemid_ign = player[count]['riotIdGameName']
                bluemid_tag = player[count]['riotIdTagline']
                bluemid_kills = player[count]['kills']
                bluemid_deaths = player[count]['deaths']
                bluemid_assists = player[count]['assists']
                bluemid_kp = round(player[count]['killParticipation'], 2)
                bluemid_kda = round(player[count]['kda'], 2)
                bluemid_dmg = player[count]['totalDamageDealtToChampions']
                bluemid_taken = player[count]['totalDamageTaken']
                bluemid_vision = player[count]['visionScore']
                bluemid_summoner1 = player[count]['summoner1Id']
                bluemid_summoner2 = player[count]['summoner2Id']
                bluemid_minions = player[count]['totalMinionsKilled']
                bluemid_champ = data['info']['participants'][count]['championName']
                bluemid_item0 = data['info']['participants'][count]['item0']
                bluemid_item1 = data['info']['participants'][count]['item1']
                bluemid_item2 = data['info']['participants'][count]['item2']
                bluemid_item3 = data['info']['participants'][count]['item3']
                bluemid_item4 = data['info']['participants'][count]['item4']
                bluemid_item5 = data['info']['participants'][count]['item5']
                bluemid_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, bluemid_id, api_key)
                bluemid_rank = rank_details[0]
                bluemid_tier = rank_details[1]
                bluemid_lp = rank_details[2]
                bluemid_item0, bluemid_item1, bluemid_item2, bluemid_item3, bluemid_item4, bluemid_item5 = get_timeline(region, match_id, api_key, puuid, item_map, bluemid_item0, bluemid_item1, bluemid_item2, bluemid_item3, bluemid_item4, bluemid_item5)
            elif player['teamPosition'] == 'MIDDLE' and player['teamId'] == 200:
                redmid_id = data['info']['participants'][count]['summonerId']
                redmid_ign = player[count]['riotIdGameName']
                redmid_tag = player[count]['riotIdTagline']
                redmid_kills = player[count]['kills']
                redmid_deaths = player[count]['deaths']
                redmid_assists = player[count]['assists']
                redmid_kp = round(player[count]['killParticipation'], 2)
                redmid_kda = round(player[count]['kda'], 2)
                redmid_dmg = player[count]['totalDamageDealtToChampions']
                redmid_taken = player[count]['totalDamageTaken']
                redmid_vision = player[count]['visionScore']
                redmid_summoner1 = player[count]['summoner1Id']
                redmid_summoner2 = player[count]['summoner2Id']
                redmid_minions = player[count]['totalMinionsKilled']
                redmid_champ = data['info']['participants'][count]['championName']
                redmid_item0 = data['info']['participants'][count]['item0']
                redmid_item1 = data['info']['participants'][count]['item1']
                redmid_item2 = data['info']['participants'][count]['item2']
                redmid_item3 = data['info']['participants'][count]['item3']
                redmid_item4 = data['info']['participants'][count]['item4']
                redmid_item5 = data['info']['participants'][count]['item5']
                redmid_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, redmid_id, api_key)
                redmid_rank = rank_details[0]
                redmid_tier = rank_details[1]
                redmid_lp = rank_details[2]
                redmid_item0, redmid_item1, redmid_item2, redmid_item3, redmid_item4, redmid_item5 = get_timeline(region, match_id, api_key, puuid, item_map, redmid_item0, redmid_item1, redmid_item2, redmid_item3, redmid_item4, redmid_item5)
            elif player['teamPosition'] == 'BOTTOM' and player['teamId'] == 100:
                bluebot_id = data['info']['participants'][count]['summonerId']
                bluebot_ign = player[count]['riotIdGameName']
                bluebot_tag = player[count]['riotIdTagline']
                bluebot_kills = player[count]['kills']
                bluebot_deaths = player[count]['deaths']
                bluebot_assists = player[count]['assists']
                bluebot_kp = round(player[count]['killParticipation'], 2)
                bluebot_kda = round(player[count]['kda'], 2)
                bluebot_dmg = player[count]['totalDamageDealtToChampions']
                bluebot_taken = player[count]['totalDamageTaken']
                bluebot_vision = player[count]['visionScore']
                bluebot_summoner1 = player[count]['summoner1Id']
                bluebot_summoner2 = player[count]['summoner2Id']
                bluebot_minions = player[count]['totalMinionsKilled']
                bluebot_champ = data['info']['participants'][count]['championName']
                bluebot_item0 = data['info']['participants'][count]['item0']
                bluebot_item1 = data['info']['participants'][count]['item1']
                bluebot_item2 = data['info']['participants'][count]['item2']
                bluebot_item3 = data['info']['participants'][count]['item3']
                bluebot_item4 = data['info']['participants'][count]['item4']
                bluebot_item5 = data['info']['participants'][count]['item5']
                bluebot_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, bluebot_id, api_key)
                bluebot_rank = rank_details[0]
                bluebot_tier = rank_details[1]
                bluebot_lp = rank_details[2]
                bluebot_item0, bluebot_item1, bluebot_item2, bluebot_item3, bluebot_item4, bluebot_item5 = get_timeline(region, match_id, api_key, puuid, item_map, bluebot_item0, bluebot_item1, bluebot_item2, bluebot_item3, bluebot_item4, bluebot_item5)
            elif player['teamPosition'] == 'BOTTOM' and player['teamId'] == 200:
                redbot_id = data['info']['participants'][count]['summonerId']
                redbot_ign = player[count]['riotIdGameName']
                redbot_tag = player[count]['riotIdTagline']
                redbot_kills = player[count]['kills']
                redbot_deaths = player[count]['deaths']
                redbot_assists = player[count]['assists']
                redbot_kp = round(player[count]['killParticipation'], 2)
                redbot_kda = round(player[count]['kda'], 2)
                redbot_dmg = player[count]['totalDamageDealtToChampions']
                redbot_taken = player[count]['totalDamageTaken']
                redbot_vision = player[count]['visionScore']
                redbot_summoner1 = player[count]['summoner1Id']
                redbot_summoner2 = player[count]['summoner2Id']
                redbot_minions = player[count]['totalMinionsKilled']
                redbot_champ = data['info']['participants'][count]['championName']
                redbot_item0 = data['info']['participants'][count]['item0']
                redbot_item1 = data['info']['participants'][count]['item1']
                redbot_item2 = data['info']['participants'][count]['item2']
                redbot_item3 = data['info']['participants'][count]['item3']
                redbot_item4 = data['info']['participants'][count]['item4']
                redbot_item5 = data['info']['participants'][count]['item5']
                redbot_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, redbot_id, api_key)
                redbot_rank = rank_details[0]
                redbot_tier = rank_details[1]
                redbot_lp = rank_details[2]
                redbot_item0, redbot_item1, redbot_item2, redbot_item3, redbot_item4, redbot_item5 = get_timeline(region, match_id, api_key, puuid, item_map, redbot_item0, redbot_item1, redbot_item2, redbot_item3, redbot_item4, redbot_item5)
            elif player['teamPosition'] == 'UTILITY' and player['teamId'] == 100:
                bluesup_id = data['info']['participants'][count]['summonerId']
                bluesup_ign = player[count]['riotIdGameName']
                bluesup_tag = player[count]['riotIdTagline']
                bluesup_kills = player[count]['kills']
                bluesup_deaths = player[count]['deaths']
                bluesup_assists = player[count]['assists']
                bluesup_kp = round(player[count]['killParticipation'], 2)
                bluesup_kda = round(player[count]['kda'], 2)
                bluesup_dmg = player[count]['totalDamageDealtToChampions']
                bluesup_taken = player[count]['totalDamageTaken']
                bluesup_vision = player[count]['visionScore']
                bluesup_summoner1 = player[count]['summoner1Id']
                bluesup_summoner2 = player[count]['summoner2Id']
                bluesup_minions = player[count]['totalMinionsKilled']
                bluesup_champ = data['info']['participants'][count]['championName']
                bluesup_item0 = data['info']['participants'][count]['item0']
                bluesup_item1 = data['info']['participants'][count]['item1']
                bluesup_item2 = data['info']['participants'][count]['item2']
                bluesup_item3 = data['info']['participants'][count]['item3']
                bluesup_item4 = data['info']['participants'][count]['item4']
                bluesup_item5 = data['info']['participants'][count]['item5']
                bluesup_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, bluesup_id, api_key)
                bluesup_rank = rank_details[0]
                bluesup_tier = rank_details[1]
                bluesup_lp = rank_details[2]
                bluesup_item0, bluesup_item1, bluesup_item2, bluesup_item3, bluesup_item4, bluesup_item5 = get_timeline(region, match_id, api_key, puuid, item_map, bluesup_item0, bluesup_item1, bluesup_item2, bluesup_item3, bluesup_item4, bluesup_item5)
            elif player['teamPosition'] == 'UTILITY' and player['teamId'] == 200:
                redsup_id = data['info']['participants'][count]['summonerId']
                redsup_ign = player[count]['riotIdGameName']
                redsup_tag = player[count]['riotIdTagline']
                redsup_kills = player[count]['kills']
                redsup_deaths = player[count]['deaths']
                redsup_assists = player[count]['assists']
                redsup_kp = round(player[count]['killParticipation'], 2)
                redsup_kda = round(player[count]['kda'], 2)
                redsup_dmg = player[count]['totalDamageDealtToChampions']
                redsup_taken = player[count]['totalDamageTaken']
                redsup_vision = player[count]['visionScore']
                redsup_summoner1 = player[count]['summoner1Id']
                redsup_summoner2 = player[count]['summoner2Id']
                redsup_minions = player[count]['totalMinionsKilled']
                redsup_champ = data['info']['participants'][count]['championName']
                redsup_item0 = data['info']['participants'][count]['item0']
                redsup_item1 = data['info']['participants'][count]['item1']
                redsup_item2 = data['info']['participants'][count]['item2']
                redsup_item3 = data['info']['participants'][count]['item3']
                redsup_item4 = data['info']['participants'][count]['item4']
                redsup_item5 = data['info']['participants'][count]['item5']
                redsup_rune0 = data['info']['participants'][count]['perks']['styles'][0]['selections'][0]['perk']
                puuid = data['info']['participants'][count]['puuid']
                rank_details = players.fetch_rank(true_region, redsup_id, api_key)
                redsup_rank = rank_details[0]
                redsup_tier = rank_details[1]
                redsup_lp = rank_details[2]
                redsup_item0, redsup_item1, redsup_item2, redsup_item3, redsup_item4, redsup_item5 = get_timeline(region, match_id, api_key, puuid, item_map, redsup_item0, redsup_item1, redsup_item2, redsup_item3, redsup_item4, redsup_item5)
            else:
                return None
        except KeyError as e:
            print(f"KeyError encountered: {e}. Skipping match.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}. Skipping match.")
            return None
    return (timestamp, gameduration, result,
        # Blue Top
        bluetop_id, bluetop_champ, bluetop_item0, bluetop_item1, bluetop_item2, bluetop_item3, bluetop_item4, bluetop_item5, bluetop_rune0, bluetop_rune1, bluetop_rune2, bluetop_rune3, bluetop_rune4, bluetop_rune5, bluetop_rune6, bluetop_rune7, bluetop_rune8,
        
        # Blue JG
        bluejg_id, bluejg_champ, bluejg_item0, bluejg_item1, bluejg_item2, bluejg_item3, bluejg_item4, bluejg_item5, bluejg_rune0, bluejg_rune1, bluejg_rune2, bluejg_rune3, bluejg_rune4, bluejg_rune5, bluejg_rune6, bluejg_rune7, bluejg_rune8,
        
        # Blue Mid
        bluemid_id, bluemid_champ, bluemid_item0, bluemid_item1, bluemid_item2, bluemid_item3, bluemid_item4, bluemid_item5, bluemid_rune0, bluemid_rune1, bluemid_rune2, bluemid_rune3, bluemid_rune4, bluemid_rune5, bluemid_rune6, bluemid_rune7, bluemid_rune8,
 
        # Blue Bot
        bluebot_id, bluebot_champ, bluebot_item0, bluebot_item1, bluebot_item2, bluebot_item3, bluebot_item4, bluebot_item5, bluebot_rune0, bluebot_rune1, bluebot_rune2, bluebot_rune3, bluebot_rune4, bluebot_rune5, bluebot_rune6, bluebot_rune7, bluebot_rune8,
        
        # Blue Sup
        bluesup_id, bluesup_champ, bluesup_item0, bluesup_item1, bluesup_item2, bluesup_item3, bluesup_item4, bluesup_item5, bluesup_rune0, bluesup_rune1, bluesup_rune2, bluesup_rune3, bluesup_rune4, bluesup_rune5, bluesup_rune6, bluesup_rune7, bluesup_rune8,
        
        # Red Top
        redtop_id, redtop_champ, redtop_item0, redtop_item1, redtop_item2, redtop_item3, redtop_item4, redtop_item5, redtop_rune0, redtop_rune1, redtop_rune2, redtop_rune3, redtop_rune4, redtop_rune5, redtop_rune6, redtop_rune7, redtop_rune8,
        
        # Red JG
        redjg_id, redjg_champ, redjg_item0, redjg_item1, redjg_item2, redjg_item3, redjg_item4, redjg_item5, redjg_rune0, redjg_rune1, redjg_rune2, redjg_rune3, redjg_rune4, redjg_rune5, redjg_rune6, redjg_rune7, redjg_rune8,
        
        # Red Mid
        redmid_id, redmid_champ, redmid_item0, redmid_item1, redmid_item2, redmid_item3, redmid_item4, redmid_item5, redmid_rune0, redmid_rune1, redmid_rune2, redmid_rune3, redmid_rune4, redmid_rune5, redmid_rune6, redmid_rune7, redmid_rune8,
        
        # Red Bot
        redbot_id, redbot_champ, redbot_item0, redbot_item1, redbot_item2, redbot_item3, redbot_item4, redbot_item5, redbot_rune0, redbot_rune1, redbot_rune2, redbot_rune3, redbot_rune4, redbot_rune5, redbot_rune6, redbot_rune7, redbot_rune8,
        
        # Red Sup
        redsup_id, redsup_champ, redsup_item0, redsup_item1, redsup_item2, redsup_item3, redsup_item4, redsup_item5, redsup_rune0, redsup_rune1, redsup_rune2, redsup_rune3, redsup_rune4, redsup_rune5, redsup_rune6, redsup_rune7, redsup_rune8
    )


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