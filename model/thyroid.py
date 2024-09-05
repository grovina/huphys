from model.blood import Blood
from model.organ import Organ


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
