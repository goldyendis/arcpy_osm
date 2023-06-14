from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.man_made_area import FeatureClassManMadeArea


class FeatureClassManMadeLine(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
             Concrete class to process Man_Made Line feature layer
             :param feature: str | The name of feature layer
             """
        super().__init__(feature=feature)

        pier_line = self.fcgeometry.select_features_by_attributes(
            attribute="man_made", field="pier",
        )
        pier_line_split = self.fcgeometry.split_line_at_vertices(in_feature=pier_line)
        self.fcgeometry.delete_features(attribute="man_made", field="pier")
        man_made_area = FeatureClassManMadeArea(feature="man_made_area", helper=True)
        pier_area = man_made_area.fcgeometry.select_features_by_attributes(
            attribute="man_made", field="pier"
        )
        self.fcgeometry.delete_features(
            in_view=self.fcgeometry.select_feature_by_locations(
                in_layer=pier_line_split,
                overlap_type="WITHIN",
                target=pier_area,
                invert=False
            )
        )
        pier_line_split_dissolve = self.fcgeometry.dissolve(
            in_feature=pier_line_split,
            fields="geom_type;name;man_made",
            diff_name="pier_line"
        )
        self.fcgeometry.append(in_feature=pier_line_split_dissolve,
                               target=self.name,
                               exp_column="man_made",
                               exp_value="pier")
