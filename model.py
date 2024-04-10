import mesa
import math


class SchellingAgent(mesa.Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, unique_id, model, agent_type, city_centers):
        """
        Create a new Schelling agent.

        Args:
           unique_id: An agent's unique identifier.
           x, y: An agent's initial location.
           agent_type: An agent's type (minority=1, majority=0)
           city_centers: the position of a city centers
        """
        super().__init__(unique_id, model)
        self.type = agent_type
        self.city_centers = city_centers

    def step(self):
        # Two city centers are initiated at the bottom-left corner and
        # the top-right corner to maximize distance.
        # Find the manhattan distance to the nearest city center 
        distance_to_center = min(
            abs(self.pos[0] - self.city_centers[0][0]) + abs(self.pos[1] - self.city_centers[0][1]),
            abs(self.pos[0] - self.city_centers[1][0]) + abs(self.pos[1] - self.city_centers[1][1])
        )
        
        similar = 0
        unsimilar = 0

        for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, radius=self.model.radius):
            # Find the number of similar and unsimilar neighbors
            if neighbor.type == self.type:
                similar += 1
            else:
                unsimilar += 1

        # If the distance to the nearest city center is longer than the required distance
        if distance_to_center > self.model.distance:
            # If the number of similar neighbors is at least 1.5 times of the number of unsimilar neighbors
            if unsimilar == 0 or similar / unsimilar >= self.model.homophily:
                # Happy
                self.model.happy += 1
            else:
                # Unhappy
                self.model.grid.move_to_empty(self)
        # If the distance to the nearest city center is shorter than the required distance
        else:
            # If the number of similar neighbors is at least the same as the number of unsimilar neighbors
            if unsimilar == 0 or similar / unsimilar >= 1:
                # Happy
                self.model.happy += 1
            else:
                # Unhappy
                self.model.grid.move_to_empty(self)


class Schelling(mesa.Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(
        self,
        height=20,
        width=20,
        homophily=1.5,
        radius=1,
        density=0.8,
        minority_pc=0.2,
        distance=2,
        city_distance=None
        seed=None,
    ):
        """
        Create a new Schelling model.

        Args:
            width, height: Size of the space.
            density: Initial Chance for a cell to populated
            minority_pc: Chances for an agent to be in minority class
            homophily: minimum ratio of number of similar agents to number of unsimilar agents
            radius: Search radius for checking similarity
            distance: required distance to a city center
            seed: Seed for Reproducibility
        """

        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.distance = distance
        self.radius = radius

        # Calculate city center positions based on city_distance
        if city_distance is None:
            city_distance = math.sqrt(height**2 + width**2) / 2  # Default to half the diagonal
        offset = city_distance / math.sqrt(2)
        self.city_centers = [
            (max(0, min(self.width - 1, int(self.width / 2 - offset))), max(0, min(self.height - 1, int(self.height / 2 - offset)))),
            (max(0, min(self.width - 1, int(self.width / 2 + offset))), max(0, min(self.height - 1, int(self.height / 2 + offset))))
        ]

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        self.happy = 0
        self.datacollector = mesa.DataCollector(model_reporters={"happy": "happy"})

        # Set up agents
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < self.minority_pc else 0
                agent = SchellingAgent(self.next_id(), self, agent_type, self.city_centers)
                self.grid.place_agent(agent, pos)
                self.schedule.add(agent)

        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()

        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
