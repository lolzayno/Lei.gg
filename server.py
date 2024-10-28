from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import requests
import datetime
import pytz
from datetime import datetime
import database
import match
import players
app = Flask(__name__)
CORS(app)  # Enable CORS
API_KEY = database.get_json("API_KEY")
@app.route("/", methods=['POST'])
def profile():
    engine = players.establish_connection()
    api_key = players.get_json("API_KEY")
    data = request.get_json()
    ign = data.get('summonerName', '')
    region = data.get('region', '')
    player = players.fetch_data(region, ign, engine, api_key)
    puuid = player[1]
    last_updated = player[4]
    patch = match.fetch_patch()
    item_map = match.fetch_item(patch)
    rune_map = match.fetch_rune(patch)
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
        for rune in dict_update[champ]['runes']:
            database.update_runes(engine, puuid, champ, rune)
        for item in dict_update[champ]['items']:
            database.update_items(engine, puuid, champ, item)
        for matchup in dict_update[champ]['matchups']:
            database.update_matchups(engine, puuid, champ, matchup)
    matchhistory = database.fetch_matchHistory(engine, puuid) #match history
    champions = database.fetch_champions(engine, puuid) #champions
    user = database.fetch_player(engine, puuid) #user info
    return

@app.route("/profile/<region>/<ign>/<tag>/<champion>", methods=['GET'])
def champion(region, ign, tag, champion):
    api_key = players.get_json("API_KEY")
    engine = players.establish_connection()
    fullign = ign + '#' + tag
    player = players.fetch_data(region, fullign, engine, api_key)
    puuid = player[1]
    champ_info = database.fetch_averages(engine, puuid)
    return champ_info
@app.route("/profile/<region>/<ign>/<tag>", methods=['POST'])
def updateprofile(region, ign, tag):
    engine = players.establish_connection()
    api_key = players.get_json("API_KEY")
    data = request.get_json()
    ign = data.get('summonerName', '')
    region = data.get('region', '')
    player = players.fetch_data(region, ign, engine, api_key)
    puuid = player[1]
    last_updated = player[4]
    patch = match.fetch_patch()
    item_map = match.fetch_item(patch)
    rune_map = match.fetch_rune(patch)
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
        for rune in dict_update[champ]['runes']:
            database.update_runes(engine, puuid, champ, rune)
        for item in dict_update[champ]['items']:
            database.update_items(engine, puuid, champ, item)
        for matchup in dict_update[champ]['matchups']:
            database.update_matchups(engine, puuid, champ, matchup)
    matchhistory = database.fetch_matchHistory(engine, puuid) #match history
    champions = database.fetch_champions(engine, puuid) #champions
    user = database.fetch_player(engine, puuid) #user info

@app.route("/profile/<region>/<ign>/<tag>/<champion>", methods=['POST'])
def updatechampion(region, ign, tag, champion):
    engine = players.establish_connection()
    api_key = players.get_json("API_KEY")
    data = request.get_json()
    ign = data.get('summonerName', '')
    region = data.get('region', '')
    player = players.fetch_data(region, ign, engine, api_key)
    puuid = player[1]
    last_updated = player[4]
    patch = match.fetch_patch()
    item_map = match.fetch_item(patch)
    rune_map = match.fetch_rune(patch)
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
        for rune in dict_update[champ]['runes']:
            database.update_runes(engine, puuid, champ, rune)
        for item in dict_update[champ]['items']:
            database.update_items(engine, puuid, champ, item)
        for matchup in dict_update[champ]['matchups']:
            database.update_matchups(engine, puuid, champ, matchup)
    matchhistory = database.fetch_matchHistory(engine, puuid) #match history
    champions = database.fetch_champions(engine, puuid) #champions
    user = database.fetch_player(engine, puuid) #user info
@app.route('//riot.txt', methods=['GET'])
def riot_file():
    return send_file('riot.txt')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
