from model.blood import Blood
from model.organ import Organ


class Muscles(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=16,  # kcal/hour
            insulin_sensitivity=1.5,  # dimensionless
        )
        self.glucose_uptake_rate = 2  # mg/min at rest
        self.glycogen_storage = 500  # g
        self.base_energy_demand = 16  # kcal/hour

    def _organ_specific_processing(self, dt: float) -> None:
        self.generate_heat(dt)
        self.metabolize_glucose(dt)
        self.metabolize_fatty_acids(dt)
        self.store_glycogen(dt)
        self.break_down_glycogen(dt)
        self.synthesize_proteins(dt)
        self.break_down_proteins(dt)
        self.regulate_blood_flow(dt)

    def generate_heat(self, dt: float):
        # Placeholder for heat generation
        pass

    def metabolize_glucose(self, dt: float):
        # Placeholder for glucose metabolism
        pass

    def metabolize_fatty_acids(self, dt: float):
        # Placeholder for fatty acid metabolism
        pass

    def store_glycogen(self, dt: float):
        # Placeholder for glycogen storage
        pass

    def break_down_glycogen(self, dt: float):
        # Placeholder for glycogen breakdown
        pass

    def synthesize_proteins(self, dt: float):
        # Placeholder for protein synthesis
        pass

    def break_down_proteins(self, dt: float):
        # Placeholder for protein breakdown
        pass

    def regulate_blood_flow(self, dt: float):
        # Placeholder for blood flow regulation
        pass

    def increase_energy_demand(self, factor: float):
        self.energy_demand = self.base_energy_demand * factor
        self.glucose_uptake_rate = 2 + 18 * (factor - 1)  # Up to 20 mg/min during intense exercise

    def reset_energy_demand(self):
        self.energy_demand = self.base_energy_demand
        self.glucose_uptake_rate = 2  # mg/min at rest

    def _organ_specific_metrics(self) -> dict:
        return {
            "glucose_uptake_rate": {"value": self.glucose_uptake_rate, "unit": "mg/min", "normal_range": (2, 20)},
            "glycogen_storage": {"value": self.glycogen_storage, "unit": "g", "normal_range": (200, 800)},
            "energy_demand": {"value": self.energy_demand, "unit": "kcal/hour", "normal_range": (10, 100)}
        }
