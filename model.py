import math


class Blood:
    def __init__(
        self,
        volume: float = 5000,  # mL
    ):
        self.volume = volume
        self.glucose_amount = 4500 * (volume / 5000)  # mg
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
        self.oxygen_saturation = 0.98  # dimensionless (fraction)
        self.dissolved_oxygen = 0.003  # mL O2 / dL blood
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
            "oxygen_saturation": {"value": self.oxygen_saturation, "unit": ""},
            "dissolved_oxygen": {"value": self.dissolved_oxygen, "unit": "mL O2/dL blood"},
            "total_oxygen_content": {"value": self.get_oxygen_content(), "unit": "mL O2"},
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

    def calculate_oxygen_content(self):
        # Oxygen content (mL O2 / dL blood) = (1.34 * Hb * SaO2) + dissolved O2
        return (1.34 * self.hemoglobin * self.oxygen_saturation) + self.dissolved_oxygen

    def get_oxygen_content(self):
        return self.calculate_oxygen_content() * (self.volume / 100)  # Total oxygen in mL


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
        oxygen_available = self.blood.get_oxygen_content()  # mL O2
        glucose_available = self.blood.glucose_amount  # mg
        fat_available = self.blood.fat_amount  # mg
        
        # Calculate energy consumption based on demand and availability
        energy_consumed = self.energy_demand * dt / 3600  # kcal, adjusted for dt in seconds
        
        # Determine energy sources
        energy_from_fat = min(energy_consumed * self.fat_oxidation_rate, fat_available * 9 / 1000)  # 9 kcal/g of fat
        energy_from_glucose = energy_consumed - energy_from_fat
        
        # Convert energy to glucose and fat consumption
        glucose_consumed = energy_from_glucose * 1000 / 4  # 1 g glucose = 4 kcal, convert to mg
        fat_consumed = energy_from_fat * 1000 / 9  # 1 g fat = 9 kcal, convert to mg
        
        # Ensure we don't consume more than available
        glucose_consumed = min(glucose_consumed, glucose_available)
        fat_consumed = min(fat_consumed, fat_available)
        
        # Calculate oxygen consumption
        oxygen_consumed = min(self.oxygen_demand * dt / 60, oxygen_available)  # mL O2, adjusted for dt in seconds
        
        # Calculate respiratory quotient (RQ) based on mixture of glucose and fat metabolism
        total_consumed = glucose_consumed + fat_consumed
        rq = (glucose_consumed * 1.0 + fat_consumed * 0.7) / total_consumed if total_consumed > 0 else 0.85
        
        # Calculate CO2 production based on oxygen consumption and RQ
        co2_produced = oxygen_consumed * rq  # mL CO2
        
        # Update blood oxygen, glucose, and fat levels
        oxygen_saturation_change = oxygen_consumed / (1.34 * self.blood.hemoglobin * self.blood.volume / 100)
        self.blood.oxygen_saturation = max(0, self.blood.oxygen_saturation - oxygen_saturation_change)
        self.blood.glucose_amount -= glucose_consumed
        self.blood.fat_amount -= fat_consumed
        
        # Update blood CO2 concentration
        # Convert mL CO2 to mmol CO2 using a more appropriate conversion factor
        # Approximately 0.0308 mmol/mL at body temperature and pressure
        co2_produced_mmol = co2_produced * 0.0308
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
        self.partial_pressure_o2 = 100  # mmHg
        self.alveolar_pco2 = 40  # mmHg
        self.diffusion_capacity_o2 = 25  # mL/min/mmHg
        self.diffusion_capacity_co2 = 400  # mL/min/mmHg
        self.expansion = 0  # dimensionless, ranges from 0 (fully exhaled) to 1 (fully inhaled)
        self.previous_expansion = 0  # to track expansion delta
        self.time_since_last_breath = 0  # seconds
        self.functional_residual_capacity = 2500  # mL
        self.dead_space_volume = 150  # mL
        self.compliance = 200  # mL/cmH2O
        self.resistance = 1  # cmH2O/L/s

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
            self.partial_pressure_o2 = (1 - fresh_fraction) * self.partial_pressure_o2 + fresh_fraction * fresh_o2
            self.alveolar_pco2 = (1 - fresh_fraction) * self.alveolar_pco2 + fresh_fraction * fresh_co2
        else:  # Exhaling
            # No change in gas concentrations during exhalation
            pass

        # O2 exchange
        o2_gradient = self.partial_pressure_o2 - (self.blood.oxygen_saturation * 100)
        o2_diffusion = self.diffusion_capacity_o2 * o2_gradient * dt / 60
        new_o2_content = self.blood.calculate_oxygen_content() + (o2_diffusion / self.blood.volume)
        self.blood.oxygen_saturation = self.oxygen_hemoglobin_dissociation(new_o2_content / (1.34 * self.blood.hemoglobin) * 100)

        # CO2 exchange
        co2_gradient = self.blood.co2_concentration - self.alveolar_pco2  # mmol/L - mmHg
        co2_diffusion = self.diffusion_capacity_co2 * co2_gradient * dt / 60  # mL/min * mmHg * min = mL
        co2_diffusion_mmol = co2_diffusion * 0.0446  # Convert mL to mmol (1 mmol of CO2 = 22.4 mL at STP)
        self.blood.co2_amount -= co2_diffusion_mmol  # mmol

        # Update alveolar gas concentrations
        self.partial_pressure_o2 -= (o2_diffusion * 760 / alveolar_volume)
        self.alveolar_pco2 += (co2_diffusion * 760 / alveolar_volume)

    def oxygen_hemoglobin_dissociation(self, po2: float) -> float:
        return 100 * (po2**2.8) / ((po2**2.8) + 26**2.8)

    def _organ_specific_metrics(self) -> dict:
        return {
            "tidal_volume": {"value": self.tidal_volume, "unit": "mL"},
            "respiratory_rate": {"value": self.respiratory_rate, "unit": "breaths/min"},
            "partial_pressure_o2": {"value": self.partial_pressure_o2, "unit": "mmHg"},
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

    def _organ_specific_metrics(self) -> dict:
        return {
            "baroreceptor_sensitivity": {"value": self.baroreceptor_sensitivity, "unit": ""},
        }


class Muscle(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=30,  # kcal/hour
            insulin_sensitivity=1.5,  # dimensionless
            oxygen_demand=20,  # mL O2/min
        )
        self.fat_oxidation_rate = 0.3  # 30% of energy from fat at rest
        self.is_exercising = False

    def _organ_specific_processing(self, dt: float) -> None:
        # Adjust fat oxidation rate based on exercise intensity
        if self.is_exercising:
            exercise_intensity = min((self.energy_demand - 30) / 100, 1)  # Normalize to 0-1
            self.fat_oxidation_rate = max(0.1, 0.3 - 0.2 * exercise_intensity)  # Decrease fat oxidation as intensity increases
        else:
            self.fat_oxidation_rate = 0.3

    def start_exercise(self):
        self.is_exercising = True
        self.energy_demand *= 2
        self.oxygen_demand *= 2

    def stop_exercise(self):
        self.is_exercising = False
        self.energy_demand /= 2
        self.oxygen_demand /= 2

    def _organ_specific_metrics(self) -> dict:
        return {
            "fat_oxidation_rate": {"value": self.fat_oxidation_rate, "unit": ""},
            "is_exercising": {"value": self.is_exercising, "unit": ""}
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
        glucagon_effect = self.blood.glucagon_concentration

        if self.blood.glucose_concentration > 110:
            glucose_stored = min(self.blood.glucose_amount * 0.1, 10 * insulin_effect * dt)
            self.blood.glucose_amount -= glucose_stored
            self.glucose_storage += glucose_stored / 100  # Convert mg to g
        elif self.blood.glucose_concentration < 70 and self.glucose_storage > 0:
            glucose_released = min(70 - self.blood.glucose_concentration, self.glucose_storage * 100, 10 * glucagon_effect * dt)
            self.blood.glucose_amount += glucose_released
            self.glucose_storage -= glucose_released / 100  # Convert mg to g

        # Gluconeogenesis
        if self.blood.glucose_concentration < 60:
            glucose_produced = 5 * dt / 60  # Produce 5 mg/min of glucose, adjusted for dt in seconds
            self.blood.glucose_amount += glucose_produced

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
        if self.blood.glucose_concentration > 110:
            insulin_produced = self.insulin_production_rate * (self.blood.glucose_concentration - 110) / 10 * dt
            self.blood.insulin_amount += insulin_produced * (self.blood.volume / 1000)
        else:
            self.blood.insulin_amount = max(0, self.blood.insulin_amount - 0.5 * dt)

        # Glucagon production
        if self.blood.glucose_concentration < 70:
            glucagon_produced = self.glucagon_production_rate * (70 - self.blood.glucose_concentration) / 10 * dt
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

        # Connect brain to lungs and heart
        self.brain.set_lungs(self.lungs)
        self.brain.set_heart(self.heart)
        self.brain.set_kidneys(self.kidneys)

        # Connect kidneys to bladder
        self.kidneys.set_bladder(self.bladder)

        self.is_exercising = False

        # Connect stomach to intestines
        self.stomach.set_intestines(self.intestines)

        self.time = 0  # in seconds
        self.total_caloric_expenditure = 0  # in kcal

    def advance(self, dt: float):
        finish_time = self.time + dt
        while self.time < finish_time:
            self.step()
        
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

        if self.is_exercising:
            self.exercise(dt)
        
        return dt

    def get_metrics(self):
        metrics = {
            "Time": {"value": self.time, "unit": "s"},
            "Energy": {
                "Total Caloric Expenditure": {"value": self.total_caloric_expenditure, "unit": "kcal"}
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

    def exercise(self, dt: float):
        self.muscles.energy_demand *= 2
        self.heart.pumping_rate = min(180, self.heart.pumping_rate * 1.5)
        self.lungs.respiratory_rate = min(30, self.lungs.respiratory_rate * 1.5)
        self.blood.epinephrine_amount = min(2000 * (self.blood.volume / 1000), self.blood.epinephrine_amount * 1.5)

    def start_exercise(self):
        self.is_exercising = True

    def stop_exercise(self):
        self.is_exercising = False
        self.muscles.energy_demand /= 2
        self.heart.pumping_rate = 60
        self.lungs.respiratory_rate = 12
        self.blood.epinephrine_amount = 250

    def drink(self, water_amount: float):
        self.stomach.receive_water(water_amount)

    def eat(self, food_amount: float):
        self.stomach.receive_food(food_amount)

    def pee(self):
        self.bladder.urinate()
