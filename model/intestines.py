from model.blood import Blood
from model.organ import Organ


class Intestines(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=4,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.absorption_rate = 0.05  # fraction of nutrients absorbed per minute
        self.carbohydrate_content = 0  # g
        self.protein_content = 0  # g
        self.fat_content = 0  # g
        self.fiber_content = 0  # g
        self.water_content = 0  # mL
        self.water_absorption_rate = 5  # mL/min
        self.bile_content = 0  # mL

    def _organ_specific_processing(self, dt: float) -> None:
        self._absorb_nutrients(dt)
        self._produce_cholecystokinin(dt)
        self._produce_secretin(dt)
        self._secrete_digestive_enzymes(dt)
        self._regulate_ph(dt)
        self._absorb_vitamins_and_minerals(dt)
        self._produce_hormones(dt)

    def _secrete_digestive_enzymes(self, dt: float) -> None:
        # Placeholder for secreting digestive enzymes
        pass

    def _regulate_ph(self, dt: float) -> None:
        # Placeholder for regulating pH in the intestines
        pass

    def _absorb_vitamins_and_minerals(self, dt: float) -> None:
        # Placeholder for absorbing vitamins and minerals
        pass

    def _produce_hormones(self, dt: float) -> None:
        # Placeholder for producing various hormones
        pass

    def _absorb_nutrients(self, dt: float) -> None:
        if self.carbohydrate_content > 0:
            absorbed_carbohydrates = min(
                self.carbohydrate_content,
                self.absorption_rate * self.carbohydrate_content * dt
            )
            self.carbohydrate_content -= absorbed_carbohydrates
            self.blood.glucose_amount += absorbed_carbohydrates * 1000

        if self.protein_content > 0:
            absorbed_proteins = min(
                self.protein_content,
                self.absorption_rate * self.protein_content * dt
            )
            self.protein_content -= absorbed_proteins
            self.blood.amino_acid_amount += absorbed_proteins * 1000

        if self.fat_content > 0:
            absorbed_fats = min(
                self.fat_content,
                self.absorption_rate * self.fat_content * dt
            )
            self.fat_content -= absorbed_fats
            self.blood.fatty_acid_amount += absorbed_fats * 1000

        if self.water_content > 0:
            absorbed_water = min(self.water_content, self.water_absorption_rate * dt)
            self.water_content -= absorbed_water
            self.blood.volume += absorbed_water

    def _produce_cholecystokinin(self, dt: float):
        if self.fat_content > 0:
            self.blood.cholecystokinin_amount += 0.1 * dt  # Increase cholecystokinin production

    def _produce_secretin(self, dt: float):
        if self.protein_content > 0:
            self.blood.secretin_amount += 0.1 * dt  # Increase secretin production

    def receive_nutrients(self, carbohydrates: float, proteins: float, fats: float, fibers: float):
        self.carbohydrate_content += carbohydrates
        self.protein_content += proteins
        self.fat_content += fats
        self.fiber_content += fibers

    def receive_water(self, amount: float):
        self.water_content += amount

    def receive_bile(self, amount: float):
        self.bile_content += amount

    def _organ_specific_metrics(self) -> dict:
        return {
            "absorption_rate": {"value": self.absorption_rate, "unit": "", "normal_range": (0.03, 0.3)},
            "carbohydrate_content": {"value": self.carbohydrate_content, "unit": "g", "normal_range": (0, 1000)},
            "protein_content": {"value": self.protein_content, "unit": "g", "normal_range": (0, 1000)},
            "fat_content": {"value": self.fat_content, "unit": "g", "normal_range": (0, 1000)},
            "fiber_content": {"value": self.fiber_content, "unit": "g", "normal_range": (0, 1000)},
            "water_content": {"value": self.water_content, "unit": "mL", "normal_range": (0, 1000)},
            "bile_content": {"value": self.bile_content, "unit": "mL", "normal_range": (0, 50)}
        }

