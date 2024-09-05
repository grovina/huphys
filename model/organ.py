from model.blood import Blood


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
        
        # Reduce insulin in the blood as it's used
        insulin_used = glucose_uptake * 0.001  # Assume 1 unit of insulin per 1000 mg of glucose
        self.blood.insulin_amount = max(0, self.blood.insulin_amount - insulin_used)

    def _organ_specific_processing(self, dt: float) -> None:
        # To be overridden by subclasses
        pass

    def update(self, dt: float):
        self.consume_nutrients(dt)
        self.process_insulin(dt)
        self._organ_specific_processing(dt)
