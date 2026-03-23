import math

# ============================================================
# DEBUG MODE
# ============================================================
DEBUG = False

def debug_print(message):
    """
    Centralized debug printing.
    Only prints messages if DEBUG mode is enabled.
    """
    if DEBUG:
        print(f"[DEBUG] {message}")

# ============================================================
# DISTANCE CALCULATION
# ============================================================
def get_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two latitude/longitude points
    on the Earth using the Haversine formula.
    Returns distance in kilometers (float)
    """
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c
