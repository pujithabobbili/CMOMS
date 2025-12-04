import mysql.connector
import toml
import os
from typing import Optional

def get_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Reads configuration from config.toml.
    Returns None if connection fails.
    """
    try:
        # Load config
        config_path = "config.toml"
        if not os.path.exists(config_path):
             # Fallback to example if main config doesn't exist (for development convenience)
             # In production, we'd strictly require config.toml
             if os.path.exists("config.example.toml"):
                 config_path = "config.example.toml"
             else:
                 print("Error: config.toml not found.")
                 return None

        with open(config_path, "r") as f:
            config = toml.load(f)
        
        db_config = config["database"]
        
        conn = mysql.connector.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

