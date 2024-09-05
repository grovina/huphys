from model.blood import Blood
from model.organ import Organ


class Pancreas(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=1,  # kcal/hour
            insulin_sensitivity=0.5  # dimensionless
        )
        self.insulin_production_rate = 0.5  # μU/mL/min
        self.glucagon_production_rate = 0.1  # ng/mL/min

    def _organ_specific_processing(self, dt: float) -> None:
        self._produce_insulin(dt)
        self._produce_glucagon(dt)
        self._produce_somatostatin(dt)
        self._produce_pancreatic_polypeptide(dt)
        self._produce_digestive_enzymes(dt)
        self._regulate_blood_sugar(dt)
        self._regulate_fat_metabolism(dt)
        self._regulate_protein_metabolism(dt)

    def _produce_somatostatin(self, dt: float):
        # Placeholder for somatostatin production
        pass

    def _produce_pancreatic_polypeptide(self, dt: float):
        # Placeholder for pancreatic polypeptide production
        pass

    def _produce_digestive_enzymes(self, dt: float):
        # Placeholder for digestive enzyme production
        pass

    def _regulate_blood_sugar(self, dt: float):
        # Placeholder for blood sugar regulation
        pass

    def _regulate_fat_metabolism(self, dt: float):
        # Placeholder for fat metabolism regulation
        pass

    def _regulate_protein_metabolism(self, dt: float):
        # Placeholder for protein metabolism regulation
        pass

    def _produce_insulin(self, dt: float):
        base_rate = 0.5  # μU/mL/min
        glucose_effect = max(0, (self.blood.glucose_concentration - 100) * 0.05)
        production_rate = base_rate + glucose_effect
        insulin_produced = production_rate * dt / 60
        self.blood.insulin_amount += insulin_produced

    def _produce_glucagon(self, dt: float):
        base_rate = 0.1  # ng/mL/min
        glucose_effect = max(0, (80 - self.blood.glucose_concentration) * 0.01)
        production_rate = base_rate + glucose_effect
        glucagon_produced = production_rate * dt / 60
        self.blood.glucagon_amount += glucagon_produced

    def _organ_specific_metrics(self) -> dict:
        return {
            "insulin_production_rate": {"value": self.insulin_production_rate, "unit": "μU/mL/min", "normal_range": (0.3, 0.7)},
            "glucagon_production_rate": {"value": self.glucagon_production_rate, "unit": "ng/mL/min", "normal_range": (0.05, 0.15)},
        }
