class ThermalSensation:
    """Class for thermal sensations mapped with is temperature"""

    def __init__(self, temperature: int | float):
        """
        Get temperature and define thermal sensations on board mapped

        :param temperature: Temperature in celsius
        """
        thermal_sensations_check = {
            "very_cold": lambda temperature: temperature < 0,
            "cold": lambda temperature: temperature > 0 and temperature <= 10,
            "chilly": lambda temperature: temperature > 10 and temperature <= 15,
            "mild": lambda temperature: temperature > 15 and temperature <= 25,
            "hot": lambda temperature: temperature > 25 and temperature <= 35,
            "very_hot": lambda temperature: temperature > 35,
        }
        for thermal_sensation, thermal_sensation_check in thermal_sensations_check.items():
            if thermal_sensation_check(temperature):
                self.thermal_sensation = thermal_sensation

    @staticmethod
    def get_all_thermal_sensations() -> tuple:
        """Return all thermal sensations defined"""
        return ("very_cold", "cold", "chilly", "mild", "hot", "very_hot")

    def __str__(self) -> str:
        return self.thermal_sensation
