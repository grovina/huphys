from model.blood import Blood
from model.organ import Organ


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
        return {
            "Blood Storage": {"value": self.blood_storage, "unit": "mL", "normal_range": (100, 300)}
        }
