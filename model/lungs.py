import math

from model.blood import Blood
from model.organ import Organ


class Lungs(Organ):
    def __init__(self, blood: Blood):
        super().__init__(
            blood=blood,
            energy_demand=5,  # kcal/hour
            insulin_sensitivity=1.0  # dimensionless
        )
        self.tidal_volume: float = 500  # mL
        self.respiratory_rate: float = 12  # breaths per minute
        self.alveolar_po2: float = 100  # mmHg
        self.alveolar_pco2: float = 40  # mmHg
        self.diffusion_capacity_o2: float = 21  # mL/min/mmHg
        self.diffusion_capacity_co2: float = 420  # mL/min/mmHg
        self.expansion: float = 0  # dimensionless, ranges from 0 (fully exhaled) to 1 (fully inhaled)
        self.previous_expansion: float = 0  # to track expansion delta
        self.time_since_last_breath: float = 0  # seconds
        self.functional_residual_capacity: float = 2500  # mL
        self.dead_space_volume: float = 150  # mL

    @property
    def alveolar_volume(self):
        return self.functional_residual_capacity + (self.tidal_volume * self.expansion)

    def _organ_specific_processing(self, dt: float) -> None:
        self._update_expansion(dt)
        self._produce_surfactant(dt)
        self._simulate_gas_exchange(dt)

    def _update_expansion(self, dt: float):
        self.time_since_last_breath = (self.time_since_last_breath + dt) % (60 / self.respiratory_rate)  # seconds
        self.previous_expansion = self.expansion
        breath_phase = self.time_since_last_breath / (60 / self.respiratory_rate)
        
        # Sinusoidal function for continuous breathing motion
        self.expansion = 0.5 * (1 + math.sin(2 * math.pi * breath_phase - math.pi / 2))

        volume_delta = self.tidal_volume * (self.expansion - self.previous_expansion)

        # Fresh air composition when it comes to alveoli
        fresh_o2 = 104  # mmHg
        fresh_co2 = 36  # mmHg

        if volume_delta > 0:  # Inhaling
            # Mix fresh air with existing alveolar air
            fresh_fraction = volume_delta / self.alveolar_volume
            self.alveolar_po2 = (1 - fresh_fraction) * self.alveolar_po2 + fresh_fraction * fresh_o2
            self.alveolar_pco2 = (1 - fresh_fraction) * self.alveolar_pco2 + fresh_fraction * fresh_co2
        else:  # Exhaling
            # No change in gas concentrations during exhalation
            pass

    def _produce_surfactant(self, dt: float):
        pass

    def _simulate_gas_exchange(self, dt: float):
        # O2 exchange
        blood_po2 = self.oxygen_hemoglobin_dissociation(self.blood.oxygen_saturation * 100)
        diffusable_o2 = 0.0446 * (self.alveolar_po2 - blood_po2) * self.diffusion_capacity_o2 * dt / 60
        diffused_o2 = min(max(diffusable_o2, 0), self.blood.total_oxygen_capacity - self.blood.o2_amount)
        self.blood.o2_amount += diffused_o2
        self.alveolar_po2 -= diffused_o2 * 760 / (22.4 * self.alveolar_volume / 1000)

        # CO2 exchange
        blood_pco2 = max(self.blood.co2_concentration / 0.03, 1e-6)
        diffusable_co2 = 0.0446 * (blood_pco2 - self.alveolar_pco2) * self.diffusion_capacity_co2 * dt / 60
        diffused_co2 = min(max(diffusable_co2, 0), self.blood.co2_amount)
        self.blood.co2_amount -= diffused_co2
        self.alveolar_pco2 += diffused_co2 * 760 / (22.4 * self.alveolar_volume / 1000)

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

    def receive_brain_signal(self, signal: float):
        # Adjust respiratory rate based on brain signal
        self.respiratory_rate = 12 * (1 + signal * 0.6)
        
        # Adjust tidal volume inversely
        extra_tidal_volume = 500 * signal * 0.1
        self.tidal_volume = 500 - extra_tidal_volume
        self.functional_residual_capacity = 2500 + extra_tidal_volume
        
        # Ensure rates stay within physiological limits
        self.respiratory_rate = max(8, min(30, self.respiratory_rate))
        self.tidal_volume = max(300, min(800, self.tidal_volume))
