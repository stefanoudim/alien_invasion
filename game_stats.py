from utils import get_high_score_path

class GameStats:


    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self._load_high_score()

        
    def reset_stats(self):
        self.spaceships_left = self.settings.spaceships_limit
        self.score = 0
        self.level = 1
    

    def _load_high_score(self):
        try:
            with open(get_high_score_path()) as f:
                self.high_score = int(f.read())
        except FileNotFoundError:
                print("[WARNING]: High score file not found.")

    def save_high_score(self):
        with open(get_high_score_path(), 'w') as f:
            f.write(str(self.high_score))
        
