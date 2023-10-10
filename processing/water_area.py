from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.waterway_line import FeatureClassWaterwayLine


class FeatureClassWaterArea(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Highway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)
        if not helper:
            print("WATER AREA")
            self.fcgeometry.dissolve(
                in_feature=self.name,
                unsplit_lines="UNSPLIT_LINES",
                fields="name"
            )
            self.fcgeometry.simplify_to_scale(input_feature="water_area_dissolve")
            self.fcgeometry.calculate_area()

            waterway_line = FeatureClassWaterwayLine(feature="waterway_line", helper=True)
            waterway_line_river = waterway_line.fcgeometry.select_features_by_attributes(
                attribute="waterway", field="river"
            )
            water_area_needed = self.fcgeometry.select_feature_by_locations(
                overlap_type="BOUNDARY_TOUCHES",
                target=waterway_line_river,
                invert=False,
            )
            self.fcgeometry.copy_feature_layer(
                input_feature=water_area_needed,
                out_name="water_area_river_touch"
            )



