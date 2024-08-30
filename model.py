import math


class Blood:
    def __init__(
        self,
        volume: float = 5000,  # mL
    ):
        self.volume = volume
        self.glucose_amount = 4500 * (volume / 5000)  # mg
        self.fatty_acid_amount = 500 * (volume / 5000)  # mg
        self.amino_acid_amount = 200 * (volume / 5000)  # mg
        self.oxygen_amount = 950  # mL O2 (initial amount for 98% saturation)
        self.co2_amount = 100 * (volume / 5000)  # mmol
        self.epinephrine_amount = 2.5 * (volume / 5000)  # ng
        self.nitric_oxide_amount = 4 * (volume / 5000)  # ng
        self.insulin_amount = 10 * (volume / 5000)  # μU
        self.glucagon_amount = 3.5 * (volume / 5000)  # ng
        self.nutrient_amount = 0  # mg
        self.bicarbonate_amount = 120000 * (volume / 5000)  # mEq
        self.systolic_pressure = 120  # mmHg
        self.diastolic_pressure = 80  # mmHg
        self.ph = 7.4  # dimensionless
        self.hematocrit = 45  # percentage
        self.hemoglobin = 15  # g/dL
        self.fat_amount = 500 * (volume / 5000)  # mg

    @property
    def glucose_concentration(self):
        return self.glucose_amount / (self.volume / 100)  # mg/dL

    @property
    def co2_concentration(self):
        return self.co2_amount / (self.volume / 1000)  # mmol/L

    @property
    def epinephrine_concentration(self):
        return self.epinephrine_amount / (self.volume / 1000)  # ng/mL

    @property
    def nitric_oxide_concentration(self):
        return self.nitric_oxide_amount / (self.volume / 1000)  # ng/mL

    @property
    def insulin_concentration(self):
        return self.insulin_amount / (self.volume / 1000)  # μU/mL

    @property
    def glucagon_concentration(self):
        return self.glucagon_amount / (self.volume / 1000)  # ng/mL

    @property
    def nutrient_concentration(self):
        return self.nutrient_amount / (self.volume / 100)  # mg/dL

    @property
    def bicarbonate_concentration(self):
        return self.bicarbonate_amount / (self.volume / 1000)  # mEq/L

    @property
    def plasma_volume(self):
        return self.volume * (1 - self.hematocrit / 100)  # mL

    @property
    def mean_arterial_pressure(self):
        return (self.systolic_pressure + 2 * self.diastolic_pressure) / 3

    @property
    def fat_concentration(self):
        return self.fat_amount / (self.volume / 100)  # mg/dL

    @property
    def total_oxygen_capacity(self):
        return self.hemoglobin * 1.34 * (self.volume / 100)  # mL O2

    @property
    def oxygen_saturation(self):
        return self.oxygen_amount / self.total_oxygen_capacity

    def __str__(self) -> str:
        return (
            f"Glucose concentration: {self.glucose_concentration:.2f}, "
            f"Systolic pressure: {self.systolic_pressure:.2f} mmHg, "
            f"Diastolic pressure: {self.diastolic_pressure:.2f} mmHg, "
            f"CO2 concentration: {self.co2_concentration:.2f}, "
            f"Epinephrine concentration: {self.epinephrine_concentration:.2f}, "
            f"Nitric oxide concentration: {self.nitric_oxide_concentration:.2f}, "
            f"pH: {self.ph:.2f}, "
            f"Hematocrit: {self.hematocrit:.2f}%, "
            f"Plasma volume: {self.plasma_volume:.2f} mL, "
            f"Volume: {self.volume:.2f} mL, "
            f"Insulin concentration: {self.insulin_concentration:.2f}, "
            f"Glucagon concentration: {self.glucagon_concentration:.2f}, "
            f"Oxygen saturation: {self.oxygen_saturation:.2f}"
        )

    def get_metrics(self) -> dict:
        return {
            "glucose_concentration": {"value": self.glucose_concentration, "unit": "mg/dL"},
            "systolic_pressure": {"value": self.systolic_pressure, "unit": "mmHg"},
            "diastolic_pressure": {"value": self.diastolic_pressure, "unit": "mmHg"},
            "co2_concentration": {"value": self.co2_concentration, "unit": "mmol/L"},
            "epinephrine_concentration": {"value": self.epinephrine_concentration, "unit": "ng/mL"},
            "nitric_oxide_concentration": {"value": self.nitric_oxide_concentration, "unit": "ng/mL"},
            "ph": {"value": self.ph, "unit": ""},
            "hematocrit": {"value": self.hematocrit, "unit": "%"},
            "plasma_volume": {"value": self.plasma_volume, "unit": "mL"},
            "volume": {"value": self.volume, "unit": "mL"},
            "insulin_concentration": {"value": self.insulin_concentration, "unit": "μU/mL"},
            "glucagon_concentration": {"value": self.glucagon_concentration, "unit": "ng/mL"},
            "hemoglobin": {"value": self.hemoglobin, "unit": "g/dL"},
            "oxygen_amount": {"value": self.oxygen_amount, "unit": "mL O2"},
            "oxygen_saturation": {"value": self.oxygen_saturation, "unit": ""},
            "bicarbonate_concentration": {"value": self.bicarbonate_concentration, "unit": "mEq/L"},
            "fat_concentration": {"value": self.fat_concentration, "unit": "mg/dL"},
        }

    def update(self, dt: float):
        # Calculate pCO2 from CO2 concentration
        k = 0.03  # Henry's constant for CO2 in mmol/L/mmHg
        pCO2 = self.co2_concentration / k
        
        # Calculate new pH using Henderson-Hasselbalch equation
        new_ph = 6.1 + math.log10(self.bicarbonate_concentration / (0.03 * pCO2))
        
        # Simulate buffer systems
        buffer_capacity = 0.1  # Represents the overall buffer capacity of blood
        ph_change = (new_ph - self.ph) * buffer_capacity
        
        # Update pH with buffering effect
        self.ph += ph_change * dt / 60  # Adjust for dt in seconds
        
        # Adjust bicarbonate content based on pH change
        self.bicarbonate_amount += ph_change * 10 * dt / 60 * (self.volume / 1000)  # Adjust for dt in seconds
        
        # Ensure pH and bicarbonate stay within physiological limits
        self.ph = max(6.8, min(7.8, self.ph))
        self.bicarbonate_amount = max(15000, min(35000, self.bicarbonate_amount))


