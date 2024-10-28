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
            print(player)
            return player
        except Exception as e:
            transaction.rollback()
            raise e
        
def update_time(engine, puuid, last_updated):
    update_sql = """
    UPDATE players
    SET
        last_updated = :last_updated
    WHERE puuid = :puuid
    """
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(text(update_sql),{
                "puuid": puuid,
                "last_updated": last_updated
            })
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        
def insert_match(engine, match_id, summoner_champ, summoner_lane, summoner_puuid, gameduration, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, summoner_result,
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
    INSERT INTO matches(match_code, game_duration, result, summoner_puuid, summoner_champ, summoner_lane, summoner_item0, summoner_item1, summoner_item2, summoner_item3, summoner_item4, summoner_item5, summoner_item6, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data, bluetop_champ, bluetop_data, redtop_champ, redtop_data, bluejg_champ, bluejg_data, redjg_champ, redjg_data, bluemid_champ, bluemid_data, redmid_champ, redmid_data, bluebot_champ, bluebot_data, redbot_champ, redbot_data, bluesup_champ, bluesup_data, redsup_champ, redsup_data) VALUES (:match_code, :game_duration, :result, :summoner_puuid, :summoner_champ, :summoner_lane, :summoner_item0, :summoner_item1, :summoner_item2, :summoner_item3, :summoner_item4, :summoner_item5, :summoner_item6, :summoner_rune0, :summoner_rune1, :summoner_rune2, :summoner_rune3, :summoner_rune4, :summoner_rune5, :summoner_data, :bluetop_champ, :bluetop_data, :redtop_champ, :redtop_data, :bluejg_champ, :bluejg_data, :redjg_champ, :redjg_data, :bluemid_champ, :bluemid_data, :redmid_champ, :redmid_data, :bluebot_champ, :bluebot_data, :redbot_champ, :redbot_data, :bluesup_champ, :bluesup_data, :redsup_champ, :redsup_data)
    """

    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(text(insert_sql),{
                "match_code": match_id,
                "game_duration": gameduration,
                "result": summoner_result,
                "summoner_puuid": summoner_puuid,
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