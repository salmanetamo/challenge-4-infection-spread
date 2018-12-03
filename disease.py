# This class defines our disease and describes the behaviours of each disease
class Disease:
    def __init__(self, name, infection_rate, recovery_rate, lethality_rate):
        self.name = name  # Name of the disease simulated
        self.infection_rate = infection_rate  # Chance that the disease transmits if two people are in contact
        self.recovery_rate = recovery_rate  # Chance that someone recovers each day
        self.lethality_rate = lethality_rate  # Chance that someone dies on a given day
