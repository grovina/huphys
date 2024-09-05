from model.blood import Blood
from model.heart import Heart
from model.kidneys import Kidneys
from model.lungs import Lungs
from model.muscles import Muscles
from model.organ import Organ


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
        self.urine_production_signal = 0  # New attribute to signal kidneys
        self.respiratory_rate_signal = 0  # New attribute to signal lungs

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
        baroreceptor_sensitivity = 1.0
        target_map = 90  # mmHg (mean arterial pressure)
        map_error = self.blood.mean_arterial_pressure - target_map

        # Baroreceptor reflex
        baroreceptor_response = baroreceptor_sensitivity * map_error * 0.01

        # Adjust heart rate
        if self.heart:
            self.heart.receive_brain_signal(-baroreceptor_response)

        # Update epinephrine level
        if map_error < -5:
            self.blood.epinephrine_amount *= 1 + 0.01 * dt
        elif map_error > 5:
            self.blood.epinephrine_amount *= 1 - 0.01 * dt

        # Adjust urine production signal
        if map_error > 5:
            self.urine_production_signal = min(1, self.urine_production_signal + 0.1 * dt)
        elif map_error < -5:
            self.urine_production_signal = max(-1, self.urine_production_signal - 0.1 * dt)
        else:
            self.urine_production_signal *= 0.9  # Gradually return to neutral

        # Send signal to kidneys
        if self.kidneys:
            self.kidneys.receive_brain_signal(self.urine_production_signal)

    def _regulate_respiratory_rate(self, dt: float):
        if self.lungs:
            target_pco2 = 40  # mmHg
            pco2_error = self.blood.pco2 - target_pco2

            # Adjust respiratory rate signal
            if pco2_error > 0.02:
                self.respiratory_rate_signal = min(1, self.respiratory_rate_signal + 0.02 * dt)
            elif pco2_error < -0.02:
                self.respiratory_rate_signal = max(-1, self.respiratory_rate_signal - 0.02 * dt)
            else:
                self.respiratory_rate_signal *= 0.9  # Gradually return to neutral

            # Send signal to lungs
            self.lungs.receive_brain_signal(self.respiratory_rate_signal)

    def _regulate_glucose(self, dt: float):
        if self.blood.glucose_concentration < 72:
            # Stimulate glucagon release
            self.blood.glucagon_amount += 0.01 * dt * (self.blood.volume / 1000)
            # Increase epinephrine to stimulate glucose release
            self.blood.epinephrine_amount *= 1 + 0.001 * dt
        elif self.blood.glucose_concentration > 130:
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
            self.muscles.increase_energy_demand(3)

    def stop_exercise(self):
        if self.muscles:
            self.muscles.reset_energy_demand()

    def _organ_specific_metrics(self) -> dict:
        return {
            "urine_production_signal": {"value": self.urine_production_signal, "unit": "", "normal_range": (-1, 1)},
            "respiratory_rate_signal": {"value": self.respiratory_rate_signal, "unit": "", "normal_range": (-1, 1)}
        }
