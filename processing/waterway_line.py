from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassWaterwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Waterway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)

        if not helper:
            print("WATERWAY LINE")

            self.fcgeometry.erase(
                input_feature=self.fcgeometry.select_features_by_attributes(
                    where_clause="waterway IN ('canal','ditch','drain','river','stream')",
                ),
                erase = "water_area",
            )
            self.fcgeometry.delete_features(in_view=self.fcgeometry.select_features_by_attributes(
                where_clause="waterway IN ('canal','ditch','drain','river','stream')",
            ))
            waterway_line_split_dissolve = self.fcgeometry.dissolve(
                in_feature=f"{self.name}_erase",
                fields="name;waterway;tunnel",
                diff_name="waterway_diff_dissolve_line"
            )
            self.fcgeometry.delete_fields(input_feature=self.name, delete_field=["geom_type",])

            self.fcgeometry.append(
                in_feature=waterway_line_split_dissolve,
                sql="waterway in ('canal','ditch','drain','river','stream')",
                target="waterway_line"
            )
