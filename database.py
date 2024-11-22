from sqlalchemy import create_engine, text
import pytz
import datetime
from datetime import datetime
import json
def insert_player(engine, puuid, summoner_info, summoner_rank):
    check_sql = """
    SELECT COUNT(*) FROM players
    WHERE puuid = :puuid
    """
    update_sql = """
    UPDATE players
    SET
        summoner_info = :summoner_info,
        summoner_rank = :summoner_rank
    WHERE puuid = :puuid
    """
    insert_sql = """
    INSERT INTO players(puuid, summoner_info, summoner_rank, last_updated) VALUES (:puuid, :summoner_info, :summoner_rank, :last_updated)
    """
    fetch_sql = """
    SELECT * FROM players
    WHERE puuid = :puuid
    """
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            result = connection.execute(text(check_sql), {
                "puuid": puuid
            })
            count = result.scalar()
            if count > 0:
                print("Found Existing Puuid")
                connection.execute(text(update_sql),{
                    "puuid": puuid,
                    "summoner_info": summoner_info,
                    "summoner_rank": summoner_rank,
                })
            else:
                print("Inserting New Player")
                time_zone = pytz.timezone('America/Los_Angeles')
                season_start = datetime(2024, 9, 25, 12, 0, 0, tzinfo=time_zone)
                connection.execute(text(insert_sql), {
                    "puuid": puuid,
                    "summoner_info": summoner_info,
                    "summoner_rank": summoner_rank,
                    "last_updated": season_start
                })
            transaction.commit()
            fetch = connection.execute(text(fetch_sql), {
                "puuid": puuid
            })
            player = fetch.fetchone()
            return player
        except Exception as e:
            transaction.rollback()
            raise e
        
        
def insert_match(engine, match_id, gameversion, gamecreation, summoner_team, summoner_champ, summoner_lane, summoner_puuid, gameduration, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, summoner_result,
                bluetop_champ, bluetop_data,
                redtop_champ, redtop_data,
                bluejg_champ, bluejg_data,
                redjg_champ, redjg_data,
                bluemid_champ, bluemid_data,
                redmid_champ, redmid_data,
                bluebot_champ, bluebot_data,
                redbot_champ, redbot_data,
                bluesup_champ, bluesup_data,
                redsup_champ, redsup_data):
    insert_sql = """
    INSERT INTO matches(match_code, game_version, game_creation, game_duration, result, summoner_puuid, summoner_team, summoner_champ, summoner_lane, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, bluetop_champ, bluetop_data, redtop_champ, redtop_data, bluejg_champ, bluejg_data, redjg_champ, redjg_data, bluemid_champ, bluemid_data, redmid_champ, redmid_data, bluebot_champ, bluebot_data, redbot_champ, redbot_data, bluesup_champ, bluesup_data, redsup_champ, redsup_data) VALUES (:match_code, :game_version, :game_creation, :game_duration, :result, :summoner_puuid, :summoner_team, :summoner_champ, :summoner_lane, :summoner_item0, :summoner_item1, :summoner_item2, :summoner_item3, :summoner_item4, :summoner_item5, :summoner_item6, :summoner_rune0, :summoner_rune1, :summoner_rune2, :summoner_rune3, :summoner_rune4, :summoner_rune5, :summoner_data, :bluetop_champ, :bluetop_data, :redtop_champ, :redtop_data, :bluejg_champ, :bluejg_data, :redjg_champ, :redjg_data, :bluemid_champ, :bluemid_data, :redmid_champ, :redmid_data, :bluebot_champ, :bluebot_data, :redbot_champ, :redbot_data, :bluesup_champ, :bluesup_data, :redsup_champ, :redsup_data)
    """

    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(text(insert_sql),{
                "match_code": match_id,
                "game_version": gameversion,
                "game_creation": gamecreation,
                "game_duration": gameduration,
                "result": summoner_result,
                "summoner_puuid": summoner_puuid,
                "summoner_team": summoner_team,
                "summoner_champ": summoner_champ,
                "summoner_lane": summoner_lane,
                "summoner_item0": summoner_item0,
                "summoner_item1": summoner_item1,
                "summoner_item2": summoner_item2,
                "summoner_item3": summoner_item3,
                "summoner_item4": summoner_item4,
                "summoner_item5": summoner_item5,
                "summoner_item6": summoner_item6,
                "summoner_rune0": summoner_rune0,
                "summoner_rune1": summoner_rune1,
                "summoner_rune2": summoner_rune2,
                "summoner_rune3": summoner_rune3,
                "summoner_rune4": summoner_rune4,
                "summoner_rune5": summoner_rune5,
                "summoner_data": json.dumps(summoner_data),
                "bluetop_champ": bluetop_champ,
                "bluetop_data": json.dumps(bluetop_data),
                "redtop_champ": redtop_champ,
                "redtop_data": json.dumps(redtop_data),
                "bluejg_champ": bluejg_champ,
                "bluejg_data": json.dumps(bluejg_data),
                "redjg_champ": redjg_champ,
                "redjg_data": json.dumps(redjg_data),
                "bluemid_champ": bluemid_champ,
                "bluemid_data": json.dumps(bluemid_data),
                "redmid_champ": redmid_champ,
                "redmid_data": json.dumps(redmid_data),
                "bluebot_champ": bluebot_champ,
                "bluebot_data": json.dumps(bluebot_data),
                "redbot_champ": redbot_champ,
                "redbot_data": json.dumps(redbot_data),
                "bluesup_champ": bluesup_champ,
                "bluesup_data": json.dumps(bluesup_data),
                "redsup_champ": redsup_champ,
                "redsup_data": json.dumps(redsup_data)
            })
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e

