class AI_Brain(object):
    """
    Base class for the AI Player controllers.
    """

    def sense(self, player, asteroids, bullets):
        """
        Checks the state of the world, and returns a feature
        matrix to be used as input to the AI update function.
        """
        raise NotImplementedError("'sense' should be implemented by "
                "AI_Brain subclasses")

    def update(self, player, sensor_data):
        """
        Runs the AI algorithm on sensor_data and
        performs the appropiate actions in response.
        """
        raise NotImplementedError("'update' should be implemented by "
                "AI_Brain subclasses")
