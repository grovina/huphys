from model.blood import Blood
from model.organ import Organ


class Fat(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=10,  # kcal/hour
            insulin_sensitivity=2.0,  # dimensionless
            glucagon_sensitivity=1.0  # dimensionless
        )
        self.fat_reserve = 10000  # g of fat (initial reserve)
        self.lipolysis_rate = 0.1  # g of fat/min

    def _organ_specific_processing(self, dt: float) -> None:
        self._store_fat(dt)
        self._store_vitamins()
        self._release_fat(dt)
        self._produce_hormones(dt)

    def _produce_hormones(self, dt: float):
        # Placeholder for hormone production (e.g., leptin)
        pass

    def _store_vitamins(self):
        # Placeholder for fat-soluble vitamin storage
        pass

    def _store_fat(self, dt: float):
        if self.blood.glucose_concentration > 120 and self.blood.insulin_concentration > 1.0:
            glucose_stored = min(self.blood.glucose_amount * 0.1, 10 * dt * self.insulin_sensitivity)
            fat_stored = glucose_stored * 0.11 / 1000  # 1g of fat is about 9 kcal, and 1g of glucose is about 4 kcal
            self.blood.glucose_amount -= glucose_stored
            self.fat_reserve += fat_stored
            self.blood.triglyceride_amount += fat_stored * 1000  # Convert g to mg

    def _release_fat(self, dt: float):
        if self.blood.glucose_concentration < 80 or self.blood.glucagon_concentration > 1.0:
            lipolysis_factor = max(1, (80 - self.blood.glucose_concentration) / 10)
            fat_released = min(self.lipolysis_rate * lipolysis_factor * dt / 60, self.fat_reserve)
            self.fat_reserve -= fat_released
            self.blood.triglyceride_amount += fat_released * 1000  # Convert g to mg

    def _organ_specific_metrics(self) -> dict:
        return {
            "fat_reserve": {"value": self.fat_reserve, "unit": "g", "normal_range": (5000, 20000)},
            "insulin_sensitivity": {"value": self.insulin_sensitivity, "unit": "", "normal_range": (1.0, 3.0)},
            "glucagon_sensitivity": {"value": self.glucagon_sensitivity, "unit": "", "normal_range": (0.5, 1.5)},
            "lipolysis_rate": {"value": self.lipolysis_rate, "unit": "g/min", "normal_range": (0.05, 0.2)},
        }