def fetch_matchHistory(engine, puuid):
    sql = """
    SELECT * FROM matches
    WHERE summoner_puuid = :puuid
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "puuid": puuid,
        }).fetchall()
         
        parsed_results = []
        with engine.connect() as connection:
            result = connection.execute(text(sql), {"puuid": puuid}).fetchall()
            
            for row in result:
                # Convert row to dictionary using _mapping for dictionary-like access
                row_dict = dict(row._mapping)
                # Assuming the JSON data is in a column called "json_data"
                row_dict["summoner_data"] = json.loads(row_dict["summoner_data"])  # Parse JSON field
                row_dict["bluetop_data"] = json.loads(row_dict["bluetop_data"])
                row_dict["redtop_data"] = json.loads(row_dict["redtop_data"])
                row_dict["bluejg_data"] = json.loads(row_dict["bluejg_data"])
                row_dict["redjg_data"] = json.loads(row_dict["redjg_data"])
                row_dict["bluemid_data"] = json.loads(row_dict["bluemid_data"])
                row_dict["redmid_data"] = json.loads(row_dict["redmid_data"])
                row_dict["bluebot_data"] = json.loads(row_dict["bluebot_data"])
                row_dict["redbot_data"] = json.loads(row_dict["redbot_data"])
                row_dict["bluesup_data"] = json.loads(row_dict["bluesup_data"])
                row_dict["redsup_data"] = json.loads(row_dict["redsup_data"])

                parsed_results.append(row_dict)

        return parsed_results

def fetch_champions(engine, puuid):
    sql = """
    SELECT * FROM champions
    WHERE puuid = :puuid
    """

    parsed_results = []
    with engine.connect() as connection:
        result = connection.execute(text(sql), {"puuid": puuid}).fetchall()
        
        for row in result:
            # Convert row to dictionary using _mapping for dictionary-like access
            row_dict = dict(row._mapping)
            # Assuming the JSON data is in a column called "json_data"
            if "json_data" in row_dict:
                try:
                    row_dict["json_data"] = json.loads(row_dict["json_data"])  # Parse JSON field
                except json.JSONDecodeError:
                    print(f"Error decoding JSON for row with ID {row_dict.get('id')}")

            parsed_results.append(row_dict)
    return parsed_results

def fetch_champion(engine, puuid, champion):
    sql = """
    SELECT * FROM champions
    WHERE puuid = :puuid
    AND champion = :champion
    """

    parsed_results = []
    with engine.connect() as connection:
        result = connection.execute(text(sql), {"puuid": puuid, "champion": champion}).fetchall()
        
        for row in result:
            # Convert row to dictionary using _mapping for dictionary-like access
            row_dict = dict(row._mapping)
            # Assuming the JSON data is in a column called "json_data"
            if "json_data" in row_dict:
                try:
                    row_dict["json_data"] = json.loads(row_dict["json_data"])  # Parse JSON field
                except json.JSONDecodeError:
                    print(f"Error decoding JSON for row with ID {row_dict.get('id')}")

            parsed_results.append(row_dict)
    return parsed_results

def fetch_player(engine, puuid):
    sql = """
    SELECT * FROM players
    WHERE puuid = :puuid
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "puuid": puuid,
        }).fetchall()
        
        return list(result[0][:4])
    
def update_timestamp(engine, puuid):
    update_sql = """
    UPDATE players
    SET last_updated = :last_updated
    WHERE puuid = :puuid
    """

    with engine.connect() as connection:
        result = connection.execute(text(update_sql), {
            "puuid": puuid,
            "last_updated": datetime.now()
        })
        connection.commit()
        return
    
