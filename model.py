import math


class Blood:
    def __init__(self, volume: float = 5000):
        self.volume: float = volume
        self.glucose_amount: float = 4000 * (volume / 5000)  # mg
        self.fatty_acid_amount: float = 450 * (volume / 5000)  # mg
        self.amino_acid_amount: float = 200 * (volume / 5000)  # mg
        self.epinephrine_amount: float = 0.05 * (volume / 5000)  # ng
        self.insulin_amount: float = 30 * (volume / 5000)  # μU
        self.glucagon_amount: float = 80 * (volume / 5000) * 3.33  # pmol (1 ng = 3.33 pmol)
        self.bicarbonate_amount: float = 24 * (volume / 1000)  # mmol
        self.systolic_pressure: float = 120  # mmHg
        self.diastolic_pressure: float = 80  # mmHg
        self.ph: float = 7.4  # dimensionless
        self.hematocrit: float = 45  # percentage
        self.hemoglobin: float = 15  # g/dL
        self.triglyceride_amount: float = 4000 * (volume / 5000)  # mg
        self.cholesterol_amount: float = 5000 * (volume / 5000)  # mg
        self.phospholipid_amount: float = 5000 * (volume / 5000)  # mg
        self.o2_amount: float = 1000 * (volume / 5000)  # mmol
        self.co2_amount: float = 6 * (volume / 5000)  # mmol
        self.gastrin_amount: float = 0  # ng
        self.ghrelin_amount: float = 0  # ng
        self.cholecystokinin_amount: float = 0  # ng
        self.secretin_amount: float = 0  # ng
        self.urea_amount: float = 300 * (volume / 5000)  # mg
        self.creatinine_amount: float = 10 * (volume / 5000)  # mg
        self.sodium_amount: float = 140 * (volume / 5000)  # mmol
        self.potassium_amount: float = 4 * (volume / 5000)  # mmol
        self.calcium_amount: float = 10 * (volume / 5000)  # mg/dL
        self.phosphate_amount: float = 3.5 * (volume / 5000)  # mg/dL
        self.renin_amount: float = 1 * (volume / 5000)  # ng/mL/h
        self.erythropoietin_amount: float = 10 * (volume / 5000)  # mIU/mL
        self.inactive_vitamin_d_amount: float = 25 * (volume / 5000)  # ng/mL
        self.active_vitamin_d_amount: float = 5 * (volume / 5000)  # ng/mL

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
    def insulin_concentration(self):
        return self.insulin_amount / (self.volume / 1000)  # μU/mL

    @property
    def glucagon_concentration(self):
        return self.glucagon_amount / (self.volume / 1000)  # pmol/L

    @property
    def bicarbonate_concentration(self):
        return self.bicarbonate_amount / (self.volume / 1000)  # mmol/L

    @property
    def plasma_volume(self):
        return self.volume * (1 - self.hematocrit / 100)  # mL

    @property
    def mean_arterial_pressure(self):
        return (self.systolic_pressure + 2 * self.diastolic_pressure) / 3

    @property
    def triglyceride_concentration(self):
        return self.triglyceride_amount / (self.volume / 100)  # mg/dL

    @property
    def cholesterol_concentration(self):
        return self.cholesterol_amount / (self.volume / 100)  # mg/dL

    @property
    def phospholipid_concentration(self):
        return self.phospholipid_amount / (self.volume / 100)  # mg/dL

    @property
    def total_oxygen_capacity(self):
        return self.hemoglobin * 1.34 * (self.volume / 100)  # mL O2

    @property
    def oxygen_saturation(self):
        return self.o2_amount / self.total_oxygen_capacity

    @property
    def secretin_concentration(self):
        return self.secretin_amount / (self.volume / 1000)  # ng/mL

    @property
    def urea_concentration(self):
        return self.urea_amount / (self.volume / 100)  # mg/dL

    @property
    def creatinine_concentration(self):
        return self.creatinine_amount / (self.volume / 100)  # mg/dL

    @property
    def sodium_concentration(self):
        return self.sodium_amount / (self.volume / 1000)  # mmol/L

    @property
    def potassium_concentration(self):
        return self.potassium_amount / (self.volume / 1000)  # mmol/L

    def get_metrics(self) -> dict:
        return {
            "glucose_concentration": {"value": self.glucose_concentration, "unit": "mg/dL", "normal_range": (70, 140)},
            "systolic_pressure": {"value": self.systolic_pressure, "unit": "mmHg", "normal_range": (90, 140)},
            "diastolic_pressure": {"value": self.diastolic_pressure, "unit": "mmHg", "normal_range": (60, 90)},
            "mean_arterial_pressure": {"value": self.mean_arterial_pressure, "unit": "mmHg", "normal_range": (70, 100)},
            "co2_concentration": {"value": self.co2_concentration, "unit": "mmol/L", "normal_range": (1.1, 1.5)},
            "epinephrine_concentration": {"value": self.epinephrine_concentration, "unit": "ng/mL", "normal_range": (0, 0.1)},
            "ph": {"value": self.ph, "unit": "", "normal_range": (7.35, 7.45)},
            "hematocrit": {"value": self.hematocrit, "unit": "%", "normal_range": (37, 52)},
            "plasma_volume": {"value": self.plasma_volume, "unit": "mL", "normal_range": (2700, 3300)},
            "volume": {"value": self.volume, "unit": "mL", "normal_range": (4500, 5500)},
            "insulin_concentration": {"value": self.insulin_concentration, "unit": "μU/mL", "normal_range": (2, 25)},
            "glucagon_concentration": {"value": self.glucagon_concentration, "unit": "pmol/L", "normal_range": (53, 60)},
            "hemoglobin": {"value": self.hemoglobin, "unit": "g/dL", "normal_range": (12, 16)},
            "oxygen_saturation": {"value": self.oxygen_saturation, "unit": "", "normal_range": (0.95, 1.0)},
            "bicarbonate_concentration": {"value": self.bicarbonate_concentration, "unit": "mmol/L", "normal_range": (22, 26)},
            "triglyceride_concentration": {"value": self.triglyceride_concentration, "unit": "mg/dL", "normal_range": (50, 150)},
            "cholesterol_concentration": {"value": self.cholesterol_concentration, "unit": "mg/dL", "normal_range": (100, 200)},
            "phospholipid_concentration": {"value": self.phospholipid_concentration, "unit": "mg/dL", "normal_range": (50, 150)},
            "gastrin_amount": {"value": self.gastrin_amount, "unit": "ng", "normal_range": (0, 100)},
            "ghrelin_amount": {"value": self.ghrelin_amount, "unit": "ng", "normal_range": (0, 100)},
            "cholecystokinin_amount": {"value": self.cholecystokinin_amount, "unit": "ng", "normal_range": (0, 100)},
            "secretin_amount": {"value": self.secretin_amount, "unit": "ng", "normal_range": (0, 100)},
            "secretin_concentration": {"value": self.secretin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "urea_concentration": {"value": self.urea_concentration, "unit": "mg/dL", "normal_range": (7, 20)},
            "creatinine_concentration": {"value": self.creatinine_concentration, "unit": "mg/dL", "normal_range": (0.6, 1.2)},
            "sodium_concentration": {"value": self.sodium_concentration, "unit": "mmol/L", "normal_range": (135, 145)},
            "potassium_concentration": {"value": self.potassium_concentration, "unit": "mmol/L", "normal_range": (3.5, 5.0)},
            "calcium_amount": {"value": self.calcium_amount, "unit": "mg/dL", "normal_range": (8.5, 10.5)},
            "phosphate_amount": {"value": self.phosphate_amount, "unit": "mg/dL", "normal_range": (2.5, 4.5)},
            "renin_amount": {"value": self.renin_amount, "unit": "ng/mL/h", "normal_range": (0.5, 2.0)},
            "erythropoietin_amount": {"value": self.erythropoietin_amount, "unit": "mIU/mL", "normal_range": (4, 20)},
            "inactive_vitamin_d_amount": {"value": self.inactive_vitamin_d_amount, "unit": "ng/mL", "normal_range": (20, 50)},
            "active_vitamin_d_amount": {"value": self.active_vitamin_d_amount, "unit": "ng/mL", "normal_range": (20, 50)},
        }

    def update(self, dt: float):
        self._update_pco2()
        self._update_ph(dt)
        self._update_bicarbonate(dt)

    def _update_pco2(self):
        k = 0.03  # Henry's constant for CO2 in mmol/L/mmHg
        self.pco2 = max(self.co2_concentration / k, 1e-6)  # Ensure pCO2 is not zero

    def _update_ph(self, dt: float):
        new_ph = 6.1 + math.log10(max(self.bicarbonate_concentration, 1e-6) / (0.03 * self.pco2))
        buffer_capacity = 0.1  # Represents the overall buffer capacity of blood
        ph_change = (new_ph - self.ph) * buffer_capacity
        self.ph += ph_change * dt / 60  # Adjust for dt in seconds

    def _update_bicarbonate(self, dt: float):
        bicarbonate_change = (self.ph - 7.4) * 0.5 * dt / 60 * (self.volume / 1000)
        self.bicarbonate_amount = max(self.bicarbonate_amount + bicarbonate_change, 0)

    def degrade_hormones(self, dt: float):
        degradation_rate = 0.01  # 10% degradation per minute
        self.insulin_amount *= (1 - degradation_rate * dt / 60)
        self.glucagon_amount *= (1 - degradation_rate * dt / 60)
        self.epinephrine_amount *= (1 - degradation_rate * dt / 60)
        # Add more hormones as needed


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
        insulin_sensitivity: float = 1.0,  # dimensionless
        glucagon_sensitivity: float = 1.0,  # dimensionless
    ):
        self.blood = blood
        self.energy_demand = energy_demand  # kcal/hour
        self.insulin_sensitivity = insulin_sensitivity  # dimensionless
        self.glucagon_sensitivity = glucagon_sensitivity  # dimensionless
        self.fat_oxidation_rate = 0.1  # fraction of energy from fat

    def _organ_specific_metrics(self) -> dict:
        return {}

    def get_metrics(self) -> dict:
        metrics = {
            "energy_demand": {"value": self.energy_demand, "unit": "kcal/hour", "normal_range": (0, 100)},
            "insulin_sensitivity": {"value": self.insulin_sensitivity, "unit": "", "normal_range": (0.5, 2.0)},
        }
        metrics.update(self._organ_specific_metrics())
        return metrics

    def consume_nutrients(self, dt: float) -> None:
        oxygen_available = self.blood.o2_amount  # mmol O2
        glucose_available = self.blood.glucose_amount  # mg
        fatty_acid_available = self.blood.fatty_acid_amount  # mg
        amino_acid_available = self.blood.amino_acid_amount  # mg
        triglyceride_available = self.blood.triglyceride_amount  # mg
        cholesterol_available = self.blood.cholesterol_amount  # mg
        phospholipid_available = self.blood.phospholipid_amount  # mg
        
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
        
        # Triglyceride consumption
        if energy_demanded > 0:
            triglyceride_energy = min(energy_demanded, triglyceride_available * 9 / 1000)  # 9 kcal/g of triglyceride
            triglyceride_consumed = triglyceride_energy * 1000 / 9  # Convert kcal to mg
            energy_demanded -= triglyceride_energy
        else:
            triglyceride_consumed = 0
        
        # Cholesterol consumption
        if energy_demanded > 0:
            cholesterol_energy = min(energy_demanded, cholesterol_available * 9 / 1000)  # 9 kcal/g of cholesterol
            cholesterol_consumed = cholesterol_energy * 1000 / 9  # Convert kcal to mg
            energy_demanded -= cholesterol_energy
        else:
            cholesterol_consumed = 0
        
        # Phospholipid consumption
        if energy_demanded > 0:
            phospholipid_energy = min(energy_demanded, phospholipid_available * 9 / 1000)  # 9 kcal/g of phospholipid
            phospholipid_consumed = phospholipid_energy * 1000 / 9  # Convert kcal to mg
            energy_demanded -= phospholipid_energy
        else:
            phospholipid_consumed = 0
        
        # Amino acid consumption (last resort)
        if energy_demanded > 0:
            amino_acid_energy = min(energy_demanded, amino_acid_available * 4 / 1000)  # 4 kcal/g of protein
            amino_acid_consumed = amino_acid_energy * 1000 / 4  # Convert kcal to mg
        else:
            amino_acid_consumed = 0
        
        # Calculate total energy from each source
        total_energy = (glucose_consumed * 4 + fatty_acid_consumed * 9 + triglyceride_consumed * 9 + cholesterol_consumed * 9 + phospholipid_consumed * 9 + amino_acid_consumed * 4) / 1000  # kcal
        
        # Calculate respiratory quotient (RQ)
        if total_energy > 0:
            rq = (glucose_consumed * 1.0 + fatty_acid_consumed * 0.7 + triglyceride_consumed * 0.7 + cholesterol_consumed * 0.7 + phospholipid_consumed * 0.7 + amino_acid_consumed * 0.8) / (glucose_consumed + fatty_acid_consumed + triglyceride_consumed + cholesterol_consumed + phospholipid_consumed + amino_acid_consumed)
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
            triglyceride_consumed *= actual_total_energy / total_energy
            cholesterol_consumed *= actual_total_energy / total_energy
            phospholipid_consumed *= actual_total_energy / total_energy
            amino_acid_consumed *= actual_total_energy / total_energy
            total_energy = actual_total_energy
        
        # Calculate CO2 production based on oxygen consumption and RQ
        co2_produced = oxygen_consumed * rq  # mmol CO2
        
        # Update blood CO2 concentration
        self.blood.co2_amount += co2_produced
        
        # Update blood nutrient levels
        self.blood.glucose_amount -= glucose_consumed
        self.blood.fatty_acid_amount -= fatty_acid_consumed
        self.blood.triglyceride_amount -= triglyceride_consumed
        self.blood.cholesterol_amount -= cholesterol_consumed
        self.blood.phospholipid_amount -= phospholipid_consumed
        self.blood.amino_acid_amount -= amino_acid_consumed
        
        # Update blood oxygen levels
        self.blood.o2_amount -= oxygen_consumed

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
            energy_demand=8,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.pumping_rate = 60  # beats per minute
        self.stroke_volume = 70  # mL per beat
        self.ejection_fraction = 0.6  # dimensionless
        self.cardiac_output = 5  # L/min
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
        self.handle_ischemia()
        self.regulate_coronary_blood_flow()

    def handle_ischemia(self):
        # Placeholder for handling reduced blood flow to heart tissue
        pass

    def regulate_coronary_blood_flow(self):
        # Placeholder for regulating blood flow to the heart muscle
        pass
    
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

        # Calculate systolic and diastolic pressure
        self.blood.systolic_pressure = mean_arterial_pressure + (pulse_pressure / 2)
        self.blood.diastolic_pressure = mean_arterial_pressure - (pulse_pressure / 2)

    def adjust_rate(self, factor: float):
        self.pumping_rate = max(40, min(200, self.pumping_rate * factor))  # beats per minute

    def receive_brain_signal(self, signal: float):
        self.adjust_rate(1 + signal * 0.1)

    def _organ_specific_metrics(self) -> dict:
        metrics = super()._organ_specific_metrics()
        metrics.update({
            "pumping_rate": {"value": self.pumping_rate, "unit": "beats/min", "normal_range": (40, 190)},
            "cardiac_output": {"value": self.cardiac_output, "unit": "L/min", "normal_range": (4, 15)},
            "ejection_fraction": {"value": self.ejection_fraction, "unit": "", "normal_range": (0.5, 0.7)},
            "stroke_volume": {"value": self.stroke_volume, "unit": "mL/beat", "normal_range": (60, 100)},
            "systolic_pressure": {"value": self.blood.systolic_pressure, "unit": "mmHg", "normal_range": (90, 140)},
            "diastolic_pressure": {"value": self.blood.diastolic_pressure, "unit": "mmHg", "normal_range": (60, 90)},
            "peripheral_resistance": {"value": self.peripheral_resistance, "unit": "dyn·s/cm^5", "normal_range": (900, 1500)},
            "compression": {"value": self.compression, "unit": "", "normal_range": (0, 1)},
        })
        return metrics

