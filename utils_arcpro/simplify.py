class Simplify:
    levels_area = {"1": ['BEND_SIMPLIFY', "1 Kilometers", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                   "2": ['BEND_SIMPLIFY', "500 Meters", "0,4 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                   "3": ['BEND_SIMPLIFY', "100 Meters", "0,15 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP']}

    levels_line = {}

    def get_simplify_properties(self, level: str, geometry: str) -> list[str]:
        """
        Get the Simplification details
        :param geometry: str | type of geometry ("area","line","point")
        :param level: str | The level of the Simplification from the levels dictionary
        :return: list[str] of the properties value
        """
        if geometry == "area":
            return self.levels_area[level]
        if geometry == "line":
            return self.levels_line[level]