def fetch_games(engine, puuid, champion, lane):
    if lane == "OVERALL":
        sql = """
        SELECT
            COUNT(*) AS games_played,
            SUM(CASE WHEN CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS total_wins,
            SUM(CASE WHEN game_duration < 1200 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_under_1200,
            SUM(CASE WHEN game_duration < 1200 THEN 1 ELSE 0 END) as games_under_1200, 
            SUM(CASE WHEN game_duration >= 1200 AND game_duration < 1500 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_1200_1500,
            SUM(CASE WHEN game_duration >= 1200 AND game_duration < 1500 THEN 1 ELSE 0 END) AS games_between_1200_1500,
            SUM(CASE WHEN game_duration >= 1500 AND game_duration < 1800 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_1500_1800,
            SUM(CASE WHEN game_duration >= 1500 AND game_duration < 1800 THEN 1 ELSE 0 END) AS games_between_1500_1800,
            SUM(CASE WHEN game_duration >= 1800 AND game_duration < 2100 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_1800_2100,
            SUM(CASE WHEN game_duration >= 1800 AND game_duration < 2100 THEN 1 ELSE 0 END) AS games_between_1800_2100,
            SUM(CASE WHEN game_duration >= 2100 AND game_duration < 2400 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_2100_2400,
            SUM(CASE WHEN game_duration >= 2100 AND game_duration < 2400 THEN 1 ELSE 0 END) AS games_between_2100_2400,
            SUM(CASE WHEN game_duration >= 2400 AND game_duration < 2700 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_2400_2700,
            SUM(CASE WHEN game_duration >= 2400 AND game_duration < 2700 THEN 1 ELSE 0 END) AS games_between_2400_2700,
            SUM(CASE WHEN game_duration >= 2700 AND game_duration < 3000 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_2700_3000,
            SUM(CASE WHEN game_duration >= 2700 AND game_duration < 3000 THEN 1 ELSE 0 END) AS games_between_2700_3000,
            SUM(CASE WHEN game_duration >= 3000 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_over_3000,
            SUM(CASE WHEN game_duration >= 3000 THEN 1 ELSE 0 END) AS games_over_3000
        FROM matches
        WHERE summoner_puuid = :puuid
        AND summoner_champ = :champion
        """
    else:
        sql = """
        SELECT
            COUNT(*) AS games_played,
            SUM(CASE WHEN CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS total_wins,
            SUM(CASE WHEN game_duration < 1200 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_under_1200,
            SUM(CASE WHEN game_duration < 1200 THEN 1 ELSE 0 END) as games_under_1200, 
            SUM(CASE WHEN game_duration >= 1200 AND game_duration < 1500 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_1200_1500,
            SUM(CASE WHEN game_duration >= 1200 AND game_duration < 1500 THEN 1 ELSE 0 END) AS games_between_1200_1500,
            SUM(CASE WHEN game_duration >= 1500 AND game_duration < 1800 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_1500_1800,
            SUM(CASE WHEN game_duration >= 1500 AND game_duration < 1800 THEN 1 ELSE 0 END) AS games_between_1500_1800,
            SUM(CASE WHEN game_duration >= 1800 AND game_duration < 2100 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_1800_2100,
            SUM(CASE WHEN game_duration >= 1800 AND game_duration < 2100 THEN 1 ELSE 0 END) AS games_between_1800_2100,
            SUM(CASE WHEN game_duration >= 2100 AND game_duration < 2400 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_2100_2400,
            SUM(CASE WHEN game_duration >= 2100 AND game_duration < 2400 THEN 1 ELSE 0 END) AS games_between_2100_2400,
            SUM(CASE WHEN game_duration >= 2400 AND game_duration < 2700 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_2400_2700,
            SUM(CASE WHEN game_duration >= 2400 AND game_duration < 2700 THEN 1 ELSE 0 END) AS games_between_2400_2700,
            SUM(CASE WHEN game_duration >= 2700 AND game_duration < 3000 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_between_2700_3000,
            SUM(CASE WHEN game_duration >= 2700 AND game_duration < 3000 THEN 1 ELSE 0 END) AS games_between_2700_3000,
            SUM(CASE WHEN game_duration >= 3000 AND CAST(result AS UNSIGNED) = 1 THEN 1 ELSE 0 END) AS wins_over_3000,
            SUM(CASE WHEN game_duration >= 3000 THEN 1 ELSE 0 END) AS games_over_3000
        FROM matches
        WHERE summoner_puuid = :puuid
        AND summoner_champ = :champion
        AND summoner_lane = :lane
        """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "puuid": puuid,
            "champion": champion,
            "lane": lane
        }).fetchone()
        
        # Extract the counts into separate variables
        games_played = int(result[0])
        total_wins = int(result[1])
        wins_under_1200 = int(result[2])
        games_under_1200 = int(result[3])
        wins_between_1200_1500 = int(result[4])
        games_between_1200_1500 = int(result[5])
        wins_between_1500_1800 = int(result[6])
        games_between_1500_1800 = int(result[7])
        wins_between_1800_2100 = int(result[8])
        games_between_1800_2100 = int(result[9])
        wins_between_2100_2400 = int(result[10])
        games_between_2100_2400 = int(result[11])
        wins_between_2400_2700 = int(result[12])
        games_between_2400_2700 = int(result[13])
        wins_between_2700_3000 = int(result[14])
        games_between_2700_3000 = int(result[15])
        wins_over_3000 = int(result[16])
        games_over_3000 = int(result[17])

        # Helper function to calculate winrate
        def calculate_wr(wins, games):
            return round(wins / games, 2) if games > 0 else 0

        game_info = {
            "games_played": games_played,
            "games_won": total_wins,
            "games_lost": games_played - total_wins,
            "games_wr": calculate_wr(total_wins, games_played),
            "wins_under_20": wins_under_1200,
            "games_under_20": games_under_1200,
            "wr_under_20": calculate_wr(wins_under_1200, games_under_1200),
            "wins_under_25": wins_between_1200_1500,
            "games_under_25": games_between_1200_1500,
            "wr_under_25": calculate_wr(wins_between_1200_1500, games_between_1200_1500),
            "wins_under_30": wins_between_1500_1800,
            "games_under_30": games_between_1500_1800,
            "wr_under_30": calculate_wr(wins_between_1500_1800, games_between_1500_1800),
            "wins_under_35": wins_between_1800_2100,
            "games_under_35": games_between_1800_2100,
            "wr_under_35": calculate_wr(wins_between_1800_2100, games_between_1800_2100),
            "wins_under_40": wins_between_2100_2400,
            "games_under_40": games_between_2100_2400,
            "wr_under_40": calculate_wr(wins_between_2100_2400, games_between_2100_2400),
            "wins_under_45": wins_between_2400_2700,
            "games_under_45": games_between_2400_2700,
            "wr_under_45": calculate_wr(wins_between_2400_2700, games_between_2400_2700),
            "wins_under_50": wins_between_2700_3000,
            "games_under_50": games_between_2700_3000,
            "wr_under_50": calculate_wr(wins_between_2700_3000, games_between_2700_3000),
            "wins_over_50": wins_over_3000,
            "games_over_50": games_over_3000,
            "wr_over_50": calculate_wr(wins_over_3000, games_over_3000)
        }
        print(game_info)
        return game_info

