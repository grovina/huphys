from model.blood import Blood
from model.organ import Organ


class Stomach(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.water_content = 0  # mL of water in stomach
        self.carbohydrate_content = 0  # g of carbohydrates in stomach
        self.protein_content = 0  # g of proteins in stomach
        self.fat_content = 0  # g of fats in stomach
        self.fiber_content = 0  # g of fibers in stomach
        self.intestines = None  # Will be set by the HumanBody class

    @property
    def food_content(self):
        return self.carbohydrate_content + self.protein_content + self.fat_content + self.fiber_content

    def _organ_specific_processing(self, dt: float) -> None:
        self._regulate_motility(dt)
        self._process_food(dt)
        self._process_water(dt)
        self._produce_gastrin(dt)
        self._produce_ghrelin(dt)
        self._secrete_hydrochloric_acid(dt)
        self._secrete_pepsin(dt)
        self._secrete_intrinsic_factor(dt)
        self._absorb_substances(dt)

    def _secrete_hydrochloric_acid(self, dt: float):
        # Placeholder for hydrochloric acid secretion
        pass

    def _secrete_pepsin(self, dt: float):
        # Placeholder for pepsin secretion
        pass

    def _secrete_intrinsic_factor(self, dt: float):
        # Placeholder for intrinsic factor secretion
        pass

    def _regulate_motility(self, dt: float):
        self.energy_demand = 3 + (self.food_content / 1000)  # Increase energy demand based on food content

    def _absorb_substances(self, dt: float):
        # Direct water absorption
        water_absorption_rate = 2  # mL/min
        absorbed_water = min(self.water_content, water_absorption_rate * dt / 60)
        self.water_content -= absorbed_water
        self.blood.volume += absorbed_water

        # Placeholder for absorption of other substances (e.g., alcohol)
        pass

    def _process_food(self, dt: float) -> None:
        if self.food_content > 0:
            digestion_fraction = 0.03 * dt / 60  # 5% per minute
            digested_carbs = self.carbohydrate_content * digestion_fraction
            digested_proteins = self.protein_content * digestion_fraction
            digested_fats = self.fat_content * digestion_fraction
            digested_fiber = self.fiber_content * digestion_fraction

            self.carbohydrate_content -= digested_carbs
            self.protein_content -= digested_proteins
            self.fat_content -= digested_fats
            self.fiber_content -= digested_fiber

            if self.intestines:
                self.intestines.receive_nutrients(digested_carbs, digested_proteins, digested_fats, digested_fiber)

    def _process_water(self, dt: float) -> None:
        if self.water_content > 0:
            water_passed = min(self.water_content, 8 * dt)  # Pass up to 8 mL/s to intestines
            self.water_content -= water_passed
            if self.intestines:
                self.intestines.receive_water(water_passed)

    def _produce_gastrin(self, dt: float):
        if self.food_content > 0:
            self.blood.gastrin_amount += 0.1 * dt  # Increase gastrin production

    def _produce_ghrelin(self, dt: float):
        if self.food_content == 0:
            self.blood.ghrelin_amount += 0.1 * dt  # Increase ghrelin production
        else:
            self.blood.ghrelin_amount = max(0, self.blood.ghrelin_amount - 0.1 * dt)  # Decrease ghrelin production

    def receive_water(self, amount: float):
        self.water_content += amount

    def receive_food(self, carbs: float = 0, proteins: float = 0, fats: float = 0, fibers: float = 0):
        self.carbohydrate_content += carbs
        self.protein_content += proteins
        self.fat_content += fats
        self.fiber_content += fibers

    def set_intestines(self, intestines):
        self.intestines = intestines

    def _organ_specific_metrics(self) -> dict:
        return {
            "food_content": {"value": self.food_content, "unit": "g", "normal_range": (0, 1000)},
            "water_content": {"value": self.water_content, "unit": "mL", "normal_range": (0, 1000)},
        }
