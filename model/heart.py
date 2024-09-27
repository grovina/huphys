import math

from model.blood import Blood
from model.organ import Organ


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
        self.compression = 0  # dimensionless, ranges from 0 (relaxed) to 1 (fully contracted)
        self.base_peripheral_resistance = 1200  # dyn·s/cm^5
        self.peripheral_resistance = self.base_peripheral_resistance

    def _organ_specific_processing(self, dt: float) -> None:
        self._simulate_cardiac_cycle(dt)
        self._regulate_vascular_system(dt)
        self._regulate_coronary_blood_flow(dt)

    def _simulate_cardiac_cycle(self, dt: float):
        self.time_since_last_beat = (self.time_since_last_beat + dt) % (60 / self.pumping_rate)
        beat_phase = self.time_since_last_beat / (60 / self.pumping_rate)

        systole_duration = 0.3  # 30% of the cardiac cycle
        if beat_phase < systole_duration:
            self.compression = math.exp(-((beat_phase - 0.15) / 0.1) ** 2)
        else:
            relaxation_rate = 5 if beat_phase < 0.5 else 1
            self.compression *= math.exp(-relaxation_rate * dt)

    def _regulate_vascular_system(self, dt: float):
        self.cardiac_output = (self.stroke_volume * self.pumping_rate) / 1000  # L/min

        epinephrine_effect = 1 + 0.01 * (self.blood.epinephrine_concentration - 1)
        volume_effect = 1 - 0.01 * (self.blood.volume / 5000 - 1)
        self.peripheral_resistance = self.base_peripheral_resistance * epinephrine_effect * volume_effect

        arterial_compliance = 1.5  # mL/mmHg
        mean_arterial_pressure = (self.cardiac_output * self.peripheral_resistance) / 80
        pulse_pressure = self.stroke_volume / arterial_compliance
        self.blood.systolic_pressure = mean_arterial_pressure + (pulse_pressure / 2)
        self.blood.diastolic_pressure = mean_arterial_pressure - (pulse_pressure / 2)

    def _regulate_coronary_blood_flow(self, dt: float):
        # Placeholder for regulating blood flow to the heart muscle
        pass

    def receive_brain_signal(self, signal: float):
        self.pumping_rate *= 1 + signal * 0.1  # beats per minute

    def _organ_specific_metrics(self) -> dict:
        return {
            "Heart Rate": {"value": self.pumping_rate, "unit": "beats/min", "normal_range": (40, 190)},
            "Cardiac Output": {"value": self.cardiac_output, "unit": "L/min", "normal_range": (4, 15)},
            "Ejection Fraction": {"value": self.ejection_fraction, "unit": "", "normal_range": (0.5, 0.7)},
            "Stroke Volume": {"value": self.stroke_volume, "unit": "mL/beat", "normal_range": (60, 100)},
            "Peripheral Resistance": {"value": self.peripheral_resistance, "unit": "dyn·s/cm^5", "normal_range": (900, 1500)},
            "Myocardial Contraction": {"value": self.compression, "unit": "", "normal_range": (0, 1)},
        }
