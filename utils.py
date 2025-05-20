import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_high_score_path():
    appdata = os.getenv("APPDATA")
    folder = os.path.join(appdata, "AlienInvasion")
    os.makedirs(folder, exist_ok=True)  
    return os.path.join(folder, "high_score.txt")