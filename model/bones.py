from model.blood import Blood
from model.organ import Organ


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