class Nerve:
    def __init__(self, name):
        self.name = name
        self.signal = 0

    def send_signal(self, signal):
        self.signal = signal

    def get_signal(self):
        return self.signal


class Organ:
    def __init__(
        self,
        blood: Blood,
        energy_demand: float = 0,  # kcal/hour
        oxygen_demand: float = 0,  # mL O2/min
        insulin_sensitivity: float = 1.0,  # dimensionless
        glucagon_sensitivity: float = 1.0,  # dimensionless
    ):
        self.blood = blood
        self.energy_demand = energy_demand  # kcal/hour
        self.oxygen_demand = oxygen_demand  # mL O2/min
        self.insulin_sensitivity = insulin_sensitivity  # dimensionless
        self.glucagon_sensitivity = glucagon_sensitivity  # dimensionless
        self.fat_oxidation_rate = 0.1  # fraction of energy from fat

    def _organ_specific_metrics(self) -> dict:
        return {}

    def get_metrics(self) -> dict:
        metrics = {
            "energy_demand": {"value": self.energy_demand, "unit": "kcal/hour"},
            "oxygen_demand": {"value": self.oxygen_demand, "unit": "mL O2/min"},
            "insulin_sensitivity": {"value": self.insulin_sensitivity, "unit": ""},
        }
        metrics.update(self._organ_specific_metrics())
        return metrics

    def consume_nutrients(self, dt: float) -> None:
        oxygen_available = self.blood.oxygen_amount  # mL O2
        glucose_available = self.blood.glucose_amount  # mg
        fatty_acid_available = self.blood.fatty_acid_amount  # mg
        amino_acid_available = self.blood.amino_acid_amount  # mg
        
        # Calculate energy consumption based on demand and availability
        energy_demanded = self.energy_demand * dt / 3600  # kcal, adjusted for dt in seconds
        
        # Glucose consumption (priority)
        if energy_demanded > 0:
            glucose_energy = min(energy_demanded, glucose_available * 4 / 1000)  # 4 kcal/g of glucose
            glucose_consumed = glucose_energy * 1000 / 4  # Convert kcal to mg
            energy_demanded -= glucose_energy
        else:
            glucose_consumed = 0
        
        # Fatty acid consumption (secondary)
        if energy_demanded > 0:
            fatty_acid_energy = min(energy_demanded, fatty_acid_available * 9 / 1000)  # 9 kcal/g of fat
            fatty_acid_consumed = fatty_acid_energy * 1000 / 9  # Convert kcal to mg
            energy_demanded -= fatty_acid_energy
        else:
            fatty_acid_consumed = 0
        
        # Amino acid consumption (last resort)
        if energy_demanded > 0:
            amino_acid_energy = min(energy_demanded, amino_acid_available * 4 / 1000)  # 4 kcal/g of protein
            amino_acid_consumed = amino_acid_energy * 1000 / 4  # Convert kcal to mg
        else:
            amino_acid_consumed = 0
        
        # Calculate total energy from each source
        total_energy = (glucose_consumed * 4 + fatty_acid_consumed * 9 + amino_acid_consumed * 4) / 1000  # kcal
        
        # Calculate respiratory quotient (RQ)
        if total_energy > 0:
            rq = (glucose_consumed * 1.0 + fatty_acid_consumed * 0.7 + amino_acid_consumed * 0.8) / (glucose_consumed + fatty_acid_consumed + amino_acid_consumed)
        else:
            rq = 0.85  # Default RQ if no energy consumed
        
        # Calculate oxygen consumption based on energy expenditure and RQ
        oxygen_consumed = total_energy * 0.2 / rq  # Approximate relationship between energy, RQ, and O2 consumption
        
        # Ensure we don't consume more than available oxygen
        if oxygen_consumed > oxygen_available:
            oxygen_consumed = oxygen_available
            # Adjust energy consumption based on available oxygen
            actual_total_energy = oxygen_consumed * rq / 0.2  # Reverse the calculation of oxygen consumption
            
            # Recalculate nutrient consumption based on adjusted energy
            glucose_consumed *= actual_total_energy / total_energy
            fatty_acid_consumed *= actual_total_energy / total_energy
            amino_acid_consumed *= actual_total_energy / total_energy
            total_energy = actual_total_energy
        
        # Calculate CO2 production based on oxygen consumption and RQ
        co2_produced = oxygen_consumed * rq  # mL CO2
        
        # Update blood nutrient levels
        self.blood.glucose_amount -= glucose_consumed
        self.blood.fatty_acid_amount -= fatty_acid_consumed
        self.blood.amino_acid_amount -= amino_acid_consumed
        
        # Update blood oxygen levels
        self.blood.oxygen_amount -= oxygen_consumed
        
        # Update blood CO2 concentration
        co2_produced_mmol = co2_produced * 0.0308  # Convert mL CO2 to mmol
        self.blood.co2_amount += co2_produced_mmol

    def process_insulin(self, dt: float) -> None:
        insulin_effect = self.blood.insulin_concentration * self.insulin_sensitivity
        glucose_uptake = min(
            self.energy_demand * dt / 3600 * 1000 / 4 * insulin_effect / 10,  # Convert kcal to mg glucose, adjust for μU/mL
            self.blood.glucose_amount * 0.1  # Limit uptake to 10% of available glucose
        )
        self.blood.glucose_amount -= glucose_uptake

    def _organ_specific_processing(self, dt: float) -> None:
        # To be overridden by subclasses
        pass

    def update(self, dt: float):
        self.consume_nutrients(dt)
        self.process_insulin(dt)
        self._organ_specific_processing(dt)


