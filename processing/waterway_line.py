from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.water_area import FeatureClassWaterArea


class FeatureClassWaterwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Waterway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)

        if not helper:
            print("WATERWAY LINE")
            waterway_line = self.fcgeometry.select_features_by_attributes(
                where_clause="waterway IN ('canal','ditch','drain','river','stream')",
            )
            waterway_line_split = self.fcgeometry.split_line_at_vertices(in_feature=waterway_line)
            self.fcgeometry.delete_features(in_view=waterway_line)
            water_area = FeatureClassWaterArea(feature="water_area", helper=True)
            self.fcgeometry.delete_features(
                in_view=self.fcgeometry.select_feature_by_locations(
                    in_layer=waterway_line_split,
                    overlap_type="WITHIN",
                    target=water_area,
                    invert=False,
                )
            )
            waterway_line_split_dissolve = self.fcgeometry.dissolve(
                in_feature=waterway_line_split,
                fields="name;waterway;tunnel",
                diff_name="waterway_diff_dissolve_line"
            )
            self.fcgeometry.append_pedestrian(
                in_feature=waterway_line_split_dissolve
            )
