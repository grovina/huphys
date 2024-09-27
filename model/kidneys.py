from model.blood import Blood
from model.organ import Organ


class Kidneys(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=6,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.glomerular_filtration_rate = 115  # mL/min
        self.tubular_reabsorption_rate = 114  # mL/min
        self.urine_production_rate = 1  # mL/min
        self.sodium_reabsorption_rate = 0.995  # dimensionless
        self.potassium_secretion_rate = 0.1  # mmol/min
        self.phosphate_reabsorption_rate = 0.85  # dimensionless
        self.calcium_reabsorption_rate = 0.98  # dimensionless
        self.vitamin_d_activation_rate = 0.1  # ng/mL/hour
        self.erythropoietin_production_rate = 0.1  # mIU/mL/hour
        self.renin_production_rate = 0.1  # ng/mL/h/hour
        self.bladder = None

    def set_bladder(self, bladder):
        self.bladder = bladder

    def receive_brain_signal(self, signal: float):
        # Adjust glomerular filtration rate based on brain signal
        self.glomerular_filtration_rate = 115 * (1 + signal * 0.02)
        
        # Adjust tubular reabsorption rate inversely
        self.tubular_reabsorption_rate = 114 * (1 - signal * 0.02)
        
        # Ensure rates stay within physiological limits
        self.glomerular_filtration_rate = max(60, min(180, self.glomerular_filtration_rate))
        self.tubular_reabsorption_rate = max(59, min(179, self.tubular_reabsorption_rate))

    def _organ_specific_processing(self, dt: float) -> None:
        self._filter_blood(dt)
        self._regulate_acid_base_balance(dt)
        self._produce_hormones(dt)
        self._activate_vitamin_d(dt)
        self._produce_prostaglandins(dt)

    def _filter_blood(self, dt: float):
        filtered_volume = self.glomerular_filtration_rate * dt / 60  # mL
        reabsorbed_volume = self.tubular_reabsorption_rate * dt / 60  # mL
        urine_volume = max(filtered_volume - reabsorbed_volume, 0) # mL

        # Update blood volume
        self.blood.volume -= urine_volume
        self.blood.urea_amount -= urine_volume / 10 * self.blood.urea_concentration # mg
        self.blood.creatinine_amount -= urine_volume / 10 * self.blood.creatinine_concentration # mg

        # Update urine production
        self.urine_production_rate = urine_volume / (dt / 60)
        if self.bladder:
            self.bladder.receive_urine(urine_volume)

        # Electrolytes regulation
        self.blood.sodium_amount -= urine_volume / 1000 * self.blood.sodium_concentration * (1 - self.sodium_reabsorption_rate)

        # Potassium regulation
        self.blood.potassium_amount += self.potassium_secretion_rate * dt / 60

        # Calcium and Phosphate regulation
        self.blood.calcium_amount -= urine_volume / 1000 * self.blood.calcium_concentration * (1 - self.calcium_reabsorption_rate)
        self.blood.phosphate_amount -= urine_volume / 10 * self.blood.phosphate_concentration * (1 - self.phosphate_reabsorption_rate)

    def _regulate_acid_base_balance(self, dt: float):
        # Simplified acid-base regulation
        if self.blood.ph < 7.35:
            self.blood.bicarbonate_amount += 0.1 * dt / 60
        elif self.blood.ph > 7.45:
            self.blood.bicarbonate_amount -= 0.1 * dt / 60

    def _produce_hormones(self, dt: float):
        # Erythropoietin production
        if self.blood.oxygen_saturation < 0.9:
            self.blood.erythropoietin_amount += self.erythropoietin_production_rate * dt / 60

        # Renin production
        if self.blood.mean_arterial_pressure < 80:
            self.blood.renin_amount += self.renin_production_rate * dt / 60

    def _produce_prostaglandins(self, dt: float) -> None:
        # Placeholder for producing prostaglandins
        pass

    def _activate_vitamin_d(self, dt: float):
        # Calculate the amount of inactive vitamin D available for activation
        inactive_vitamin_d = self.blood.inactive_vitamin_d_amount

        # Calculate the amount that can be activated based on various factors
        calcium_factor = min(1.0, max(0.1, self.blood.calcium_concentration / 10))
        phosphate_factor = min(1.0, max(0.1, self.blood.phosphate_amount / 4))
        parathyroid_hormone_factor = 1.0  # Placeholder for parathyroid hormone effect

        activation_factor = calcium_factor * phosphate_factor * parathyroid_hormone_factor
        max_activation = self.vitamin_d_activation_rate * dt / 60 * activation_factor

        # Activate vitamin D, but don't exceed available inactive vitamin D
        activated_amount = min(inactive_vitamin_d, max_activation)

        # Update blood vitamin D levels
        self.blood.inactive_vitamin_d_amount -= activated_amount
        self.blood.active_vitamin_d_amount += activated_amount

        # Simulate excretion and degradation of vitamin D
        inactive_excretion = self.blood.inactive_vitamin_d_amount * 0.001 * dt / 60
        active_degradation = self.blood.active_vitamin_d_amount * 0.002 * dt / 60

        self.blood.inactive_vitamin_d_amount -= inactive_excretion
        self.blood.active_vitamin_d_amount -= active_degradation

    def _organ_specific_metrics(self) -> dict:
        return {
            "glomerular_filtration_rate": {"value": self.glomerular_filtration_rate, "unit": "mL/min", "normal_range": (90, 130)},
            "tubular_reabsorption_rate": {"value": self.tubular_reabsorption_rate, "unit": "mL/min", "normal_range": (90, 130)},
            "urine_production_rate": {"value": self.urine_production_rate, "unit": "mL/min", "normal_range": (0.5, 2)},
            "potassium_secretion_rate": {"value": self.potassium_secretion_rate, "unit": "mmol/min", "normal_range": (0.05, 0.15)},
            "vitamin_d_activation_rate": {"value": self.vitamin_d_activation_rate, "unit": "ng/mL/hour", "normal_range": (0.05, 0.2)},
        }


class Bladder(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=1,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.urine_volume = 0  # mL
        self.max_capacity = 500  # mL

    def _organ_specific_processing(self, dt: float) -> None:
        pass

    def receive_urine(self, volume: float):
        self.urine_volume = min(self.urine_volume + volume, self.max_capacity)

    def urinate(self) -> float:
        urine_output = self.urine_volume
        self.urine_volume = 0
        return urine_output
    def _organ_specific_metrics(self) -> dict:
        return {
            "Urine Volume": {"value": self.urine_volume, "unit": "mL", "normal_range": (0, self.max_capacity)},
            "Fullness Percentage": {"value": (self.urine_volume / self.max_capacity) * 100, "unit": "%", "normal_range": (0, 100)}
        }
