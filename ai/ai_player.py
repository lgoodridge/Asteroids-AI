from asteroids.player import Player

class AI_Player(Player):
    """
    Defines the player ship, controlled by an AI.
    """

    # Size of the decision vector
    DECISION_VECTOR_SIZE = 4

    def __init__(self, x, y, ai_brain):
       super(AI_Player, self).__init__(x, y)
       self._brain = ai_brain

    def sense(self, asteroids, bullets):
        """
        Checks the state of the world, and returns a feature
        matrix to be used as input to the AI update function.
        """
        return self._brain.sense(self, asteroids, bullets)

    def update(self, bullets, sensor_data):
        """
        Updates any time dependent player state, then runs
        the AI algorithm on sensor_data, and performs the
        appropiate actions in response.
        """
        super(AI_Player, self).update(bullets, sensor_data)
        decision_vector = self._brain.think(self, bullets, sensor_data)
        self._perform_decisions(decision_vector, bullets)

    def _perform_decisions(self, decision_vector, bullets):
        """
        Accepts a boolean vector containing the following decisions:
          0: Whether to shoot
          1: Whether to boost
          2: Whether to spin clockwise
          3: Whether to spin counter-clockwise

        The player ship then carries out these decisions for this timestep.
        """
        if len(decision_vector) != AI_Player.DECISION_VECTOR_SIZE:
            raise RuntimeError(("Programmer Error: decision vector has "
                    "length '%d' instead of expected length '%d'." %
                    (len(decision_vector), AI_Player.DECISION_VECTOR_SIZE)))

        if decision_vector[0]:
            self.shoot(bullets)

        if decision_vector[1]:
            self.start_boosting()
        else:
            self.stop_boosting()

        # Spin in the decided upon direction, or stop spinning entirely
        # Note: if both spin decisions are True, arbitrarily spin clockwise
        if decision_vector[2]:
            self.start_spinning(True)
        elif decision_vector[3]:
            self.start_spinning(False)
        else:
            self.stop_spinning()
