

class CHunter:
    def __init__(self, hunter:dict) -> None:
        self.image = hunter["image"]
        self.velocity_chase = hunter["velocity_chase"]
        self.velocity_return = hunter["velocity_return"]
        self.distance_start_chase = hunter["distance_start_chase"]
        self.distance_start_return = hunter["distance_start_return"]