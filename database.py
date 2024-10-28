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

def fetch_matchHistory(engine, puuid):
    sql = """
    SELECT * FROM matches
    WHERE summoner_puuid = :puuid
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
        }).fetchall()
         
        print(result)
        return result

def fetch_champions(engine, puuid):
    sql = """
    SELECT * FROM champions
    WHERE summoner_puuid = :puuid
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
        }).fetchall()
         
        print(result)
        return result

def fetch_player(engine, puuid):
    sql = """
    SELECT * FROM players
    WHERE puuid = :puuid
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
        }).fetchall()
         
        print(result)
        return result
    
def fetch_averages(engine, puuid, champion):
    sql = """
    SELECT * FROM champions
    WHERE puuid = :puuid
    AND champion = :champion
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "summoner_puuid": puuid,
            "champion": champion
        }).fetchall()
         
        print(result)
        return result
    
def update_champions(engine, puuid, champion):
    sql = """
    SELECT game_duration, result, summoner_champ, summoner_lane, summoner_data
    FROM matches
    WHERE summoner_puuid = :puuid
    AND summoner_champ = :champion
    """

    # SQL to insert a new record
    insert_sql = """
    INSERT INTO champions (
        puuid, champion, champ_data
    ) VALUES (
        :puuid, :champion, :champ_data
    )
    """
    
    # SQL to update an existing record
    update_sql = """
    UPDATE champions
    SET champ_data = :champ_data
    WHERE puuid = :puuid
    AND champion = :champion
    """
    check_sql = """
    SELECT * FROM champions
    WHERE puuid = :puuid
    AND champion = :champion
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "puuid": puuid,
            "champion": champion
        }).fetchall()
        games_played = len(result)
        games_won = 0
        avg_game_duration = 0
        avg_allin = 0
        avg_assistme = 0
        avg_ping = 0
        avg_commandping = 0
        avg_dangerping = 0
        avg_missingping = 0
        avg_visionping = 0
        avg_backping = 0
        avg_holdping = 0
        avg_needvisionping = 0
        avg_onmywayping = 0
        avg_pushpings = 0
        avg_supportitem = 0
        avg_controlward = 0
        avg_damagepermin = 0
        avg_damagetaken = 0
        avg_dodgeclose = 0
        avg_healshield = 0
        avg_cc = 0
        avg_earlyturrets = 0
        avg_kda = 0
        avg_kp = 0
        avg_killsunderturret = 0
        avg_knockintoteamkill = 0
        avg_earlyskillshots = 0
        avg_minion10 = 0
        avg_maxcs = 0
        avg_maxlvl = 0
        avg_rift = 0
        avg_scuttle = 0
        avg_totaldodge = 0
        avg_totalland = 0
        avg_solokill = 0
        avg_wards = 0
        avg_baron = 0
        avg_damagepercent = 0
        avg_plates = 0
        avg_turrets = 0
        avg_visionadvantage = 0
        avg_visionscorepermin = 0
        avg_lvl = 0
        avg_exp = 0
        avg_damagebuilding = 0
        avg_damageobj = 0
        avg_deaths = 0
        avg_drag = 0
        avg_surrender = 0
        avg_kills = 0
        avg_magictaken = 0
        avg_magicdmg = 0
        avg_physicaltaken = 0
        avg_physicaldmg = 0
        avg_totaldmg = 0
        avg_totaltaken = 0
        avg_truedmg = 0
        avg_truetaken = 0
        avg_q = 0
        avg_w = 0
        avg_e = 0
        avg_r = 0
        avg_spell1 = 0
        avg_spell1casts = 0
        avg_spell2 = 0
        avg_spell2casts = 0
        avg_team = 0
        avg_ccing = 0
        avg_visionscore = 0
        avg_wardskilled = 0
        avg_totalhealing = 0
        avg_healteam = 0
        avg_shield = 0
        avg_minions = 0
        for row in result:
            if row[1] == '1':
                games_won += 1
            data = json.loads(row[4])
            avg_game_duration += row[0]
            avg_allin += data["summoner_AllInPings"]
            avg_assistme += data["summoner_AssistMePings"]
            avg_ping += data["summoner_Pings"]
            avg_commandping += data["summoner_CommandPings"]
            avg_dangerping += data["summoner_DangerPing"]
            avg_missingping += data["summoner_MissingPing"]
            avg_visionping += data["summoner_VisionPing"]
            avg_backping += data["summoner_BackPing"]
            avg_holdping += data["summoner_HoldPing"]
            avg_needvisionping += data["summoner_NeedVisionPing"]
            avg_onmywayping += data["summoner_OnMyWayPing"]
            avg_pushpings += data["summoner_PushPings"]
            avg_supportitem += data["summoner_SupportItem"]
            avg_controlward += data["summoner_ControlWard"]
            avg_damagepermin += data["summoner_DamagePerMin"]
            avg_damagetaken += data["summoner_DamageTaken"]
            avg_dodgeclose += data["summoner_DodgeClose"]
            avg_healshield += data["summoner_HealShield"]
            avg_cc += data["summoner_CC"]
            avg_earlyturrets += data["summoner_EarlyTurretsBeforePlates"]
            avg_kda += data["summoner_KDA"]
            avg_kp += data["summoner_KP"]
            avg_killsunderturret += data["summoner_KillsUnderTurret"]
            avg_knockintoteamkill += data["summoner_KnockIntoTeamKill"]
            avg_earlyskillshots += data["summoner_EarlySkillShots"]
            avg_minion10 += data["summoner_Minions10"]
            avg_maxcs += data["summoner_MaxCSAdvantage"]
            avg_maxlvl += data["summoner_MaxLevelLead"]
            avg_rift += data["summoner_RiftHeraldTakedown"]
            avg_scuttle += data["summoner_ScuttleCrabs"]
            avg_totaldodge += data["summoner_TotalDodges"]
            avg_totalland += data["summoner_TotalLand"]
            avg_solokill += data["summoner_SoloKill"]
            avg_wards += data["summoner_Wards"]
            avg_baron += data["summoner_Baron"]
            avg_damagepercent += data["summoner_DamagePercent"]
            avg_plates += data["summoner_Plates"]
            avg_turrets += data["summoner_Turrets"]
            avg_visionadvantage += data["summoner_VisionAdvantange"]
            avg_visionscorepermin += data["summoner_VisionScorePerMin"]
            avg_lvl += data["summoner_Level"]
            avg_exp += data["summoner_Exp"]
            avg_damagebuilding += data["summoner_DamageBuilding"]
            avg_damageobj += data["summoner_DamageObj"]
            avg_deaths += data["summoner_Deaths"]
            avg_drag += data["summoner_Dragon"]
            avg_surrender += data["summoner_Surrender"]
            avg_kills += data["summoner_Kills"]
            avg_magictaken += data["summoner_MagicTaken"]
            avg_magicdmg += data["summoner_MagicDmg"]
            avg_physicaltaken += data["summoner_PhysicalTaken"]
            avg_physicaldmg += data["summoner_PhysicalDmg"]
            avg_totaldmg += data["summoner_TotalDmg"]
            avg_totaltaken += data["summoner_TotalTaken"]
            avg_truedmg += data["summoner_TrueDmg"]
            avg_truetaken += data["summoner_TrueTaken"]
            avg_q += data["summoner_Q"]
            avg_w += data["summoner_W"]
            avg_e += data["summoner_E"]
            avg_r += data["summoner_R"]
            avg_spell1 += data["summoner_Spell1"]
            avg_spell1casts += data["summoner_Spell1Casts"]
            avg_spell2 += data["summoner_Spell2"]
            avg_spell2casts += data["summoner_Spell2Casts"]
            avg_team += data["summoner_Team"]
            avg_ccing += data["summoner_CCing"]
            avg_visionscore += data["summoner_VisionScore"]
            avg_wardskilled += data["summoner_WardsKilled"]
            avg_totalhealing += data["summoner_TotalHealing"]
            avg_healteam += data["summoner_HealTeam"]
            avg_shield += data["summoner_Shield"]
            avg_minions += data["summoner_Minions"]

        avg_game_duration /= len(result)
        avg_allin /= len(result)
        avg_assistme /= len(result)
        avg_ping /= len(result)
        avg_commandping /= len(result)
        avg_dangerping /= len(result)
        avg_missingping /= len(result)
        avg_visionping /= len(result)
        avg_backping /= len(result)
        avg_holdping /= len(result)
        avg_needvisionping /= len(result)
        avg_onmywayping /= len(result)
        avg_pushpings /= len(result)
        avg_supportitem /= len(result)
        avg_controlward /= len(result)
        avg_damagepermin /= len(result)
        avg_damagetaken /= len(result)
        avg_dodgeclose /= len(result)
        avg_healshield /= len(result)
        avg_cc /= len(result)
        avg_earlyturrets /= len(result)
        avg_kda /= len(result)
        avg_kp /= len(result)
        avg_killsunderturret /= len(result)
        avg_knockintoteamkill /= len(result)
        avg_earlyskillshots /= len(result)
        avg_minion10 /= len(result)
        avg_maxcs /= len(result)
        avg_maxlvl /= len(result)
        avg_rift /= len(result)
        avg_scuttle /= len(result)
        avg_totaldodge /= len(result)
        avg_totalland /= len(result)
        avg_solokill /= len(result)
        avg_wards /= len(result)
        avg_baron /= len(result)
        avg_damagepercent /= len(result)
        avg_plates /= len(result)
        avg_turrets /= len(result)
        avg_visionadvantage /= len(result)
        avg_visionscorepermin /= len(result)
        avg_lvl /= len(result)
        avg_exp /= len(result)
        avg_damagebuilding /= len(result)
        avg_damageobj /= len(result)
        avg_deaths /= len(result)
        avg_drag /= len(result)
        avg_surrender /= len(result)
        avg_kills /= len(result)
        avg_magictaken /= len(result)
        avg_magicdmg /= len(result)
        avg_physicaltaken /= len(result)
        avg_physicaldmg /= len(result)
        avg_totaldmg /= len(result)
        avg_totaltaken /= len(result)
        avg_truedmg /= len(result)
        avg_truetaken /= len(result)
        avg_q /= len(result)
        avg_w /= len(result)
        avg_e /= len(result)
        avg_r /= len(result)
        avg_spell1 /= len(result)
        avg_spell1casts /= len(result)
        avg_spell2 /= len(result)
        avg_spell2casts /= len(result)
        avg_team /= len(result)
        avg_ccing /= len(result)
        avg_visionscore /= len(result)
        avg_wardskilled /= len(result)
        avg_totalhealing /= len(result)
        avg_healteam /= len(result)
        avg_shield /= len(result)
        avg_minions /= len(result)
        summoner_data = {
        "summoner_GamesWon": games_won,
        "summoner_GamesLost": games_played - games_won,
        "summoner_GamesPlayed": games_played,
        "summoner_Winrate": round(games_won / games_played, 2),
        "summoner_AllInPings": round(avg_allin, 1),
        "summoner_AssistMePings": round(avg_assistme, 1),
        "summoner_Pings": round(avg_ping, 1),
        "summoner_CommandPings": round(avg_commandping, 1),
        "summoner_DangerPing": round(avg_dangerping, 1),
        "summoner_MissingPing": round(avg_missingping, 1),
        "summoner_VisionPing": round(avg_visionping, 1),
        "summoner_BackPing": round(avg_backping, 1),
        "summoner_HoldPing": round(avg_holdping, 1),
        "summoner_NeedVisionPing": round(avg_needvisionping, 1),
        "summoner_OnMyWayPing": round(avg_onmywayping, 1),
        "summoner_PushPings": round(avg_pushpings, 1),
        "summoner_SupportItem": round(avg_supportitem, 1),
        "summoner_ControlWard": round(avg_controlward, 1),
        "summoner_DamagePerMin": round(avg_damagepermin, 1),
        "summoner_DamageTaken": round(avg_damagetaken, 1),
        "summoner_DodgeClose": round(avg_dodgeclose, 1),
        "summoner_HealShield": round(avg_healshield, 1),
        "summoner_CC": round(avg_cc, 1),
        "summoner_EarlyTurretsBeforePlates": round(avg_earlyturrets, 1),
        "summoner_KDA": round(avg_kda, 2),
        "summoner_KP": round(avg_kp, 2),
        "summoner_KillsUnderTurret": round(avg_killsunderturret, 1),
        "summoner_KnockIntoTeamKill": round(avg_knockintoteamkill, 1),
        "summoner_EarlySkillShots": round(avg_earlyskillshots, 1),
        "summoner_Minions10": round(avg_minion10, 1),
        "summoner_MaxCSAdvantage": round(avg_maxcs, 1),
        "summoner_MaxLevelLead": round(avg_maxlvl, 1),
        "summoner_RiftHeraldTakedown": round(avg_rift, 1),
        "summoner_ScuttleCrabs": round(avg_scuttle, 1),
        "summoner_TotalDodges": round(avg_totaldodge, 1),
        "summoner_TotalLand": round(avg_totalland, 1),
        "summoner_SoloKill": round(avg_solokill, 1),
        "summoner_Wards": round(avg_wards, 1),
        "summoner_Baron": round(avg_baron, 1),
        "summoner_DamagePercent": round(avg_damagepercent, 2),
        "summoner_Plates": round(avg_plates, 1),
        "summoner_Turrets": round(avg_turrets, 1),
        "summoner_VisionAdvantange": round(avg_visionadvantage, 1),
        "summoner_VisionScorePerMin": round(avg_visionscorepermin, 1),
        "summoner_Level": round(avg_lvl, 1),
        "summoner_Exp": round(avg_exp, 1),
        "summoner_DamageBuilding": round(avg_damagebuilding, 1),
        "summoner_DamageObj": round(avg_damageobj, 1),
        "summoner_Deaths": round(avg_deaths, 1),
        "summoner_Dragon": round(avg_drag, 1),
        "summoner_Surrender": round(avg_surrender, 1),
        "summoner_Kills": round(avg_kills, 1),
        "summoner_MagicTaken": round(avg_magictaken, 1),
        "summoner_MagicDmg": round(avg_magicdmg, 1),
        "summoner_PhysicalTaken": round(avg_physicaltaken, 1),
        "summoner_PhysicalDmg": round(avg_physicaldmg, 1),
        "summoner_TotalDmg": round(avg_totaldmg, 1),
        "summoner_TotalTaken": round(avg_totaltaken, 1),
        "summoner_TrueDmg": round(avg_truedmg, 1),
        "summoner_TrueTaken": round(avg_truetaken, 1),
        "summoner_Q": round(avg_q, 1),
        "summoner_W": round(avg_w, 1),
        "summoner_E": round(avg_e, 1),
        "summoner_R": round(avg_r, 1),
        "summoner_Spell1": round(avg_spell1, 1),
        "summoner_Spell1Casts": round(avg_spell1casts, 1),
        "summoner_Spell2": round(avg_spell2, 1),
        "summoner_Spell2Casts": round(avg_spell2casts, 1),
        "summoner_Team": round(avg_team, 1),
        "summoner_CCing": round(avg_ccing, 1),
        "summoner_VisionScore": round(avg_visionscore, 1),
        "summoner_WardsKilled": round(avg_wardskilled, 1),
        "summoner_TotalHealing": round(avg_totalhealing, 1),
        "summoner_HealTeam": round(avg_healteam, 1),
        "summoner_Shield": round(avg_shield, 1),
        "summoner_Minions": round(avg_minions, 1)
    }

        exists = connection.execute(text(check_sql), {
            "puuid": puuid,
            "champion": champion
        }).fetchall()

        try:
            if exists:
                # Record exists, so update it
                connection.execute(text(update_sql), {
                    "puuid": puuid,
                    "champion": champion,
                    "champ_data": json.dumps(summoner_data)
                })
                connection.commit()
                print("Data updated successfully.")
            else:
                connection.execute(text(insert_sql), {
                    "puuid": puuid,
                    "champion": champion,
                    "champ_data": json.dumps(summoner_data)
                })
                connection.commit()
                print("Data updated successfully.")
        except Exception as e:
            print("Failed to insert or update data:", e)
        return summoner_data
    
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