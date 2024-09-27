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
        self.ammonia_amount: float = 50 * (volume / 1000)  # μg

    @property
    def glucose_concentration(self):
        return self.glucose_amount / (self.volume / 100)  # mg/dL

    @property
    def fatty_acid_concentration(self):
        return self.fatty_acid_amount / (self.volume / 1000)  # mg/L

    @property
    def amino_acid_concentration(self):
        return self.amino_acid_amount / (self.volume / 1000)  # mg/L

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

    @property
    def ammonia_concentration(self):
        return self.ammonia_amount / (self.volume / 1000)  # μg/L

    def get_metrics(self) -> dict:
        metrics = {
            "Glucose": {"value": self.glucose_concentration, "unit": "mg/dL", "normal_range": (70, 140)},
            "Fatty Acids": {"value": self.fatty_acid_concentration, "unit": "mg/L", "normal_range": (70, 110)},
            "Amino Acids": {"value": self.amino_acid_concentration, "unit": "mg/L", "normal_range": (30, 50)},
            "Systolic Blood Pressure": {"value": self.systolic_pressure, "unit": "mmHg", "normal_range": (90, 140)},
            "Diastolic Blood Pressure": {"value": self.diastolic_pressure, "unit": "mmHg", "normal_range": (60, 90)},
            "Mean Arterial Pressure": {"value": self.mean_arterial_pressure, "unit": "mmHg", "normal_range": (70, 100)},
            "CO2": {"value": self.co2_concentration, "unit": "mmol/L", "normal_range": (1.1, 1.5)},
            "Epinephrine": {"value": self.epinephrine_concentration, "unit": "pg/mL", "normal_range": (0, 140)},
            "pH": {"value": self.ph, "unit": "", "normal_range": (7.35, 7.45)},
            "Hematocrit": {"value": self.hematocrit, "unit": "%", "normal_range": (37, 52)},
            "Plasma Volume": {"value": self.plasma_volume, "unit": "mL", "normal_range": (2700, 3300)},
            "Total Blood Volume": {"value": self.volume, "unit": "mL", "normal_range": (4500, 5500)},
            "Insulin": {"value": self.insulin_concentration, "unit": "μU/mL", "normal_range": (2, 25)},
            "Glucagon": {"value": self.glucagon_concentration, "unit": "pmol/L", "normal_range": (53, 60)},
            "Hemoglobin": {"value": self.hemoglobin, "unit": "g/dL", "normal_range": (12, 16)},
            "Oxygen Saturation": {"value": self.oxygen_saturation, "unit": "", "normal_range": (0.95, 1.0)},
            "Bicarbonate": {"value": self.bicarbonate_concentration, "unit": "mmol/L", "normal_range": (22, 26)},
            "Triglycerides": {"value": self.triglyceride_concentration, "unit": "mg/dL", "normal_range": (50, 150)},
            "Cholesterol": {"value": self.cholesterol_concentration, "unit": "mg/dL", "normal_range": (100, 200)},
            "Phospholipids": {"value": self.phospholipid_concentration, "unit": "mg/dL", "normal_range": (50, 150)},
            "Gastrin": {"value": self.gastrin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "Ghrelin": {"value": self.ghrelin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "Cholecystokinin": {"value": self.cholecystokinin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "Secretin": {"value": self.secretin_concentration, "unit": "ng/mL", "normal_range": (0, 100)},
            "Urea": {"value": self.urea_concentration, "unit": "mg/dL", "normal_range": (5, 20)},
            "Creatinine": {"value": self.creatinine_concentration, "unit": "mg/dL", "normal_range": (0.6, 1.2)},
            "Sodium": {"value": self.sodium_concentration, "unit": "mmol/L", "normal_range": (135, 145)},
            "Potassium": {"value": self.potassium_concentration, "unit": "mmol/L", "normal_range": (3.5, 5.0)},
            "Calcium": {"value": self.calcium_concentration, "unit": "mmol/L", "normal_range": (2.2, 2.7)},
            "Phosphate": {"value": self.phosphate_concentration, "unit": "mg/dL", "normal_range": (2.5, 4.5)},
            "Renin": {"value": self.renin_concentration, "unit": "ng/mL", "normal_range": (0.5, 2.0)},
            "Erythropoietin": {"value": self.erythropoietin_concentration, "unit": "mIU/mL", "normal_range": (4, 20)},
            "Inactive Vitamin D": {"value": self.inactive_vitamin_d_concentration, "unit": "ng/mL", "normal_range": (20, 50)},
            "Active Vitamin D": {"value": self.active_vitamin_d_concentration, "unit": "ng/mL", "normal_range": (20, 50)},
            "pCO2": {"value": self.pco2, "unit": "mmHg", "normal_range": (35, 45)},
            "Ammonia": {"value": self.ammonia_concentration, "unit": "μg/L", "normal_range": (10, 80)},
        }
        return metrics

    def update(self, dt: float):
        self._update_ph(dt)
        self._update_bicarbonate(dt)

    def _update_ph(self, dt: float):
        new_ph = 6.1 + math.log10(max(self.bicarbonate_concentration, 1e-6) / (0.03 * self.pco2))
        buffer_capacity = 0.1  # Represents the overall buffer capacity of blood
        ph_change = (new_ph - self.ph) * buffer_capacity
        self.ph += ph_change * dt / 60  # Adjust for dt in seconds

    def _update_bicarbonate(self, dt: float):
        bicarbonate_change = (self.ph - 7.4) * 0.5 * dt / 60 * (self.volume / 1000)
        self.bicarbonate_amount = max(self.bicarbonate_amount + bicarbonate_change, 0)

