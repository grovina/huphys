from model.blood import Blood
from model.brain import Brain
from model.fat import Fat
from model.heart import Heart
from model.intestines import Intestines
from model.kidneys import Bladder, Kidneys
from model.liver import GallBladder, Liver
from model.lungs import Lungs
from model.muscles import Muscles
from model.pancreas import Pancreas
from model.skin import Skin
from model.spleen import Spleen
from model.stomach import Stomach


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