class Lungs(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.tidal_volume = 500  # mL
        self.respiratory_rate = 12  # breaths per minute
        self.alveolar_po2 = 100  # mmHg
        self.alveolar_pco2 = 40  # mmHg
        self.diffusion_capacity_o2 = 21  # mL/min/mmHg
        self.diffusion_capacity_co2 = 420  # mL/min/mmHg
        self.expansion = 0  # dimensionless, ranges from 0 (fully exhaled) to 1 (fully inhaled)
        self.previous_expansion = 0  # to track expansion delta
        self.time_since_last_breath = 0  # seconds
        self.functional_residual_capacity = 2500  # mL
        self.dead_space_volume = 150  # mL

    def _organ_specific_processing(self, dt: float) -> None:
        self.time_since_last_breath += dt
        breath_interval = 60 / self.respiratory_rate  # seconds
        self.time_since_last_breath %= breath_interval

        self._update_expansion(dt)
        self._produce_surfactant(dt)
        self._simulate_gas_exchange(dt)

    def _update_expansion(self, dt: float):
        self.previous_expansion = self.expansion
        breath_phase = self.time_since_last_breath / (60 / self.respiratory_rate)
        
        # Sinusoidal function for continuous breathing motion
        self.expansion = 0.5 * (1 + math.sin(2 * math.pi * breath_phase - math.pi / 2))

    def _produce_surfactant(self, dt: float):
        pass

    def _simulate_gas_exchange(self, dt: float):
        volume_delta = self.tidal_volume * (self.expansion - self.previous_expansion)
        alveolar_volume = self.functional_residual_capacity + (self.tidal_volume * self.expansion)

        # Fresh air composition when it comes to alveoli
        fresh_o2 = 104  # mmHg
        fresh_co2 = 35  # mmHg

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
        diffusable_o2 = 0.0446 * (self.alveolar_po2 - blood_po2) * self.diffusion_capacity_o2 * dt / 60
        diffused_o2 = min(max(diffusable_o2, 0), self.blood.total_oxygen_capacity - self.blood.o2_amount)
        self.blood.o2_amount += diffused_o2
        self.alveolar_po2 -= diffused_o2 * 760 / (22.4 * alveolar_volume / 1000)

        # CO2 exchange
        blood_pco2 = max(self.blood.co2_concentration / 0.03, 1e-6)
        diffusable_co2 = 0.0446 * (blood_pco2 - self.alveolar_pco2) * self.diffusion_capacity_co2 * dt / 60
        diffused_co2 = min(max(diffusable_co2, 0), self.blood.co2_amount)
        self.blood.co2_amount -= diffused_co2
        self.alveolar_pco2 += diffused_co2 * 760 / (22.4 * alveolar_volume / 1000)

    def oxygen_hemoglobin_dissociation(self, po2: float) -> float:
        return 100 * (po2**2.8) / (po2**2.8 + 26**2.8)

    def _organ_specific_metrics(self) -> dict:
        return {
            "tidal_volume": {"value": self.tidal_volume, "unit": "mL", "normal_range": (400, 600)},
            "respiratory_rate": {"value": self.respiratory_rate, "unit": "breaths/min", "normal_range": (12, 20)},
            "alveolar_po2": {"value": self.alveolar_po2, "unit": "mmHg", "normal_range": (95, 105)},
            "alveolar_pco2": {"value": self.alveolar_pco2, "unit": "mmHg", "normal_range": (35, 45)},
            "expansion": {"value": self.expansion, "unit": "", "normal_range": (0, 1)},
            "alveolar_volume": {"value": self.functional_residual_capacity + (self.tidal_volume * self.expansion), "unit": "mL", "normal_range": (2000, 3000)},
            "minute_ventilation": {"value": self.tidal_volume * self.respiratory_rate / 1000, "unit": "L/min", "normal_range": (5, 8)},
            "alveolar_ventilation": {"value": (self.tidal_volume - self.dead_space_volume) * self.respiratory_rate / 1000, "unit": "L/min", "normal_range": (4, 6)}
        }

class Kidneys(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=6,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.glomerular_filtration_rate = 125  # mL/min
        self.tubular_reabsorption_rate = 124  # mL/min
        self.urine_production_rate = 1  # mL/min
        self.sodium_reabsorption_rate = 99.5  # percentage
        self.potassium_secretion_rate = 0.1  # mmol/min
        self.urea_clearance_rate = 70  # mL/min
        self.creatinine_clearance_rate = 125  # mL/min
        self.phosphate_reabsorption_rate = 85  # percentage
        self.calcium_reabsorption_rate = 98  # percentage
        self.vitamin_d_activation_rate = 0.1  # ng/mL/hour
        self.erythropoietin_production_rate = 0.1  # mIU/mL/hour
        self.renin_production_rate = 0.1  # ng/mL/h/hour
        self.bladder = None

    def set_bladder(self, bladder):
        self.bladder = bladder

    def _organ_specific_processing(self, dt: float) -> None:
        self._filter_blood(dt)
        self._regulate_electrolytes(dt)
        self._regulate_acid_base_balance(dt)
        self._produce_hormones(dt)
        self._activate_vitamin_d(dt)
        self._produce_prostaglandins(dt)

    def _filter_blood(self, dt: float):
        filtered_volume = self.glomerular_filtration_rate * dt / 60  # mL
        reabsorbed_volume = self.tubular_reabsorption_rate * dt / 60  # mL
        urine_volume = filtered_volume - reabsorbed_volume

        # Update blood volume
        self.blood.volume -= urine_volume

        # Filter and clear urea and creatinine
        urea_cleared = self.urea_clearance_rate * dt / 60 * self.blood.urea_concentration
        creatinine_cleared = self.creatinine_clearance_rate * dt / 60 * self.blood.creatinine_concentration
        self.blood.urea_amount -= urea_cleared
        self.blood.creatinine_amount -= creatinine_cleared

        # Update urine production rate and total urine produced
        self.urine_production_rate = urine_volume / (dt / 60)
        if self.bladder:
            self.bladder.receive_urine(urine_volume)

    def _regulate_electrolytes(self, dt: float):
        # Sodium regulation
        sodium_filtered = self.glomerular_filtration_rate * dt / 60 * self.blood.sodium_concentration
        sodium_reabsorbed = sodium_filtered * self.sodium_reabsorption_rate / 100
        self.blood.sodium_amount -= (sodium_filtered - sodium_reabsorbed)

        # Potassium regulation
        potassium_secreted = self.potassium_secretion_rate * dt / 60
        self.blood.potassium_amount -= potassium_secreted

        # Calcium and Phosphate regulation
        calcium_filtered = self.glomerular_filtration_rate * dt / 60 * self.blood.calcium_amount / 100
        calcium_reabsorbed = calcium_filtered * self.calcium_reabsorption_rate / 100
        self.blood.calcium_amount -= (calcium_filtered - calcium_reabsorbed)

        phosphate_filtered = self.glomerular_filtration_rate * dt / 60 * self.blood.phosphate_amount / 100
        phosphate_reabsorbed = phosphate_filtered * self.phosphate_reabsorption_rate / 100
        self.blood.phosphate_amount -= (phosphate_filtered - phosphate_reabsorbed)

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

    def calculate_gfr(self):
        base_gfr = 125  # mL/min
        map_effect = (self.blood.mean_arterial_pressure - 90) * 0.5  # 0.5 mL/min per mmHg above 90
        hematocrit_effect = (self.blood.hematocrit - 45) * -1  # -1 mL/min per % above 45
        self.glomerular_filtration_rate = max(60, min(180, base_gfr + map_effect + hematocrit_effect))

    def _organ_specific_metrics(self) -> dict:
        return {
            "glomerular_filtration_rate": {"value": self.glomerular_filtration_rate, "unit": "mL/min", "normal_range": (90, 120)},
            "urine_production_rate": {"value": self.urine_production_rate, "unit": "mL/min", "normal_range": (0.5, 2)},
            "sodium_reabsorption_rate": {"value": self.sodium_reabsorption_rate, "unit": "%", "normal_range": (98, 99.5)},
            "potassium_secretion_rate": {"value": self.potassium_secretion_rate, "unit": "mmol/min", "normal_range": (0.05, 0.15)},
            "urea_clearance_rate": {"value": self.urea_clearance_rate, "unit": "mL/min", "normal_range": (60, 80)},
            "creatinine_clearance_rate": {"value": self.creatinine_clearance_rate, "unit": "mL/min", "normal_range": (90, 130)},
            "vitamin_d_activation_rate": {"value": self.vitamin_d_activation_rate, "unit": "ng/mL/hour", "normal_range": (0.05, 0.2)},
        }

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

class Bones(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=1,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.calcium_content = 1000  # g

    def _organ_specific_processing(self, dt: float) -> None:
        self._store_minerals(dt)
        self._produce_blood_cells(dt)

    def _store_minerals(self, dt: float):
        # Placeholder for storing minerals (calcium, phosphate)
        pass

    def _produce_blood_cells(self, dt: float):
        # Placeholder for producing blood cells (hematopoiesis)
        pass

    def _organ_specific_metrics(self) -> dict:
        return {
            "calcium_content": {"value": self.calcium_content, "unit": "g", "normal_range": (900, 1100)},
        }

class Brain(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=11,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.lungs = None  # Will be set by the HumanBody class
        self.heart = None  # Will be set by the HumanBody class
        self.kidneys = None  # Will be set by the HumanBody class
        self.muscles = None  # Will be set by the HumanBody class

    def _organ_specific_processing(self, dt: float) -> None:
        self._regulate_blood_pressure(dt)
        self._regulate_respiratory_rate(dt)
        self._regulate_glucose(dt)
        self._regulate_body_temperature(dt)
        self._process_sensory_input(dt)
        self._control_motor_functions(dt)
        self._regulate_sleep_wake_cycle(dt)
        self._regulate_cerebrospinal_fluid(dt)
        self._regulate_appetite(dt)
        self._regulate_endocrine_system(dt)

    def _regulate_body_temperature(self, dt: float):
        # Placeholder for regulating body temperature
        pass

    def _process_sensory_input(self, dt: float):
        # Placeholder for processing sensory input
        pass

    def _control_motor_functions(self, dt: float):
        # Placeholder for controlling motor functions
        pass

    def _regulate_sleep_wake_cycle(self, dt: float):
        # Placeholder for regulating sleep-wake cycle
        pass

    def _regulate_cerebrospinal_fluid(self, dt: float):
        # Placeholder for regulating cerebrospinal fluid production and circulation
        pass

    def _regulate_appetite(self, dt: float):
        # Placeholder for regulating appetite
        pass

    def _regulate_endocrine_system(self, dt: float):
        # Placeholder for regulating endocrine system
        pass

    def _regulate_blood_pressure(self, dt: float):
        baroreceptor_sensitivity = 1.0  # dimensionless
        target_map = 93  # mmHg (mean arterial pressure)
        map_error = self.blood.mean_arterial_pressure - target_map

        # Baroreceptor reflex
        baroreceptor_response = baroreceptor_sensitivity * map_error * 0.01

        # Adjust heart rate
        if self.heart:
            self.heart.receive_brain_signal(-baroreceptor_response)

        # Adjust peripheral resistance
        resistance_change = max(-0.1, min(0.1, baroreceptor_response * 0.5))
        if self.heart:
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

    def _regulate_respiratory_rate(self, dt: float):
        if self.lungs:
            if self.blood.co2_concentration > 1.5:  # mmol/L
                self.lungs.respiratory_rate = self.lungs.respiratory_rate + 0.5 * dt
            elif self.blood.co2_concentration < 1.1:  # mmol/L
                self.lungs.respiratory_rate = max(self.lungs.respiratory_rate - 0.5 * dt, 1e-6)
            else:
                # Gradually return to normal respiratory rate
                normal_rate = 12
                if self.lungs.respiratory_rate > normal_rate:
                    self.lungs.respiratory_rate = max(self.lungs.respiratory_rate - 0.1 * dt, 1e-6)
                elif self.lungs.respiratory_rate < normal_rate:
                    self.lungs.respiratory_rate = self.lungs.respiratory_rate + 0.1 * dt

    def _regulate_glucose(self, dt: float):
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

    def set_muscles(self, muscles: Muscles):
        self.muscles = muscles

    def start_exercise(self):
        if self.muscles:
            self.muscles.increase_energy_demand(2)  # Double the energy demand

    def stop_exercise(self):
        if self.muscles:
            self.muscles.reset_energy_demand()

    def _organ_specific_metrics(self) -> dict:
        return {
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
            "absorption_rate": {"value": self.absorption_rate, "unit": "", "normal_range": (0.1, 0.3)},
            "carbohydrate_content": {"value": self.carbohydrate_content, "unit": "g", "normal_range": (0, 1000)},
            "protein_content": {"value": self.protein_content, "unit": "g", "normal_range": (0, 1000)},
            "fat_content": {"value": self.fat_content, "unit": "g", "normal_range": (0, 1000)},
            "fiber_content": {"value": self.fiber_content, "unit": "g", "normal_range": (0, 1000)},
            "water_content": {"value": self.water_content, "unit": "mL", "normal_range": (0, 1000)},
            "bile_content": {"value": self.bile_content, "unit": "mL", "normal_range": (0, 50)}
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

class Thyroid(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=0,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )

    def _organ_specific_processing(self, dt: float) -> None:
        self._produce_hormones(dt)

    def _produce_hormones(self, dt: float):
        # Placeholder for producing thyroid hormones (T3, T4)
        pass

    def _organ_specific_metrics(self) -> dict:
        return {}

class Skin(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=2,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )

    def _organ_specific_processing(self, dt: float) -> None:
        self._regulate_temperature(dt)
        self._produce_vitamin_d(dt)
        self._sense_environment(dt)
        self._regulate_water_loss(dt)

    def _regulate_temperature(self, dt: float) -> None:
        # Placeholder for temperature regulation
        pass

    def _produce_vitamin_d(self, dt: float) -> None:
        # Placeholder for vitamin D production
        pass

    def _sense_environment(self, dt: float) -> None:
        # Placeholder for sensory function
        pass

    def _regulate_water_loss(self, dt: float) -> None:
        # Placeholder for water regulation
        pass

    def _organ_specific_metrics(self) -> dict:
        return {}


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


class Spleen(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=1,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.blood_storage = 200  # mL

    def _organ_specific_processing(self, dt: float) -> None:
        # Spleen-specific blood processing logic
        pass

    def _organ_specific_metrics(self) -> dict:
        return {"blood_storage": {"value": self.blood_storage, "unit": "mL", "normal_range": (100, 300)}}


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
            "urine_volume": {"value": self.urine_volume, "unit": "mL", "normal_range": (0, self.max_capacity)},
            "fullness_percentage": {"value": (self.urine_volume / self.max_capacity) * 100, "unit": "%", "normal_range": (0, 100)}
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
        self.muscles = Muscles(self.blood)
        self.pancreas = Pancreas(self.blood)
        self.fat = Fat(self.blood)
        self.stomach = Stomach(self.blood)
        self.intestines = Intestines(self.blood)
        self.skin = Skin(self.blood)
        self.spleen = Spleen(self.blood)
        self.bladder = Bladder(self.blood)
        self.gall_bladder = GallBladder(self.blood)

        # Connect brain to lungs, heart, and muscles
        self.brain.set_lungs(self.lungs)
        self.brain.set_heart(self.heart)
        self.brain.set_kidneys(self.kidneys)
        self.brain.set_muscles(self.muscles)

        # Connect kidneys to bladder
        self.kidneys.set_bladder(self.bladder)

        # Connect liver to gall bladder
        self.liver.set_gall_bladder(self.gall_bladder)

        # Connect gall bladder to intestines
        self.gall_bladder.set_intestines(self.intestines)

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
            self.intestines, self.skin, self.spleen, self.bladder, self.gall_bladder
        ]
        
        total_energy_expenditure = 0
        for organ in organs:
            organ.update(dt)
            total_energy_expenditure += organ.energy_demand * (dt / 3600)  # Convert to kcal/step
        
        self.total_caloric_expenditure += total_energy_expenditure
        
        self.blood.update(dt)
        
        self.maintain_homeostasis(dt)
        
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
            "GallBladder": self.gall_bladder,
        }
        
        for organ_name, organ in organs.items():
            metrics["Organs"][organ_name] = organ.get_metrics()
        
        return metrics

    def drink(self, water_amount: float):
        self.stomach.receive_water(water_amount)

    def eat(self, food_amount: float):
        self.stomach.receive_food(carbs=food_amount)

    def pee(self):
        self.bladder.urinate()
