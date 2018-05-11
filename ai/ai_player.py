from asteroids.player import Player

class AI_Player(Player):
    """
    Defines the player ship, controlled by an AI.
    """

    def __init__(self, x, y, ai_brain):
       super(AI_Player, self).__init__(x, y)
       self._brain = ai_brain

    def sense(self, asteroids, bullets):
        """
        Checks the state of the world, and returns a feature
        matrix to be used as input to the AI update function.
        """
        return self._brain.sense(self, asteroids, bullets)

    def update(self, sensor_data):
        """
        Runs the AI algorithm on sensor_data and
        performs the appropiate actions in response.
        """
        return self._brain.update(self, sensor_data)
