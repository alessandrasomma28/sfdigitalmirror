from mesa import Agent
import random

class Passenger(Agent):
    """
    Passenger represents a passenger requesting a ride.

    Attributes:
        origin_taz (int): TAZ from where the passenger starts.
        destination_taz (int): TAZ where the passenger wants to go.
        request_time (int): Simulation time when request was made.
        wait_time (int): Total time waited until matched.
        matched (bool): Whether the passenger has been matched to a driver.
        driver_id (int): ID of the matched driver.
    """

    def __init__(self, unique_id, model, origin_taz, request_time):
        super().__init__(unique_id, model)
        self.origin_taz = origin_taz
        self.destination_taz = self._sample_destination()
        self.request_time = request_time
        self.wait_time = 0
        self.matched = False
        self.driver_id = None

        self.origin_edge = None
        self.destination_edge = None

    def _sample_destination(self):
        """
        Randomly select a destination TAZ different from the origin.

        Returns:
            int: Destination TAZ.
        """
        possible = [t for t in self.model.taz_list if t != self.origin_taz]
        return random.choice(possible)

    def step(self):
        """
        Called at each simulation step. If not matched, register with the
        ride-sharing service and increment waiting time.
        """
        if not self.matched:
            self.wait_time += 1
            self.model.ride_service.register_request(self)

    def match_with_driver(self, driver_id):
        """
        Mark the passenger as matched with a driver.

        Args:
            driver_id (int): ID of the matched driver.
        """
        self.driver_id = driver_id
        self.matched = True