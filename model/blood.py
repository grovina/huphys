import math


class Blood:
    def __init__(self, volume: float = 5000):
        self.volume: float = volume
        self.glucose_amount: float = 80 * (volume / 100)  # mg
        self.fatty_acid_amount: float = 90 * (volume / 1000)  # mg
        self.amino_acid_amount: float = 40 * (volume / 1000)  # mg
        self.epinephrine_amount: float = 8 * (volume / 1000)  # pg
        self.insulin_amount: float = 6 * (volume / 1000)  # μU
        self.glucagon_amount: float = 16 * (volume / 1000) * 3.33  # pmol (1 ng = 3.33 pmol)
        self.bicarbonate_amount: float = 24 * (volume / 1000)  # mmol
        self.systolic_pressure: float = 120  # mmHg
        self.diastolic_pressure: float = 80  # mmHg
        self.ph: float = 7.4  # dimensionless
        self.hematocrit: float = 45  # percentage
        self.hemoglobin: float = 15  # g/dL
        self.triglyceride_amount: float = 800 * (volume / 1000)  # mg
        self.cholesterol_amount: float = 1000 * (volume / 1000)  # mg
        self.phospholipid_amount: float = 1000 * (volume / 1000)  # mg
        self.o2_amount: float = 200 * (volume / 1000)  # mmol
        self.co2_amount: float = 1.25 * (volume / 1000)  # mmol
        self.gastrin_amount: float = 0  # ng
        self.ghrelin_amount: float = 0  # ng
        self.cholecystokinin_amount: float = 0  # ng
        self.secretin_amount: float = 0  # ng
        self.urea_amount: float = 60 * (volume / 1000)  # mg
        self.creatinine_amount: float = 1.0 * (volume / 100)  # mg
        self.sodium_amount: float = 140 * (volume / 1000)  # mmol
        self.potassium_amount: float = 4 * (volume / 1000)  # mmol
        self.calcium_amount: float = 2.5 * (volume / 1000)  # mmol
        self.phosphate_amount: float = 3.5 * (volume / 100)  # mg
        self.renin_amount: float = 1.0 * (volume / 1000)  # ng
        self.erythropoietin_amount: float = 5 * (volume / 1000)  # mIU
        self.inactive_vitamin_d_amount: float = 30 * (volume / 1000)  # ng
        self.active_vitamin_d_amount: float = 30 * (volume / 1000)  # ng

    @property
    def glucose_concentration(self):
        return self.glucose_amount / (self.volume / 100)  # mg/dL

    @property
    def co2_concentration(self):
        return self.co2_amount / (self.volume / 1000)  # mmol/L

    @property
    def epinephrine_concentration(self):
        return self.epinephrine_amount / (self.volume / 1000)  # pg/mL

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
    def calcium_concentration(self):
        return self.calcium_amount / (self.volume / 1000)  # mmol/L

    @property
    def sodium_concentration(self):
        return self.sodium_amount / (self.volume / 1000)  # mmol/L

    @property
    def potassium_concentration(self):
        return self.potassium_amount / (self.volume / 1000)  # mmol/L

    @property
    def phosphate_concentration(self):
        return self.phosphate_amount / (self.volume / 100)  # mg/dL

    @property
    def gastrin_concentration(self):
        return self.gastrin_amount / (self.volume / 1000)  # ng/mL

    @property
    def ghrelin_concentration(self):
        return self.ghrelin_amount / (self.volume / 1000)  # ng/mL

    @property
    def cholecystokinin_concentration(self):
        return self.cholecystokinin_amount / (self.volume / 1000)  # ng/mL

    @property
    def renin_concentration(self):
        return self.renin_amount / (self.volume / 1000)  # ng/mL

    @property
    def erythropoietin_concentration(self):
        return self.erythropoietin_amount / (self.volume / 1000)  # mIU/mL

    @property
    def inactive_vitamin_d_concentration(self):
        return self.inactive_vitamin_d_amount / (self.volume / 1000)  # ng/mL

    @property
    def active_vitamin_d_concentration(self):
        return self.active_vitamin_d_amount / (self.volume / 1000)  # ng/mL

    @property
    def pco2(self):
        k = 0.03  # Henry's constant for CO2 in mmol/L/mmHg
        return max(self.co2_concentration / k, 1e-6)  # Ensure pCO2 is not zero

    def get_metrics(self) -> dict:
        return {
            "glucose_concentration": {"value": self.glucose_concentration, "unit": "mg/dL", "normal_range": (70, 140)},
            "systolic_pressure": {"value": self.systolic_pressure, "unit": "mmHg", "normal_range": (90, 140)},
            "diastolic_pressure": {"value": self.diastolic_pressure, "unit": "mmHg", "normal_range": (60, 90)},
            "mean_arterial_pressure": {"value": self.mean_arterial_pressure, "unit": "mmHg", "normal_range": (70, 100)},
            "co2_concentration": {"value": self.co2_concentration, "unit": "mmol/L", "normal_range": (1.1, 1.5)},
            "epinephrine_concentration": {"value": self.epinephrine_concentration, "unit": "pg/mL", "normal_range": (0, 140)},
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
            "gastrin_concentration": {"value": self.gastrin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "ghrelin_concentration": {"value": self.ghrelin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "cholecystokinin_concentration": {"value": self.cholecystokinin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "secretin_concentration": {"value": self.secretin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "urea_concentration": {"value": self.urea_concentration, "unit": "mg/dL", "normal_range": (5, 20)},
            "creatinine_concentration": {"value": self.creatinine_concentration, "unit": "mg/dL", "normal_range": (0.6, 1.2)},
            "sodium_concentration": {"value": self.sodium_concentration, "unit": "mmol/L", "normal_range": (135, 145)},
            "potassium_concentration": {"value": self.potassium_concentration, "unit": "mmol/L", "normal_range": (3.5, 5.0)},
            "calcium_concentration": {"value": self.calcium_concentration, "unit": "mmol/L", "normal_range": (2.2, 2.7)},
            "phosphate_concentration": {"value": self.phosphate_concentration, "unit": "mg/dL", "normal_range": (2.5, 4.5)},
            "renin_concentration": {"value": self.renin_concentration, "unit": "ng/mL", "normal_range": (0.5, 2.0)},
            "erythropoietin_concentration": {"value": self.erythropoietin_concentration, "unit": "mIU/mL", "normal_range": (4, 20)},
            "inactive_vitamin_d_concentration": {"value": self.inactive_vitamin_d_concentration, "unit": "ng/mL", "normal_range": (20, 50)},
            "active_vitamin_d_concentration": {"value": self.active_vitamin_d_concentration, "unit": "ng/mL", "normal_range": (20, 50)},
            "pco2": {"value": self.pco2, "unit": "mmHg", "normal_range": (35, 45)},
        }

    def update(self, dt: float):
        self._update_ph(dt)
        self._update_bicarbonate(dt)
        self._degrade_hormones(dt)

    def _update_ph(self, dt: float):
        new_ph = 6.1 + math.log10(max(self.bicarbonate_concentration, 1e-6) / (0.03 * self.pco2))
        buffer_capacity = 0.1  # Represents the overall buffer capacity of blood
        ph_change = (new_ph - self.ph) * buffer_capacity
        self.ph += ph_change * dt / 60  # Adjust for dt in seconds

    def _update_bicarbonate(self, dt: float):
        bicarbonate_change = (self.ph - 7.4) * 0.5 * dt / 60 * (self.volume / 1000)
        self.bicarbonate_amount = max(self.bicarbonate_amount + bicarbonate_change, 0)

    def _degrade_hormones(self, dt: float):
        degradation_rate = 0.01  # 1% degradation per minute
        self.insulin_amount *= (1 - degradation_rate * dt / 60)
        self.glucagon_amount *= (1 - degradation_rate * dt / 60)
        self.epinephrine_amount *= (1 - degradation_rate * dt / 60)
        # Add more hormones as needed
