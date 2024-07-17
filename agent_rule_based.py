class RuleBasedAgent:
    def __init__(self):
        pass

    def get_action(self, dino, obstacle):
        if obstacle.rect.x - dino.dino_rect.x < 150:
            return "jump"
        return "run"
