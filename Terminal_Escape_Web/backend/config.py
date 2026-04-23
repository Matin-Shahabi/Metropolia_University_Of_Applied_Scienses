import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)
    
    # Database
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'msh701150')
    DB_NAME = os.getenv('DB_NAME', 'flight_game')
    
    # Game Constants
    START_MONEY = 17000
    START_CO2 = 6000
    MAX_FLIGHT_OPTIONS = 5
    COST_PER_KM = 0.5
    CO2_PER_KM = 0.2
    POLICE_CATCH_START = 0.0
    POLICE_CATCH_INCREMENT = 0.08
    POLICE_CATCH_MAX = 0.5
    FLIGHT_AVAILABILITY_MAX = 0.75