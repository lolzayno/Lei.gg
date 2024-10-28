from sqlalchemy import create_engine, text
import os
import json
import requests
import datetime
import pytz
from datetime import datetime
import database
import match
def establish_connection():
    engine = create_engine(f'mysql+mysqlconnector://{get_json("user")}:{get_json("host_pw")}@{get_json("host_host")}/{get_json("database")}')
    try:
        with engine.connect() as connection:
            print("Connection to the database was successful!")
    except Exception as e:
        print(f"Error: {e}")

    return engine

def get_json(subject):
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, 'config.json')

    with open(config_path, 'r') as file:
        config = json.load(file)

    return config.get(subject)

def fetch_id(region, ingame_ign, api_key):
    split_name = ingame_ign.split('#') #splits into ign and tag
    ingame_ign = split_name[0] #ign
    ingame_tag = split_name[1] #tag
    #true region calculation for api requests
    if region in ['BR1', 'LA1', 'LA2', 'NA1', 'OC1']:
        region = 'americas'
    elif region in ['JP1', 'KR']:
        region = 'asia'
    elif region in ['EUW1', 'EUN1', 'RU', 'TR1', 'ME1']:
        region = 'europe'
    else:
        region = 'sea'
    #api request url
    id_api_url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{ingame_ign}/{ingame_tag}?api_key={api_key}'
    fetched_info = requests.get(id_api_url) #actual api request
    if fetched_info.status_code == 404: #if errors
        print("Invalid Ign")
        return "Invalid Ign"
    fetched_info = fetched_info.json()
    fetched_id = fetched_info['puuid']
    return fetched_id

def fetch_additional(true_region, puuid, api_key):
    specific_url = f"https://{true_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    response = requests.get(specific_url)
    data = response.json()
    return data['id'], data['accountId'], data['profileIconId'], data['summonerLevel']
    
def fetch_rank(true_region, summoner_id, api_key):
    specific_rank_url = f"https://{true_region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    response = requests.get(specific_rank_url)
    if len(response.json()) != 0:
        data = response.json()[0]
        return data['tier'], data['rank'], data['leaguePoints'], data['wins'], data['losses']
    else:
        return 'None', 'None', 0, 0, 0

def fetch_data(region, ign, engine, api_key):
    puuid = fetch_id(region, ign, api_key)
    summoner_id, account_id, profile_icon, summoner_level = fetch_additional(region, puuid, api_key)
    account_info = {
        "summoner_id": summoner_id,
        "account_id": account_id,
        "profile_icon": profile_icon,
        "summoner_level": summoner_level
    }
    tier, rank, lp, wins, losses = fetch_rank(region, summoner_id, api_key)
    rank_info = {
        "Rank": tier,
        "Tier": rank,
        "LP": lp,
        "Games": wins + losses,
        "Wins": wins,
        "Losses": losses,   
        "WR": round(wins / (wins + losses), 2)
    }
    player = database.insert_player(engine, puuid, json.dumps(account_info), json.dumps(rank_info))
    return player



if __name__ == '__main__':
    engine = establish_connection()
    api_key = get_json("API_KEY")
    region = "NA1"
    ign = "Zayno#NA1"
    player = fetch_data(region, ign, engine, api_key)
    puuid = player[1]
    last_updated = player[4]
    patch = match.fetch_patch()
    item_map = match.fetch_item(patch)
    rune_map = match.fetch_rune(patch)
    time_zone = pytz.timezone('America/Los_Angeles')
    all_matches = match.fetch_matches(region, puuid, int(last_updated.timestamp()), api_key)
    database.update_timestamp(engine, puuid)
    dict_update = {}
    for game in all_matches:
        details = match.fetch_match_data(game, puuid, region, item_map, rune_map, dict_update, api_key)
        if details is not None:
            (match_id, summoner_champ, summoner_lane, summoner_puuid, gameduration, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, summoner_result,
                bluetop_champ, bluetop_data,
                redtop_champ, redtop_data,
                bluejg_champ, bluejg_data,
                redjg_champ, redjg_data,
                bluemid_champ, bluemid_data,
                redmid_champ, redmid_data,
                bluebot_champ, bluebot_data,
                redbot_champ, redbot_data,
                bluesup_champ, bluesup_data,
                redsup_champ, redsup_data) = details
            database.insert_match(engine, match_id, summoner_champ, summoner_lane, summoner_puuid, gameduration, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, summoner_result,
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
        break
    for champ in dict_update:
        database.update_champions(engine, puuid, champ)
        for rune in dict_update[champ]['runes']:
            database.update_runes(engine, puuid, champ, rune)
        for item in dict_update[champ]['items']:
            database.update_items(engine, puuid, champ, item)
        for matchup in dict_update[champ]['matchups']:
            database.update_matchups(engine, puuid, champ, matchup)
