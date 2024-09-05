from model.blood import Blood
from model.intestines import Intestines
from model.organ import Organ


class Liver(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=18,  # kcal/hour
            insulin_sensitivity=0.8  # dimensionless
        )
        self.glucose_storage = 100  # Glycogen storage in g
        self.gall_bladder = None

    def set_gall_bladder(self, gall_bladder):
        self.gall_bladder = gall_bladder

    def _organ_specific_processing(self, dt: float) -> None:
        self._regulate_glucose(dt)
        self._regulate_blood_ph(dt)
        self._regulate_bile_production(dt)
        self._synthesize_proteins(dt)
        self._detoxify_substances(dt)
        self._store_vitamins_and_minerals(dt)
        self._produce_cholesterol(dt)
        self._metabolize_drugs(dt)
        self._regulate_blood_clotting(dt)
        self._produce_immune_factors(dt)
        self._regulate_hormone_levels(dt)

    def _synthesize_proteins(self, dt: float):
        # Placeholder for protein synthesis function
        pass

    def _detoxify_substances(self, dt: float):
        # Placeholder for detoxification function
        pass

    def _store_vitamins_and_minerals(self, dt: float):
        # Placeholder for vitamin and mineral storage function
        pass

    def _produce_cholesterol(self, dt: float):
        # Placeholder for cholesterol production function
        pass

    def _metabolize_drugs(self, dt: float):
        # Placeholder for drug metabolism function
        pass

    def _regulate_blood_clotting(self, dt: float):
        # Placeholder for blood clotting regulation function
        pass

    def _produce_immune_factors(self, dt: float):
        # Placeholder for immune factor production function
        pass

    def _regulate_hormone_levels(self, dt: float):
        # Placeholder for hormone level regulation function
        pass

    def _regulate_glucose(self, dt: float):
        insulin_effect = self.blood.insulin_concentration * self.insulin_sensitivity
        glucagon_effect = self.blood.glucagon_concentration * self.glucagon_sensitivity

        # Glycogen storage (glycogenesis)
        if self.blood.glucose_concentration > 100:
            glucose_stored = min(self.blood.glucose_amount * 0.1, 10 * insulin_effect * dt)
            self.blood.glucose_amount -= glucose_stored
            self.glucose_storage += glucose_stored / 1000  # Convert mg to g

        # Glycogen breakdown (glycogenolysis)
        elif self.blood.glucose_concentration < 70 and self.glucose_storage > 0:
            glucose_released = min(70 - self.blood.glucose_concentration, self.glucose_storage * 1000, 10 * glucagon_effect * dt)
            self.blood.glucose_amount += glucose_released
            self.glucose_storage -= glucose_released / 1000  # Convert mg to g

        # Gluconeogenesis
        if self.blood.glucose_concentration < 60:
            glucose_produced = 5 * dt / 60 * glucagon_effect  # Adjusted for glucagon effect
            self.blood.glucose_amount += glucose_produced

        # Glucose export to blood
        if self.blood.glucose_concentration < 90:
            glucose_exported = min(self.glucose_storage * 1000 * 0.01, (90 - self.blood.glucose_concentration) * 10) * dt / 60
            self.blood.glucose_amount += glucose_exported
            self.glucose_storage -= glucose_exported / 1000

    def _regulate_blood_ph(self, dt: float):
        # Simulate ammonia production
        ammonia_production = 0.1 * dt
        
        # Convert ammonia to urea (which is less acidic)
        urea_production = ammonia_production * 0.8
        
        # Adjust blood pH based on urea production
        ph_change = urea_production * 0.01
        self.blood.ph += ph_change

    def _regulate_bile_production(self, dt: float):
        if self.blood.secretin_concentration > 1.0:
            bile_production = 0.1 * dt  # Increase bile production
            if self.gall_bladder:
                self.gall_bladder.store_bile(bile_production)

    def _organ_specific_metrics(self) -> dict:
        return {
            "glucose_storage": {"value": self.glucose_storage, "unit": "g", "normal_range": (50, 200)},
        }

class GallBladder(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=0,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.bile_storage = 0  # mL of bile
        self.intestines = None

    def _organ_specific_processing(self, dt: float) -> None:
        self._release_bile(dt)

    def store_bile(self, amount: float):
        self.bile_storage += amount

    def _release_bile(self, dt: float) -> None:
        bile_released = min(self.bile_storage, 0.1 * dt)  # Release up to 0.1 mL/s
        if self.intestines:
            self.bile_storage -= bile_released
            self.intestines.receive_bile(bile_released)
    
    def set_intestines(self, intestines: Intestines) -> None:
        self.intestines = intestines

    def _organ_specific_metrics(self) -> dict:
        return {
            "bile_storage": {"value": self.bile_storage, "unit": "mL", "normal_range": (0, 50)}
        }
