from sqlalchemy import create_engine, text
import pytz
import datetime
from datetime import datetime
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