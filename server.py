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
import user
from io import BytesIO
from sqlalchemy import create_engine, text
app = Flask(__name__)
CORS(app)  # Enable CORS
API_KEY = players.get_json("API_KEY")
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
    dict_update = {}
    counter = 0
    for game in all_matches:
        counter = counter + 1
        details = match.fetch_match_data(game, puuid, region, item_map, rune_map, dict_update, api_key)
        if details is not None:
            (match_id, gameversion, gamecreation, summoner_team, summoner_champ, summoner_lane, summoner_puuid, gameduration, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, summoner_result,
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
            database.insert_match(engine, match_id, gameversion, gamecreation, summoner_team, summoner_champ, summoner_lane, summoner_puuid, gameduration, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, summoner_result,
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
        if counter == 3:
            break
        break
    #database.update_timestamp(engine, puuid)
    for champ in dict_update:
        for lane in dict_update[champ]:
            database.update_champions(engine, puuid, champ, lane)
            for rune in dict_update[champ][lane]['runes']:
                database.update_runes(engine, puuid, champ, rune, lane)
            for item in dict_update[champ][lane]['items']:
                database.update_items(engine, puuid, champ, item, lane)
            for matchup in dict_update[champ][lane]['matchups']:
                database.update_matchups(engine, puuid, champ, matchup, lane)
    matchhistory = database.fetch_matchHistory(engine, puuid) #match history
    champions = database.fetch_champions(engine, puuid) #champions
    user = database.fetch_player(engine, puuid) #user info
    user_json = {}
    user_json["Matches"] = matchhistory
    user_json["Champions"] = champions
    user_json["User"] = user
    print(user_json)
    return jsonify(user_json)

@app.route("/profile/<region>/<ign>/<tag>/<champion>", methods=['GET'])
def champion(region, ign, tag, champion):
    api_key = players.get_json("API_KEY")
    engine = players.establish_connection()
    fullign = ign + '#' + tag
    player = players.fetch_data(region, fullign, engine, api_key)
    puuid = player[1]
    champ_info = database.fetch_champion(engine, puuid, champion)
    return jsonify(champ_info)
@app.route("/profile/<region>/<ign>/<tag>", methods=['GET', 'POST'])
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
    dict_update = {}
    counter = 0
    for game in all_matches:
        counter = counter + 1
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
        if counter == 3:
            break
    database.update_timestamp(engine, puuid)
    for champ in dict_update:
        database.update_champions(engine, puuid, champ)
        for rune in dict_update[champ]['runes']:
            database.update_runes(engine, puuid, champ, rune)
        for item in dict_update[champ]['items']:
            database.update_items(engine, puuid, champ, item)
        for matchup in dict_update[champ]['matchups']:
            database.update_matchups(engine, puuid, champ, matchup)
    matchhistory = database.fetch_matchHistory(engine, puuid) #match history
    champions = database.fetch_champions(engine, puuid) #champions
    user = database.fetch_player(engine, puuid) #user info
    user_json = {}
    user_json["Matches"] = matchhistory
    user_json["Champions"] = champions
    user_json["User"] = user
    print(user_json)
    return jsonify(user_json)

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

@app.route('/login', methods=['POST'])
def logmein():
    engine = players.establish_connection()
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    login_user = user.login(engine, username, password)
    if login_user == "Success!":
        return jsonify({"success": True, "message": "Successful Login"}), 200
    else:
        return jsonify({"success": False, "message": "Incorrect Username or Password"}), 400


@app.route('/signup', methods=['POST'])
def signup():
    engine = players.establish_connection()
    data = request.get_json()
    username = data.get('username', '')
    email = data.get('email', '')
    password = data.get('password', '')
    created_user = user.create_user(engine, username, email, password)
    if created_user == "Existing User Under Email":
        return jsonify({"success": False, "message": "Email already in use"}), 400
    elif created_user == "Existing Username":
        return jsonify({"success": False, "message": "Username already in use"}), 400
    else:
        return jsonify({"success": True, "message": "Account created successfully"}), 200

# Flask route to handle profile picture upload
@app.route('/update-profile-pic', methods=['POST'])
def update_profile_pic():
    engine = players.establish_connection()
    username = request.form.get('username')
    profile_pic = request.files.get('profilePic')

    if not username or not profile_pic:
        return jsonify({"error": "Username and profile picture are required"}), 400

    # Read the image file as binary data
    image_data = profile_pic.read()

    # Update profile picture binary data in the database
    user.update_profile_picture(engine, username, image_data)

    return jsonify({"message": "Profile picture updated successfully!"}), 200

@app.route('/get-profile-pic/<username>', methods=['GET'])
def get_profile_pic(username):
    engine = players.establish_connection()
    sql = "SELECT profile_pic FROM users WHERE username = :username"
    with engine.connect() as connection:
        result = connection.execute(text(sql), {"username": username}).mappings().fetchone()

        # Now result is a dictionary, so you can access it by column name
        if not result or not result['profile_pic']:
            return jsonify({"error": "Profile picture not found"}), 404

        # Return the image as a file-like object
        return send_file(BytesIO(result['profile_pic']), mimetype='image/jpeg')  # Adjust mimetype as needed


if __name__ == "__main__":
    app.run(debug=True, port=5000)
