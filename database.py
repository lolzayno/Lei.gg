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

def update_runes(engine, puuid, champion, rune):
    # SQL to check if the record already exists
    check_sql = """
    SELECT 1 FROM runes
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND rune = :rune
    """
    
    # SQL to insert a new record
    insert_sql = """
    INSERT INTO runes (
        summoner_puuid, champion, rune, games, wins, losses, winrate, variable1, variable2, variable3
    ) VALUES (
        :summoner_puuid, :champion, :rune, :games, :wins, :losses, :winrate, :variable1, :variable2, :variable3
    )
    """
    
    # SQL to update an existing record
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
    """
    
    rune_win = 0
    avg_var1 = 0
    avg_var2 = 0
    avg_var3 = 0
    
    with engine.connect() as connection:
        # Fetch match data
        sql = """
        SELECT result, summoner_rune0, summoner_rune1, summoner_rune2, summoner_rune3, summoner_rune4, summoner_rune5, summoner_data
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
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
            "summoner_champ": champion,
            "rune": rune
        }).fetchall()

        if not result:
            print("No matching records found for the given criteria.")
            return

        # Count wins and aggregate variables
        for row in result:
            selection = json.loads(row[7])  # Ensure row[7] is JSON data
            if row[0] == '1':  # Assuming '1' indicates a win
                rune_win += 1
            
            # Aggregate values based on rune matches
            if row[1] == rune:
                avg_var1 += selection.get("summoner_Rune01", 0)
                avg_var2 += selection.get("summoner_Rune02", 0)
                avg_var3 += selection.get("summoner_Rune03", 0)
            elif row[2] == rune:
                avg_var1 += selection.get("summoner_Rune11", 0)
                avg_var2 += selection.get("summoner_Rune12", 0)
                avg_var3 += selection.get("summoner_Rune13", 0)
            elif row[3] == rune:
                avg_var1 += selection.get("summoner_Rune21", 0)
                avg_var2 += selection.get("summoner_Rune22", 0)
                avg_var3 += selection.get("summoner_Rune23", 0)
            elif row[4] == rune:
                avg_var1 += selection.get("summoner_Rune31", 0)
                avg_var2 += selection.get("summoner_Rune32", 0)
                avg_var3 += selection.get("summoner_Rune33", 0)
            elif row[5] == rune:
                avg_var1 += selection.get("summoner_Rune41", 0)
                avg_var2 += selection.get("summoner_Rune42", 0)
                avg_var3 += selection.get("summoner_Rune43", 0)
            elif row[6] == rune:
                avg_var1 += selection.get("summoner_Rune51", 0)
                avg_var2 += selection.get("summoner_Rune52", 0)
                avg_var3 += selection.get("summoner_Rune53", 0)

        # Calculate averages
        games = len(result)
        winrate = round(rune_win / games, 2) if games > 0 else 0
        avg_var1 /= games
        avg_var2 /= games
        avg_var3 /= games

        # Check if the record already exists
        exists = connection.execute(text(check_sql), {
            "summoner_puuid": puuid,
            "champion": champion,
            "rune": rune
        }).fetchone()

        try:
            if exists:
                # Record exists, so update it
                connection.execute(text(update_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "rune": rune,
                    "games": games,
                    "wins": rune_win,
                    "losses": games - rune_win,
                    "winrate": winrate,
                    "variable1": avg_var1,
                    "variable2": avg_var2,
                    "variable3": avg_var3
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                # Record does not exist, so insert it
                connection.execute(text(insert_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "rune": rune,
                    "games": games,
                    "wins": rune_win,
                    "losses": games - rune_win,
                    "winrate": winrate,
                    "variable1": avg_var1,
                    "variable2": avg_var2,
                    "variable3": avg_var3
                })
                connection.commit()
                print("Data inserted successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)

def update_items(engine, puuid, champion, item):
    # SQL to check if the record already exists
    check_sql = """
    SELECT 1 FROM items
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND item = :item
    """
    
    # SQL to insert a new record
    insert_sql = """
    INSERT INTO items (
        summoner_puuid, champion, item, games, wins, losses, winrate
    ) VALUES (
        :summoner_puuid, :champion, :item, :games, :wins, :losses, :winrate
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
    """
    
    item_win = 0
    
    with engine.connect() as connection:
        # Fetch match data
        sql = """
        SELECT result
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
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
            "summoner_champ": champion,
            "item": item
        }).fetchall()

        if not result:
            print("No matching records found for the given criteria.")
            return

        # Count wins and games
        for row in result:
            if row[0] == '1':  # Assuming '1' indicates a win
                item_win += 1

        games = len(result)
        winrate = round(item_win / games, 2) if games > 0 else 0

        # Check if the record already exists
        exists = connection.execute(text(check_sql), {
            "summoner_puuid": puuid,
            "champion": champion,
            "item": item
        }).fetchone()

        try:
            if exists:
                # Record exists, so update it
                connection.execute(text(update_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "item": item,
                    "games": games,
                    "wins": item_win,
                    "losses": games - item_win,
                    "winrate": winrate
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                # Record does not exist, so insert it
                connection.execute(text(insert_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "item": item,
                    "games": games,
                    "wins": item_win,
                    "losses": games - item_win,
                    "winrate": winrate
                })
                connection.commit()
                print("Data inserted successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)


def update_matchups(engine, puuid, champion, matchup):
    # SQL to check if the record already exists
    check_sql = """
    SELECT 1 FROM matchups
    WHERE summoner_puuid = :summoner_puuid
    AND champion = :champion
    AND matchup = :matchup
    """
    
    # SQL to insert a new record
    insert_sql = """
    INSERT INTO matchups (
        summoner_puuid, champion, matchup, games, wins, losses, winrate
    ) VALUES (
        :summoner_puuid, :champion, :matchup, :games, :wins, :losses, :winrate
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
    """
    
    matchup_win = 0
    
    with engine.connect() as connection:
        # Fetch match data
        sql = """
        SELECT result
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
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
            "summoner_champ": champion,
            "matchup": matchup
        }).fetchall()

        if not result:
            print("No matching records found for the given criteria.")
            return

        # Count wins and games
        for row in result:
            if row[0] == '1':  # Assuming '1' indicates a win
                matchup_win += 1

        games = len(result)
        winrate = round(matchup_win / games, 2) if games > 0 else 0

        # Check if the record already exists
        exists = connection.execute(text(check_sql), {
            "summoner_puuid": puuid,
            "champion": champion,
            "matchup": matchup
        }).fetchone()

        try:
            if exists:
                # Record exists, so update it
                connection.execute(text(update_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "matchup": matchup,
                    "games": games,
                    "wins": matchup_win,
                    "losses": games - matchup_win,
                    "winrate": winrate
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                # Record does not exist, so insert it
                connection.execute(text(insert_sql), {
                    "summoner_puuid": puuid,
                    "champion": champion,
                    "matchup": matchup,
                    "games": games,
                    "wins": matchup_win,
                    "losses": games - matchup_win,
                    "winrate": winrate
                })
                connection.commit()
                print("Data inserted successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)