def update_champions(engine, puuid, champion, lane, game_info):
    if lane == "OVERALL":
        sql = """
        SELECT
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_AllInPings')), 2) AS avg_allin,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_AssistMePings')), 2) AS avg_assistme,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Pings')), 2) AS avg_pings,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_CommandPings')), 2) AS avg_commandping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DangerPing')), 2) AS avg_dangerping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MissingPing')), 2) AS avg_missingping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionPing')), 2) AS avg_visionping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_BackPing')), 2) AS avg_backping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_HoldPing')), 2) AS avg_holdping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_NeedVisionPing')), 2) AS avg_needvisionping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_OnMyWayPing')), 2) AS avg_onmywayping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_PushPings')), 2) AS avg_pushpings,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_SupportItem')), 2) AS avg_supportitem,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_ControlWard')), 2) AS avg_controlward,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamagePerMin')), 2) AS avg_damagepermin,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamageTaken')), 2) AS avg_damagetaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DodgeClose')), 2) AS avg_dodgeclose,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_HealShield')), 2) AS avg_healshield,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_CC')), 2) AS avg_cc,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_EarlyTurretsBeforePlates')), 2) AS avg_earlyturrets,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KDA')), 2) AS avg_kda,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KP')), 2) AS avg_kp,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KillsUnderTurret')), 2) AS avg_killsunderturret,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KnockIntoTeamKill')), 2) AS avg_knockintoteamkill,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_EarlySkillShots')), 2) AS avg_earlyskillshots,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Minions10')), 2) AS avg_minion10,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MaxCSAdvantage')), 2) AS avg_maxcs,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MaxLevelLead')), 2) AS avg_maxlvl,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_RiftHeraldTakedown')), 2) AS avg_rift,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_ScuttleCrabs')), 2) AS avg_scuttle,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalDodges')), 2) AS avg_totaldodge,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalLand')), 2) AS avg_totalland,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_SoloKill')), 2) AS avg_solokill,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Wards')), 2) AS avg_wards,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Baron')), 2) AS avg_baron,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamagePercent')), 2) AS avg_damagepercent,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Plates')), 2) AS avg_plates,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Turrets')), 2) AS avg_turrets,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionAdvantange')), 2) AS avg_visionadvantage,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionScorePerMin')), 2) AS avg_visionscorepermin,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Level')), 2) AS avg_lvl,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Exp')), 2) AS avg_exp,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamageBuilding')), 2) AS avg_damagebuilding,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamageObj')), 2) AS avg_damageobj,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Deaths')), 2) AS avg_deaths,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Dragon')), 2) AS avg_drag,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Kills')), 2) AS avg_kills,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MagicTaken')), 2) AS avg_magictaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MagicDmg')), 2) AS avg_magicdmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_PhysicalTaken')), 2) AS avg_physicaltaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_PhysicalDmg')), 2) AS avg_physicaldmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalDmg')), 2) AS avg_totaldmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalTaken')), 2) AS avg_totaltaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TrueDmg')), 2) AS avg_truedmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TrueTaken')), 2) AS avg_truetaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Q')), 2) AS avg_q,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_W')), 2) AS avg_w,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_E')), 2) AS avg_e,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_R')), 2) AS avg_r,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Spell1Casts')), 2) AS avg_spell1casts,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Spell2Casts')), 2) AS avg_spell2casts,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Team')), 2) AS avg_team,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_CCing')), 2) AS avg_ccing,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionScore')), 2) AS avg_visionscore,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_WardsKilled')), 2) AS avg_wardskilled,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalHealing')), 2) AS avg_totalhealing,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_HealTeam')), 2) AS avg_healteam,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Shield')), 2) AS avg_shield,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Minions')), 2) AS avg_minions
        FROM matches
        WHERE summoner_puuid = :puuid
        AND summoner_champ = :champion
    """
    else:
        sql = """
        SELECT
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_AllInPings')), 2) AS avg_allin,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_AssistMePings')), 2) AS avg_assistme,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Pings')), 2) AS avg_pings,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_CommandPings')), 2) AS avg_commandping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DangerPing')), 2) AS avg_dangerping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MissingPing')), 2) AS avg_missingping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionPing')), 2) AS avg_visionping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_BackPing')), 2) AS avg_backping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_HoldPing')), 2) AS avg_holdping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_NeedVisionPing')), 2) AS avg_needvisionping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_OnMyWayPing')), 2) AS avg_onmywayping,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_PushPings')), 2) AS avg_pushpings,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_SupportItem')), 2) AS avg_supportitem,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_ControlWard')), 2) AS avg_controlward,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamagePerMin')), 2) AS avg_damagepermin,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamageTaken')), 2) AS avg_damagetaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DodgeClose')), 2) AS avg_dodgeclose,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_HealShield')), 2) AS avg_healshield,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_CC')), 2) AS avg_cc,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_EarlyTurretsBeforePlates')), 2) AS avg_earlyturrets,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KDA')), 2) AS avg_kda,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KP')), 2) AS avg_kp,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KillsUnderTurret')), 2) AS avg_killsunderturret,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_KnockIntoTeamKill')), 2) AS avg_knockintoteamkill,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_EarlySkillShots')), 2) AS avg_earlyskillshots,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Minions10')), 2) AS avg_minion10,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MaxCSAdvantage')), 2) AS avg_maxcs,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MaxLevelLead')), 2) AS avg_maxlvl,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_RiftHeraldTakedown')), 2) AS avg_rift,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_ScuttleCrabs')), 2) AS avg_scuttle,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalDodges')), 2) AS avg_totaldodge,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalLand')), 2) AS avg_totalland,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_SoloKill')), 2) AS avg_solokill,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Wards')), 2) AS avg_wards,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Baron')), 2) AS avg_baron,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamagePercent')), 2) AS avg_damagepercent,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Plates')), 2) AS avg_plates,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Turrets')), 2) AS avg_turrets,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionAdvantange')), 2) AS avg_visionadvantage,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionScorePerMin')), 2) AS avg_visionscorepermin,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Level')), 2) AS avg_lvl,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Exp')), 2) AS avg_exp,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamageBuilding')), 2) AS avg_damagebuilding,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_DamageObj')), 2) AS avg_damageobj,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Deaths')), 2) AS avg_deaths,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Dragon')), 2) AS avg_drag,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Kills')), 2) AS avg_kills,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MagicTaken')), 2) AS avg_magictaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_MagicDmg')), 2) AS avg_magicdmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_PhysicalTaken')), 2) AS avg_physicaltaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_PhysicalDmg')), 2) AS avg_physicaldmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalDmg')), 2) AS avg_totaldmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalTaken')), 2) AS avg_totaltaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TrueDmg')), 2) AS avg_truedmg,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TrueTaken')), 2) AS avg_truetaken,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Q')), 2) AS avg_q,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_W')), 2) AS avg_w,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_E')), 2) AS avg_e,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_R')), 2) AS avg_r,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Spell1Casts')), 2) AS avg_spell1casts,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Spell2Casts')), 2) AS avg_spell2casts,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Team')), 2) AS avg_team,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_CCing')), 2) AS avg_ccing,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_VisionScore')), 2) AS avg_visionscore,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_WardsKilled')), 2) AS avg_wardskilled,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_TotalHealing')), 2) AS avg_totalhealing,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_HealTeam')), 2) AS avg_healteam,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Shield')), 2) AS avg_shield,
            ROUND(AVG(JSON_EXTRACT(summoner_data, '$.summoner_Minions')), 2) AS avg_minions
        FROM matches
        WHERE summoner_puuid = :puuid
        AND summoner_champ = :champion
        AND summoner_lane = :lane
    """

    #SQL to insert a new record
    insert_sql = """
    INSERT INTO champions (
        puuid, champion, lane, champ_data, game_data
    ) VALUES (
        :puuid, :champion, :lane, :champ_data, :game_data
    )
    """
    
    update_sql = """
    UPDATE champions
    SET champ_data = :champ_data,
        game_data = :game_data
    WHERE puuid = :puuid
    AND champion = :champion
    AND lane = :lane
    """
    check_sql = """
    SELECT * FROM champions
    WHERE puuid = :puuid
    AND champion = :champion
    AND lane = :lane
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "puuid": puuid,
            "champion": champion,
            "lane": lane
        }).fetchall()

        exists = connection.execute(text(check_sql), {
            "puuid": puuid,
            "champion": champion,
            "lane": lane
        }).fetchall()
        result = result[0]
        summoner_data = {
            "avg_allin": result[0],
            "avg_assistme": result[1],
            "avg_pings": result[2],
            "avg_commandping": result[3],
            "avg_dangerping": result[4],
            "avg_missingping": result[5],
            "avg_visionping": result[6],
            "avg_backping": result[7],
            "avg_holdping": result[8],
            "avg_needvisionping": result[9],
            "avg_onmywayping": result[10],
            "avg_pushpings": result[11],
            "avg_supportitem": result[12],
            "avg_controlward": result[13],
            "avg_damagepermin": result[14],
            "avg_damagetaken": result[15],
            "avg_dodgeclose": result[16],
            "avg_healshield": result[17],
            "avg_cc": result[18],
            "avg_earlyturrets": result[19],
            "avg_kda": result[20],
            "avg_kp": result[21],
            "avg_killsunderturret": result[22],
            "avg_knockintoteamkill": result[23],
            "avg_earlyskillshots": result[24],
            "avg_minion10": result[25],
            "avg_maxcs": result[26],
            "avg_maxlvl": result[27],
            "avg_rift": result[28],
            "avg_scuttle": result[29],
            "avg_totaldodge": result[30],
            "avg_totalland": result[31],
            "avg_solokill": result[32],
            "avg_wards": result[33],
            "avg_baron": result[34],
            "avg_damagepercent": result[35],
            "avg_plates": result[36],
            "avg_turrets": result[37],
            "avg_visionadvantage": result[38],
            "avg_visionscorepermin": result[39],
            "avg_lvl": result[40],
            "avg_exp": result[41],
            "avg_damagebuilding": result[42],
            "avg_damageobj": result[43],
            "avg_deaths": result[44],
            "avg_drag": result[45],
            "avg_kills": result[46],
            "avg_magictaken": result[47],
            "avg_magicdmg": result[48],
            "avg_physicaltaken": result[49],
            "avg_physicaldmg": result[50],
            "avg_totaldmg": result[51],
            "avg_totaltaken": result[52],
            "avg_truedmg": result[53],
            "avg_truetaken": result[54],
            "avg_q": result[55],
            "avg_w": result[56],
            "avg_e": result[57],
            "avg_r": result[58],
            "avg_spell1casts": result[59],
            "avg_spell2casts": result[60],
            "avg_team": result[61],
            "avg_ccing": result[62],
            "avg_visionscore": result[63],
            "avg_wardskilled": result[64],
            "avg_totalhealing": result[65],
            "avg_healteam": result[66],
            "avg_shield": result[67],
            "avg_minions": result[68],
        }
        try:
            if exists:
                # Record exists, so update it
                connection.execute(text(update_sql), {
                    "puuid": puuid,
                    "champion": champion,
                    "lane": lane,
                    "champ_data": json.dumps(summoner_data),
                    "game_data": json.dumps(game_info)
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                connection.execute(text(insert_sql), {
                    "puuid": puuid,
                    "champion": champion,
                    "lane": lane,
                    "champ_data": json.dumps(summoner_data),
                    "game_data": json.dumps(game_info)
                })
                connection.commit()
                print("Data updated successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)
        return summoner_data

def update_matchups(engine, puuid, champion, matchup, lane):
    # Fetch match data with aggregated calculations
    if lane == "OVERALL":
        sql = """
        SELECT 
            COUNT(*) AS total_games,
            SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) AS wins,
            ROUND(SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) / COUNT(*), 2) AS winrate
        FROM matches
        WHERE summoner_puuid = :summoner_puuid
        AND summoner_champ = :summoner_champ
        AND (
            bluetop_champ = :matchup
            OR redtop_champ = :matchup
            OR bluejg_champ = :matchup
            OR redjg_champ = :matchup
            OR bluemid_champ = :matchup
            OR redmid_champ = :matchup
            OR bluebot_champ = :matchup
            OR redbot_champ = :matchup
            OR bluesup_champ = :matchup
            OR redsup_champ = :matchup
        )
        """
    else:
        sql = """
        SELECT 
            COUNT(*) AS total_games,
            SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) AS wins,
            ROUND(SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) / COUNT(*), 2) AS winrate
        FROM matches
        WHERE summoner_puuid = :summoner_puuid
        AND summoner_champ = :summoner_champ
        AND summoner_lane = :lane
        AND (
            bluetop_champ = :matchup
            OR redtop_champ = :matchup
            OR bluejg_champ = :matchup
            OR redjg_champ = :matchup
            OR bluemid_champ = :matchup
            OR redmid_champ = :matchup
            OR bluebot_champ = :matchup
            OR redbot_champ = :matchup
            OR bluesup_champ = :matchup
            OR redsup_champ = :matchup
        )
        """

    # SQL to check if the record already exists
    check_sql = """
    SELECT 1 FROM matchups
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND matchup = :matchup
    AND lane = :lane
    """
    
    # SQL to insert a new record
    insert_sql = """
    INSERT INTO matchups (
        summoner_puuid, champion, lane, matchup, games, wins, losses, winrate
    ) VALUES (
        :summoner_puuid, :champion, :lane, :matchup, :games, :wins, :losses, :winrate
    )
    """
    
    # SQL to update an existing record
    update_sql = """
    UPDATE matchups
    SET games = :games,
        wins = :wins,
        losses = :losses,
        winrate = :winrate
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND matchup = :matchup
    AND lane = :lane
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
            "summoner_champ": champion,
            "lane": lane,
            "matchup": matchup
        }).fetchone()
        games = int(result[0])
        wins = int(result[1])
        winrate = float(result[2])
        losses = games - wins

        # Check if the record already exists
        exists = connection.execute(text(check_sql), {
            "summoner_puuid": puuid,
            "champion": champion,
            "lane": lane,
            "matchup": matchup
        }).fetchone()

        try:
            if exists:
                # Record exists, so update it
                connection.execute(text(update_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "lane": lane,
                    "matchup": matchup,
                    "games": games,
                    "wins": wins,
                    "losses": losses,
                    "winrate": winrate
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                # Record does not exist, so insert it
                connection.execute(text(insert_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "lane": lane,
                    "matchup": matchup,
                    "games": games,
                    "wins": wins,
                    "losses": losses,
                    "winrate": winrate
                })
                connection.commit()
                print("Data inserted successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)

def update_runes(engine, puuid, champion, rune, lane, matchup):
    # Fetch match data with aggregate calculations
    if lane == "OVERALL":
        sql = """
        SELECT 
            COUNT(*) AS total_games,
            SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) AS wins,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune01')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune11')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune21')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune31')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune41')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune51') END), 2) AS variable1,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune02')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune12')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune22')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune32')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune42')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune52') END), 2) AS variable2,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune03')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune13')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune23')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune33')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune43')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune53') END), 2) AS variable3

        FROM matches
        WHERE summoner_puuid = :summoner_puuid
        AND summoner_champ = :summoner_champ
        AND (
            summoner_rune0 = :rune
            OR summoner_rune1 = :rune
            OR summoner_rune2 = :rune
            OR summoner_rune3 = :rune
            OR summoner_rune4 = :rune
            OR summoner_rune5 = :rune
        )
        """
    elif matchup:
        sql = """
        SELECT 
            COUNT(*) AS total_games,
            SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) AS wins,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune01')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune11')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune21')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune31')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune41')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune51') END), 2) AS variable1,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune02')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune12')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune22')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune32')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune42')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune52') END), 2) AS variable2,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune03')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune13')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune23')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune33')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune43')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune53') END), 2) AS variable3

        FROM matches
        WHERE summoner_puuid = :summoner_puuid
        AND summoner_champ = :summoner_champ
        AND (
            summoner_rune0 = :rune
            OR summoner_rune1 = :rune
            OR summoner_rune2 = :rune
            OR summoner_rune3 = :rune
            OR summoner_rune4 = :rune
            OR summoner_rune5 = :rune
        )
        AND (
            bluetop_champ = :matchup
            OR redtop_champ = :matchup
            OR bluejg_champ = :matchup
            OR redjg_champ = :matchup
            OR bluemid_champ = :matchup
            OR redmid_champ = :matchup
            OR bluebot_champ = :matchup
            OR redbot_champ = :matchup
            OR bluesup_champ = :matchup
            OR redsup_champ = :matchup
        )
        """
    else:
        sql = """
        SELECT 
            COUNT(*) AS total_games,
            SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) AS wins,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune01')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune11')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune21')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune31')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune41')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune51') END), 2) AS variable1,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune02')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune12')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune22')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune32')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune42')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune52') END), 2) AS variable2,
            ROUND(AVG(CASE WHEN summoner_rune0 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune03')
                        WHEN summoner_rune1 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune13')
                        WHEN summoner_rune2 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune23')
                        WHEN summoner_rune3 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune33')
                        WHEN summoner_rune4 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune43')
                        WHEN summoner_rune5 = :rune THEN JSON_EXTRACT(summoner_data, '$.summoner_Rune53') END), 2) AS variable3

        FROM matches
        WHERE summoner_puuid = :summoner_puuid
        AND summoner_champ = :summoner_champ
        AND summoner_lane = :lane
        AND (
            summoner_rune0 = :rune
            OR summoner_rune1 = :rune
            OR summoner_rune2 = :rune
            OR summoner_rune3 = :rune
            OR summoner_rune4 = :rune
            OR summoner_rune5 = :rune
        )
        """

    # Check and update database
    check_sql = """
    SELECT 1 FROM runes
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND rune = :rune
    AND lane = :lane
    AND ((:matchup IS NULL AND matchup IS NULL) OR (:matchup IS NOT NULL AND matchup = :matchup))
    """
    insert_sql = """
    INSERT INTO runes (
        summoner_puuid, champion, matchup, lane, rune, games, wins, losses, winrate, variable1, variable2, variable3
    ) VALUES (
        :summoner_puuid, :champion, :matchup, :lane, :rune, :games, :wins, :losses, :winrate, :variable1, :variable2, :variable3
    )
    """
    update_sql = """
    UPDATE runes
    SET games = :games,
        wins = :wins,
        losses = :losses,
        winrate = :winrate,
        variable1 = :variable1,
        variable2 = :variable2,
        variable3 = :variable3
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND rune = :rune
    AND lane = :lane
    AND ((:matchup IS NULL AND matchup IS NULL) OR (:matchup IS NOT NULL AND matchup = :matchup))
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
            "summoner_champ": champion,
            "rune": rune,
            "lane": lane,
            "matchup": matchup
        }).fetchone()

        # Extract values from query result
        games = int(result[0])
        wins = int(result[1])
        losses = games - wins
        winrate = round(wins / games, 2) if games > 0 else 0
        variable1 = float(result[2]) if result[2] else 0
        variable2 = float(result[3]) if result[3] else 0
        variable3 = float(result[4]) if result[4] else 0

        # Check if the record already exists
        exists = connection.execute(text(check_sql), {
            "summoner_puuid": puuid,
            "champion": champion,
            "rune": rune,
            "lane": lane,
            "matchup": matchup
        }).fetchone()

        try:
            if exists:
                # Update existing record
                connection.execute(text(update_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "matchup": matchup,
                    "lane": lane,
                    "rune": rune,
                    "games": games,
                    "wins": wins,
                    "losses": losses,
                    "winrate": winrate,
                    "variable1": variable1,
                    "variable2": variable2,
                    "variable3": variable3
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                # Insert new record
                connection.execute(text(insert_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "matchup": matchup,
                    "lane": lane,
                    "rune": rune,
                    "games": games,
                    "wins": wins,
                    "losses": losses,
                    "winrate": winrate,
                    "variable1": variable1,
                    "variable2": variable2,
                    "variable3": variable3
                })
                connection.commit()
                print("Data inserted successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)

def update_items(engine, puuid, champion, item, lane):
    # Fetch match data with aggregate calculations
    if lane == "OVERALL":
        sql = """
        SELECT 
            COUNT(*) AS total_games,
            SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) AS wins,
            ROUND(SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) / COUNT(*), 2) AS winrate
        FROM matches
        WHERE summoner_puuid = :summoner_puuid
        AND summoner_champ = :summoner_champ
        AND (
            summoner_item0 = :item
            OR summoner_item1 = :item
            OR summoner_item2 = :item
            OR summoner_item3 = :item
            OR summoner_item4 = :item
            OR summoner_item5 = :item
        )
        """
    else:
        sql = """
        SELECT 
            COUNT(*) AS total_games,
            SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) AS wins,
            ROUND(SUM(CASE WHEN result = '1' THEN 1 ELSE 0 END) / COUNT(*), 2) AS winrate
        FROM matches
        WHERE summoner_puuid = :summoner_puuid
        AND summoner_champ = :summoner_champ
        AND summoner_lane = :lane
        AND (
            summoner_item0 = :item
            OR summoner_item1 = :item
            OR summoner_item2 = :item
            OR summoner_item3 = :item
            OR summoner_item4 = :item
            OR summoner_item5 = :item
        )
        """
    # SQL to check if the record already exists
    check_sql = """
    SELECT 1 FROM items
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND item = :item
    AND lane = :lane
    """
    
    # SQL to insert a new record
    insert_sql = """
    INSERT INTO items (
        summoner_puuid, champion, lane, item, games, wins, losses, winrate
    ) VALUES (
        :summoner_puuid, :champion, :lane, :item, :games, :wins, :losses, :winrate
    )
    """
    
    # SQL to update an existing record
    update_sql = """
    UPDATE items
    SET games = :games,
        wins = :wins,
        losses = :losses,
        winrate = :winrate
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND item = :item
    AND lane = :lane
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
            "summoner_champ": champion,
            "lane": lane,
            "item": item
        }).fetchone()


        # Extract values from query result
        games = int(result[0])
        wins = int(result[1])
        losses = games - wins
        winrate = float(result[2])

        # Check if the record already exists
        exists = connection.execute(text(check_sql), {
            "summoner_puuid": puuid,
            "champion": champion,
            "lane": lane,
            "item": item
        }).fetchone()

        try:
            if exists:
                # Record exists, so update it
                connection.execute(text(update_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "lane": lane,
                    "item": item,
                    "games": games,
                    "wins": wins,
                    "losses": losses,
                    "winrate": winrate
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                # Record does not exist, so insert it
                connection.execute(text(insert_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "lane": lane,
                    "item": item,
                    "games": games,
                    "wins": wins,
                    "losses": losses,
                    "winrate": winrate
                })
                connection.commit()
                print("Data inserted successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)
