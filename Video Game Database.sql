/*video_games_tb = "CREATE TABLE video_games(
				id INTEGER NOT NULL PRIMARY KEY,
				name TEXT NOT NULL,
				genre TEXT NOT NULL,
				game_developer TEXT NOT NULL,
				release_date TEXT NOT NULL);"

game_developers_tb = "CREATE TABLE game_developers(
				id INTEGER NOT NULL PRIMARY KEY,
				name TEXT NOT NULL,
				address TEXT,
				state TEXT,
				city TEXT NOT NULL,
				country TEXT NOT NULL);"

platforms_tb = "CREATE TABLE platforms(
				id INTEGER NOT NULL PRIMARY KEY,
                company_id INTEGER NOT NULL,
				name TEXT NOT NULL,
				company TEXT,
				release_date TEXT NOT NULL,
				original_price REAL NOT NULL);"

platforms_games_tb = "CREATE TABLE platforms_games(
				game_id INTEGER NOT NULL,
				platform_id INTEGER NOT NULL,
				platform_name TEXT NOT NULL,
				FOREIGN KEY(game_id) REFERENCES video_games(id),
				FOREIGN KEY(platform_id) REFERENCES platforms(id),
                PRIMARY KEY(game_id, platform_id));"

characters_tb = "CREATE TABLE characters(
				id INTEGER NOT NULL PRIMARY KEY,
				name TEXT NOT NULL,
				birthday TEXT NOT NULL,
				gender NUMERIC NOT NULL,
				info TEXT NOT NULL);"

games_characters_tb = "CREATE TABLE games_characters(
				character_id INTEGER NOT NULL,
				character_name TEXT NOT NULL,
				game_id INTEGER NOT NULL,
				FOREIGN KEY(character_id) REFERENCES characters(id),
				FOREIGN KEY(game_id) REFERENCES video_games(id),
                PRIMARY KEY(character_id, game_id));"

---- here ends stage 1*/

/*delete_rows = "DELETE FROM games_characters WHERE character_id IS NULL AND game_id IS NOT NULL"
alter_table_platforms = "UPDATE platforms
                            SET release_date = DATE(release_date);"
alter_table_characters = "UPDATE characters
                            SET birthday = DATE(birthday);"

---- here ends stage2*/

search_nathan = "SELECT * 
                 FROM characters 
                 WHERE id = (SELECT character_id 
                             FROM games_characters 
                             WHERE character_name = 'Nathan Drake')"

/*how_many_people = "SELECT COUNT(info) FROM characters WHERE info LIKE '%Nathan Drake%'"
find_location = "SELECT address,
                        state,
                        city,
                        country 
                 FROM game_developers 
                 WHERE name = (SELECT game_developer
                               FROM video_games
                               WHERE id = (SELECT game_id
                                           FROM games_characters
                                           WHERE character_name = 'Nathan Drake'));" 
---- here ends stage3*/

count_games_ca = "SELECT COUNT(name) 
                  FROM video_games 
                  WHERE game_developer IN (SELECT name 
                                           FROM game_developers 
                                           WHERE state = 'California');"
address =  "SELECT address, city, state, country 
            FROM game_developers 
            WHERE name = (SELECT game_developer
            			  FROM video_games 
            			  WHERE game_developer IN 
                    							  (SELECT name 
            									   FROM game_developers 
            									   WHERE state = 
            													 (SELECT state 
            													  FROM game_developers 
            													  GROUP BY state 
                												  ORDER by count(state) DESC
            													  LIMIT 1)) 
            ORDER BY release_date DESC 
            LIMIT 1);"