class Heart(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=6,  # kcal/hour
            oxygen_demand=30,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.pumping_rate = 60  # beats per minute
        self.stroke_volume = 70  # mL per beat
        self.ejection_fraction = 0.6  # dimensionless
        self.cardiac_output = 0  # L/min
        self.time_since_last_beat = 0  # seconds
        self.base_peripheral_resistance = 1200  # dyn·s/cm^5
        self.peripheral_resistance = self.base_peripheral_resistance
        self.compression = 0  # dimensionless, ranges from 0 (relaxed) to 1 (fully contracted)

    def _organ_specific_processing(self, dt: float) -> None:
        self.time_since_last_beat += dt
        beat_interval = 60 / self.pumping_rate  # seconds

        if self.time_since_last_beat >= beat_interval:
            self.heartbeat(dt)
            self.time_since_last_beat %= beat_interval

        self.update_compression(dt)

    def update_compression(self, dt: float):
        beat_phase = self.time_since_last_beat / (60 / self.pumping_rate)
        
        # Modified Gaussian function for systole
        systole_duration = 0.3  # 30% of the cardiac cycle
        if beat_phase < systole_duration:
            self.compression = math.exp(-((beat_phase - 0.15) / 0.1) ** 2)
        else:
            # Rapid relaxation followed by slow relaxation
            relaxation_rate = 5 if beat_phase < 0.5 else 1
            self.compression *= math.exp(-relaxation_rate * dt)

    def heartbeat(self, dt: float):
        self.cardiac_output = (self.stroke_volume * self.pumping_rate) / 1000  # L/min
        self.update_peripheral_resistance()
        self.calculate_blood_pressure()

    def update_peripheral_resistance(self):
        # Consider multiple factors affecting peripheral resistance
        epinephrine_effect = 1 + 0.2 * (self.blood.epinephrine_concentration - 1)
        volume_effect = 1 - 0.1 * ((self.blood.volume - 5000) / 5000)
        
        # Add more factors here (e.g., nitric oxide, angiotensin II)
        
        self.peripheral_resistance = self.base_peripheral_resistance * epinephrine_effect * volume_effect

    def calculate_blood_pressure(self):
        # Use the revised formula: MAP = CO * PVR / 80
        mean_arterial_pressure = (self.cardiac_output * self.peripheral_resistance) / 80

        # Calculate pulse pressure based on stroke volume and arterial compliance
        arterial_compliance = 1.5  # mL/mmHg
        pulse_pressure = self.stroke_volume / arterial_compliance

        self.blood.systolic_pressure = mean_arterial_pressure + (pulse_pressure / 2)
        self.blood.diastolic_pressure = mean_arterial_pressure - (pulse_pressure / 2)

        # Ensure blood pressure stays within physiological limits
        self.blood.systolic_pressure = max(90, min(180, self.blood.systolic_pressure))
        self.blood.diastolic_pressure = max(60, min(120, self.blood.diastolic_pressure))

    def adjust_rate(self, factor: float):
        self.pumping_rate = max(40, min(200, self.pumping_rate * factor))  # beats per minute

    def receive_brain_signal(self, signal: float):
        self.adjust_rate(1 + signal * 0.1)

    def _organ_specific_metrics(self) -> dict:
        metrics = super()._organ_specific_metrics()
        metrics.update({
            "pumping_rate": {"value": self.pumping_rate, "unit": "beats/min"},
            "cardiac_output": {"value": self.cardiac_output, "unit": "L/min"},
            "ejection_fraction": {"value": self.ejection_fraction, "unit": ""},
            "stroke_volume": {"value": self.stroke_volume, "unit": "mL/beat"},
            "systolic_pressure": {"value": self.blood.systolic_pressure, "unit": "mmHg"},
            "diastolic_pressure": {"value": self.blood.diastolic_pressure, "unit": "mmHg"},
            "peripheral_resistance": {"value": self.peripheral_resistance, "unit": "dyn·s/cm^5"},
            "compression": {"value": self.compression, "unit": ""},
        })
        return metrics

class Lungs(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            oxygen_demand=5,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.tidal_volume = 500  # mL
        self.respiratory_rate = 12  # breaths per minute
        self.alveolar_po2 = 100  # mmHg
        self.alveolar_pco2 = 40  # mmHg
        self.diffusion_capacity_o2 = 25  # mL/min/mmHg
        self.diffusion_capacity_co2 = 400  # mL/min/mmHg
        self.expansion = 0  # dimensionless, ranges from 0 (fully exhaled) to 1 (fully inhaled)
        self.previous_expansion = 0  # to track expansion delta
        self.time_since_last_breath = 0  # seconds
        self.functional_residual_capacity = 2500  # mL
        self.dead_space_volume = 150  # mL

    def _organ_specific_processing(self, dt: float) -> None:
        self.time_since_last_breath += dt
        breath_interval = 60 / self.respiratory_rate  # seconds
        self.time_since_last_breath %= breath_interval

        self.update_expansion(dt)
        self.simulate_gas_exchange(dt)

    def update_expansion(self, dt: float):
        self.previous_expansion = self.expansion
        breath_phase = self.time_since_last_breath / (60 / self.respiratory_rate)
        
        # Sinusoidal function for continuous breathing motion
        self.expansion = 0.5 * (1 + math.sin(2 * math.pi * breath_phase - math.pi / 2))

    def simulate_gas_exchange(self, dt: float):
        expansion_delta = self.expansion - self.previous_expansion
        volume_delta = expansion_delta * self.tidal_volume

        alveolar_volume = self.functional_residual_capacity + (self.tidal_volume * self.expansion)

        # Fresh air composition
        fresh_o2 = 150  # mmHg
        fresh_co2 = 0.3  # mmHg

        if volume_delta > 0:  # Inhaling
            # Mix fresh air with existing alveolar air
            fresh_fraction = volume_delta / alveolar_volume
            self.alveolar_po2 = (1 - fresh_fraction) * self.alveolar_po2 + fresh_fraction * fresh_o2
            self.alveolar_pco2 = (1 - fresh_fraction) * self.alveolar_pco2 + fresh_fraction * fresh_co2
        else:  # Exhaling
            # No change in gas concentrations during exhalation
            pass

        # O2 exchange
        blood_po2 = self.oxygen_hemoglobin_dissociation(self.blood.oxygen_saturation * 100)
        diffusable_o2 = (self.alveolar_po2 - blood_po2) * self.diffusion_capacity_o2 * dt / 60
        diffused_o2 = min(diffusable_o2, self.blood.total_oxygen_capacity - self.blood.oxygen_amount)
        self.blood.oxygen_amount += diffused_o2
        self.alveolar_po2 -= diffused_o2 * 760 / (22.4 * alveolar_volume / 1000)

        # CO2 exchange
        blood_pco2 = self.blood.co2_concentration / 0.03
        diffusable_co2 = (blood_pco2 - self.alveolar_pco2) * self.diffusion_capacity_co2 * dt / 60
        diffused_co2 = max(diffusable_co2, 0)
        self.blood.co2_amount -= diffused_co2
        self.alveolar_pco2 += diffused_co2 * 760 / (22.4 * alveolar_volume / 1000)

    def oxygen_hemoglobin_dissociation(self, po2: float) -> float:
        return 100 * (po2**2.8) / ((po2**2.8) + 26**2.8)

    def _organ_specific_metrics(self) -> dict:
        return {
            "tidal_volume": {"value": self.tidal_volume, "unit": "mL"},
            "respiratory_rate": {"value": self.respiratory_rate, "unit": "breaths/min"},
            "alveolar_po2": {"value": self.alveolar_po2, "unit": "mmHg"},
            "alveolar_pco2": {"value": self.alveolar_pco2, "unit": "mmHg"},
            "expansion": {"value": self.expansion, "unit": ""},
            "alveolar_volume": {"value": self.functional_residual_capacity + (self.tidal_volume * self.expansion), "unit": "mL"},
            "minute_ventilation": {"value": self.tidal_volume * self.respiratory_rate / 1000, "unit": "L/min"},
            "alveolar_ventilation": {"value": (self.tidal_volume - self.dead_space_volume) * self.respiratory_rate / 1000, "unit": "L/min"}
        }


class Kidneys(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=10,  # kcal/hour
            oxygen_demand=10,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.waste_filtering_rate = 0.1  # dimensionless
        self.urine_production_rate = 1 / 60  # mL/s (equivalent to 1 mL/min)
        self.bladder = None

    def set_bladder(self, bladder):
        self.bladder = bladder

    def _organ_specific_processing(self, dt: float) -> None:
        self.regulate_blood_ph(dt)
        self.produce_urine(dt)

    def produce_urine(self, dt: float):
        # Calculate urine production based on blood volume and hydration status
        base_production = self.urine_production_rate * dt
        blood_volume_factor = max(0, min(2, self.blood.volume / 5000))  # Normalize around 5000 mL blood volume
        hydration_factor = max(0.5, min(1.5, self.blood.plasma_volume / 3000))  # Normalize around 3000 mL plasma volume
        
        urine_produced = base_production * blood_volume_factor * hydration_factor
        
        if self.bladder:
            self.bladder.receive_urine(urine_produced)
        
        self.blood.volume -= urine_produced

    def regulate_blood_ph(self, dt: float):
        target_ph = 7.4
        current_ph = self.blood.ph
        ph_difference = current_ph - target_ph

        # Adjust bicarbonate reabsorption based on pH
        if ph_difference < -0.05:  # Acidosis
            bicarbonate_change = 0.2 * dt * (self.blood.volume / 1000)
        elif ph_difference > 0.05:  # Alkalosis
            bicarbonate_change = -0.2 * dt * (self.blood.volume / 1000)
        else:
            bicarbonate_change = 0

        # Update blood bicarbonate content
        self.blood.bicarbonate_amount += bicarbonate_change

        # Adjust hydrogen ion excretion
        if ph_difference < 0:
            h_ion_excretion = 0.1 * abs(ph_difference) * dt
        else:
            h_ion_excretion = -0.05 * ph_difference * dt

        # Update blood pH based on hydrogen ion excretion
        self.blood.ph += h_ion_excretion

        # Ensure pH stays within physiological limits
        self.blood.ph = max(6.8, min(7.8, self.blood.ph))

        # Adjust urine production based on pH
        if ph_difference < -0.1:
            self.urine_production_rate *= 1.1  # Increase urine production to excrete more acid
        elif ph_difference > 0.1:
            self.urine_production_rate *= 0.9  # Decrease urine production to retain more bicarbonate

        # Ensure urine production rate stays within reasonable limits
        self.urine_production_rate = max(0.5 / 60, min(2 / 60, self.urine_production_rate))

    def increase_urine_production(self, dt: float):
        self.urine_production_rate *= (1 + 0.1 * dt)
        self.urine_production_rate = min(2 / 60, self.urine_production_rate)  # Max 2 mL/s

    def decrease_urine_production(self, dt: float):
        self.urine_production_rate *= (1 - 0.1 * dt)
        self.urine_production_rate = max(0.5 / 60, self.urine_production_rate)  # Min 0.5 mL/s

    def _organ_specific_metrics(self) -> dict:
        return {
            "waste_filtering_rate": {"value": self.waste_filtering_rate, "unit": ""},
            "urine_production_rate": {"value": self.urine_production_rate, "unit": "mL/s"}
        }


class Muscle(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=30,  # kcal/hour
            insulin_sensitivity=1.5,  # dimensionless
            oxygen_demand=20,  # mL O2/min
        )
        self.glucose_uptake_rate = 2  # mg/min at rest
        self.glycogen_storage = 500  # g
        self.base_energy_demand = 30  # kcal/hour

    def _organ_specific_processing(self, dt: float) -> None:
        glucose_consumed = min(self.glucose_uptake_rate * dt / 60, self.blood.glucose_amount * 0.1)
        self.blood.glucose_amount -= glucose_consumed

        if self.energy_demand > self.base_energy_demand and self.glycogen_storage > 0:
            exercise_intensity = (self.energy_demand - self.base_energy_demand) / self.base_energy_demand
            glycogen_used = min(exercise_intensity * 5 * dt / 60, self.glycogen_storage)  # Up to 5 g/min during intense exercise
            self.glycogen_storage -= glycogen_used
            self.blood.glucose_amount += glycogen_used * 1000  # Convert g to mg

    def increase_energy_demand(self, factor: float):
        self.energy_demand = self.base_energy_demand * factor
        self.oxygen_demand = self.oxygen_demand * factor
        self.glucose_uptake_rate = 2 + 18 * (factor - 1)  # Up to 20 mg/min during intense exercise

    def reset_energy_demand(self):
        self.energy_demand = self.base_energy_demand
        self.oxygen_demand = 20  # mL O2/min
        self.glucose_uptake_rate = 2  # mg/min at rest

    def _organ_specific_metrics(self) -> dict:
        return {
            "glucose_uptake_rate": {"value": self.glucose_uptake_rate, "unit": "mg/min"},
            "glycogen_storage": {"value": self.glycogen_storage, "unit": "g"},
            "energy_demand": {"value": self.energy_demand, "unit": "kcal/hour"}
        }


class Brain(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=20,  # kcal/hour
            oxygen_demand=3.5,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.baroreceptor_sensitivity = 1.0  # dimensionless
        self.target_map = 93  # mmHg (mean arterial pressure)
        self.lungs = None  # Will be set by the HumanBody class
        self.heart = None  # Will be set by the HumanBody class
        self.kidneys = None  # Will be set by the HumanBody class
        self.muscles = None  # Will be set by the HumanBody class

    def _organ_specific_processing(self, dt: float) -> None:
        self.regulate_blood_pressure(dt)
        self.regulate_respiratory_rate(dt)
        self.regulate_glucose(dt)

    def regulate_respiratory_rate(self, dt: float):
        if self.lungs:
            if self.blood.co2_concentration > 29:  # mmol/L
                self.lungs.respiratory_rate = self.lungs.respiratory_rate + 0.5 * dt
            elif self.blood.co2_concentration < 20:  # mmol/L
                self.lungs.respiratory_rate = self.lungs.respiratory_rate - 0.5 * dt
            else:
                # Gradually return to normal respiratory rate
                normal_rate = 12
                if self.lungs.respiratory_rate > normal_rate:
                    self.lungs.respiratory_rate = self.lungs.respiratory_rate - 0.1 * dt
                elif self.lungs.respiratory_rate < normal_rate:
                    self.lungs.respiratory_rate = self.lungs.respiratory_rate + 0.1 * dt

    def regulate_blood_pressure(self, dt: float):
        current_map = self.blood.mean_arterial_pressure
        map_error = current_map - self.target_map

        # Baroreceptor reflex
        baroreceptor_response = self.baroreceptor_sensitivity * map_error * 0.01

        # Adjust heart rate
        self.heart.receive_brain_signal(-baroreceptor_response)

        # Adjust peripheral resistance
        resistance_change = max(-0.1, min(0.1, baroreceptor_response * 0.5))
        self.heart.peripheral_resistance *= (1 + resistance_change * dt)

        # Update epinephrine level
        if map_error < -5:
            self.blood.epinephrine_amount = min(2000, self.blood.epinephrine_amount * (1 + 0.1 * dt))
        elif map_error > 5:
            self.blood.epinephrine_amount = max(250, self.blood.epinephrine_amount * (1 - 0.1 * dt))

        # Adjust blood volume through kidney function
        if self.kidneys:
            if map_error > 5:
                self.kidneys.increase_urine_production(dt)
            elif map_error < -5:
                self.kidneys.decrease_urine_production(dt)

    def regulate_glucose(self, dt: float):
        if self.blood.glucose_concentration < 60:
            # Stimulate glucagon release
            self.blood.glucagon_amount += 0.1 * dt * (self.blood.volume / 1000)
            # Increase epinephrine to stimulate glucose release
            self.blood.epinephrine_amount = min(2000 * (self.blood.volume / 1000), self.blood.epinephrine_amount * 1.2)
        elif self.blood.glucose_concentration > 140:
            # Stimulate insulin release
            self.blood.insulin_amount += 0.1 * dt * (self.blood.volume / 1000)

        # Ensure brain always gets glucose
        glucose_consumed = min(self.energy_demand * dt / 3600 * 1000 / 4, self.blood.glucose_amount * 0.1)
        self.blood.glucose_amount -= glucose_consumed

    def set_lungs(self, lungs: Lungs):
        self.lungs = lungs

    def set_heart(self, heart: Heart):
        self.heart = heart

    def set_kidneys(self, kidneys: Kidneys):
        self.kidneys = kidneys

    def set_muscles(self, muscles: Muscle):
        self.muscles = muscles

    def start_exercise(self):
        if self.muscles:
            self.muscles.increase_energy_demand(2)  # Double the energy demand

    def stop_exercise(self):
        if self.muscles:
            self.muscles.reset_energy_demand()

    def _organ_specific_metrics(self) -> dict:
        return {
            "baroreceptor_sensitivity": {"value": self.baroreceptor_sensitivity, "unit": ""},
        }


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
        self.store_fat(dt)
        self.release_fat(dt)

    def store_fat(self, dt: float):
        if self.blood.glucose_concentration > 120 and self.blood.insulin_concentration > 1.0:
            glucose_stored = min(self.blood.glucose_amount * 0.1, 10 * dt * self.insulin_sensitivity)
            fat_stored = glucose_stored * 0.11 / 1000  # 1g of fat is about 9 kcal, and 1g of glucose is about 4 kcal
            self.blood.glucose_amount -= glucose_stored
            self.fat_reserve += fat_stored
            self.blood.fat_amount += fat_stored * 1000  # Convert g to mg

    def release_fat(self, dt: float):
        if self.blood.glucose_concentration < 80 or self.blood.glucagon_concentration > 1.0:
            lipolysis_factor = max(1, (80 - self.blood.glucose_concentration) / 10)
            fat_released = min(self.lipolysis_rate * lipolysis_factor * dt / 60, self.fat_reserve)
            self.fat_reserve -= fat_released
            self.blood.fat_amount += fat_released * 1000  # Convert g to mg

    def _organ_specific_metrics(self) -> dict:
        return {
            "fat_reserve": {"value": self.fat_reserve, "unit": "g"},
            "insulin_sensitivity": {"value": self.insulin_sensitivity, "unit": ""},
            "glucagon_sensitivity": {"value": self.glucagon_sensitivity, "unit": ""},
            "lipolysis_rate": {"value": self.lipolysis_rate, "unit": "g/min"},
        }


class Liver(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=20,  # kcal/hour
            insulin_sensitivity=0.8  # dimensionless
        )
        self.glucose_storage = 100  # Glycogen storage in g

    def _organ_specific_processing(self, dt: float) -> None:
        self.regulate_glucose(dt)
        self.regulate_blood_ph(dt)

    def regulate_glucose(self, dt: float):
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

    def regulate_blood_ph(self, dt: float):
        # Simulate ammonia production
        ammonia_production = 0.1 * dt
        
        # Convert ammonia to urea (which is less acidic)
        urea_production = ammonia_production * 0.8
        
        # Adjust blood pH based on urea production
        ph_change = urea_production * 0.01
        self.blood.ph += ph_change

    def _organ_specific_metrics(self) -> dict:
        return {
            "glucose_storage": {"value": self.glucose_storage, "unit": "g"},
        }


class Stomach(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            oxygen_demand=5,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.digestion_rate = 0.1  # fraction of food processed per minute
        self.food_content = 0  # mg of food in stomach
        self.water_content = 0  # mL of water in stomach
        self.intestines = None  # Will be set by the HumanBody class

    def _organ_specific_processing(self, dt: float) -> None:
        if self.food_content > 0:
            digested_amount = min(self.food_content, self.digestion_rate * self.food_content * dt)
            self.food_content -= digested_amount
            self.intestines.receive_nutrients(digested_amount)

        if self.water_content > 0:
            water_passed = min(self.water_content, 10 * dt)  # Pass up to 10 mL/s to intestines
            self.water_content -= water_passed
            self.intestines.receive_water(water_passed)

    def receive_water(self, amount: float):
        self.water_content += amount

    def receive_food(self, amount: float):
        self.food_content += amount

    def set_intestines(self, intestines):
        self.intestines = intestines

    def _organ_specific_metrics(self) -> dict:
        return {
            "digestion_rate": {"value": self.digestion_rate, "unit": ""},
            "food_content": {"value": self.food_content, "unit": "mg"},
            "water_content": {"value": self.water_content, "unit": "mL"}
        }


class Intestines(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            oxygen_demand=5,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.absorption_rate = 0.2  # fraction of nutrients absorbed per minute
        self.available_nutrients = 0  # mg
        self.water_content = 0  # mL
        self.water_absorption_rate = 5  # mL/min

    def _organ_specific_processing(self, dt: float) -> None:
        if self.available_nutrients > 0:
            absorbed_nutrients = min(
                self.available_nutrients,
                self.absorption_rate * self.available_nutrients * dt
            )
            self.available_nutrients -= absorbed_nutrients

            glucose_increase = absorbed_nutrients * 0.7
            other_nutrients = absorbed_nutrients * 0.3

            self.blood.glucose_amount += glucose_increase
            self.blood.nutrient_amount += other_nutrients

        if self.water_content > 0:
            absorbed_water = min(self.water_content, self.water_absorption_rate * dt)
            self.water_content -= absorbed_water
            self.blood.volume += absorbed_water

    def receive_water(self, amount: float):
        self.water_content += amount

    def _organ_specific_metrics(self) -> dict:
        return {
            "absorption_rate": {"value": self.absorption_rate, "unit": ""},
            "available_nutrients": {"value": self.available_nutrients, "unit": "mg"},
            "water_content": {"value": self.water_content, "unit": "mL"}
        }


class Skin(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            oxygen_demand=5,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.temperature = 37.0  # Normal body temperature in Celsius

    def _organ_specific_processing(self, dt: float) -> None:
        # Simple temperature regulation
        if self.temperature > 37.5:
            self.temperature -= 0.1 * dt
        elif self.temperature < 36.5:
            self.temperature += 0.1 * dt

    def _organ_specific_metrics(self) -> dict:
        return {"temperature": {"value": self.temperature, "unit": "°C"}}


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
        self.produce_hormones(dt)

    def produce_hormones(self, dt: float):
        # Insulin production
        base_insulin_production = 0.5 * dt / 60  # Base production rate
        if self.blood.glucose_concentration > 90:
            glucose_stimulus = (self.blood.glucose_concentration - 90) / 10
            insulin_produced = (base_insulin_production + self.insulin_production_rate * glucose_stimulus) * dt
            self.blood.insulin_amount += insulin_produced * (self.blood.volume / 1000)
        else:
            self.blood.insulin_amount = max(0, self.blood.insulin_amount - 0.5 * dt)

        # Glucagon production
        base_glucagon_production = 0.1 * dt / 60  # Base production rate
        if self.blood.glucose_concentration < 80:
            glucose_stimulus = (80 - self.blood.glucose_concentration) / 10
            glucagon_produced = (base_glucagon_production + self.glucagon_production_rate * glucose_stimulus) * dt
            self.blood.glucagon_amount += glucagon_produced
        else:
            self.blood.glucagon_amount = max(0, self.blood.glucagon_amount - 0.05 * dt)

    def _organ_specific_metrics(self) -> dict:
        return {
            "insulin_production_rate": {"value": self.insulin_production_rate, "unit": "μU/mL/min"},
            "glucagon_production_rate": {"value": self.glucagon_production_rate, "unit": "ng/mL/min"},
        }


class Spleen(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            oxygen_demand=5,  # mL O2/min
            insulin_sensitivity=1.0  # dimensionless
        )
        self.blood_storage = 200  # mL

    def _organ_specific_processing(self, dt: float) -> None:
        # Spleen-specific blood processing logic
        pass

    def _organ_specific_metrics(self) -> dict:
        return {"blood_storage": {"value": self.blood_storage, "unit": "mL"}}


class Bladder(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=1,  # kcal/hour
            oxygen_demand=1,  # mL O2/min
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
            "urine_volume": {"value": self.urine_volume, "unit": "mL"},
            "fullness_percentage": {"value": (self.urine_volume / self.max_capacity) * 100, "unit": "%"}
        }


class HumanBody:
    def __init__(self):
        self.blood = Blood(volume=5000)  # Total blood volume in mL

        # Initialize organs
        self.lungs = Lungs(self.blood)
        self.brain = Brain(self.blood)
        self.heart = Heart(self.blood)
        self.kidneys = Kidneys(self.blood)
        self.liver = Liver(self.blood)
        self.muscles = Muscle(self.blood)
        self.pancreas = Pancreas(self.blood)
        self.fat = Fat(self.blood)
        self.stomach = Stomach(self.blood)
        self.intestines = Intestines(self.blood)
        self.skin = Skin(self.blood)
        self.spleen = Spleen(self.blood)
        self.bladder = Bladder(self.blood)

        # Connect brain to lungs, heart, and muscles
        self.brain.set_lungs(self.lungs)
        self.brain.set_heart(self.heart)
        self.brain.set_kidneys(self.kidneys)
        self.brain.set_muscles(self.muscles)

        # Connect kidneys to bladder
        self.kidneys.set_bladder(self.bladder)

        self.is_exercising = False

        # Connect stomach to intestines
        self.stomach.set_intestines(self.intestines)

        self.time = 0  # in seconds
        self.total_caloric_expenditure = 0  # in kcal

    def start_exercise(self):
        self.is_exercising = True
        self.brain.start_exercise()

    def stop_exercise(self):
        self.is_exercising = False
        self.brain.stop_exercise()

    def step(self) -> float:
        dt = 0.1  # Fixed time step of 0.1 seconds

        self.time += dt

        organs = [
            self.heart, self.lungs, self.brain, self.kidneys, self.liver,
            self.muscles, self.pancreas, self.fat, self.stomach,
            self.intestines, self.skin, self.spleen, self.bladder
        ]
        
        total_energy_expenditure = 0
        for organ in organs:
            organ.update(dt)
            total_energy_expenditure += organ.energy_demand * (dt / 3600)  # Convert to kcal/step
        
        self.total_caloric_expenditure += total_energy_expenditure
        
        self.blood.update(dt)
        
        return dt

    def get_metrics(self):
        metrics = {
            "Time": {"value": self.time, "unit": "s"},
            "Energy": {
                "Total Caloric Expenditure": {"value": self.total_caloric_expenditure, "unit": "kcal"},
                "Daily Projected Caloric Expenditure": {"value": self.total_caloric_expenditure * 60 * 60 * 24 / self.time, "unit": "kcal"},
            },
            "Blood": self.blood.get_metrics(),
            "Organs": {}
        }
        
        organs = {
            "Heart": self.heart,
            "Lungs": self.lungs,
            "Brain": self.brain,
            "Kidneys": self.kidneys,
            "Liver": self.liver,
            "Muscles": self.muscles,
            "Pancreas": self.pancreas,
            "Fat": self.fat,
            "Stomach": self.stomach,
            "Intestines": self.intestines,
            "Skin": self.skin,
            "Spleen": self.spleen,
            "Bladder": self.bladder,
        }
        
        for organ_name, organ in organs.items():
            metrics["Organs"][organ_name] = organ.get_metrics()
        
        return metrics

    def drink(self, water_amount: float):
        self.stomach.receive_water(water_amount)

    def eat(self, food_amount: float):
        self.stomach.receive_food(food_amount)

    def pee(self):
        self.bladder.urinate()
