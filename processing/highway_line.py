from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.highway_area import FeatureClassHighwayArea


class FeatureClassHighwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Highway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__()
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.duplicate = f"{self.name}_1"
        self.fcgeometry = FeatureClassGeometry(name=self.name, geometry=self.geometry)

        if self.name.find("egyben") > -1:
            delete_features = ["unclassified", "bridleway", "cycleway", "footway", "living_street", "path",
                               "pedestrian", "platform", "raceway", "residential", "road", "service", "services",
                               "steps", "track", "corridor", "tertiary_link", "secondary_link"]
            for field in delete_features:
                self.fcgeometry.delete_features(attribute="highway", field=field)

            self.fcgeometry.dissolve(in_feature=self.name,
                                     fields="highway;ref",
                                     multi_part="MULTI_PART")

        else:
            pedestrian_line = self.fcgeometry.select_features_by_attributes(
                attribute="highway", field="pedestrian",
            )
            pedestrian_line_split = self.fcgeometry.split_line_at_vertices(in_feature=pedestrian_line)
            self.fcgeometry.delete_features(attribute="highway",field="pedestrian")
            highway_area = FeatureClassHighwayArea(feature="highway_area", helper=True)
            pedestrian_area = highway_area.fcgeometry.select_features_by_attributes(
                attribute="highway", field="pedestrian"
            )
            self.fcgeometry.delete_features(
                in_view=self.fcgeometry.select_feature_by_locations(
                    in_layer=pedestrian_line_split,
                    overlap_type="WITHIN",
                    target=pedestrian_area,
                    invert=False
                )
            )
            pedestrian_line_split_dissolve = self.fcgeometry.dissolve(
                in_feature=pedestrian_line_split,
                fields="geom_type;name;highway;bridge;tunnel;ref",
                diff_name="pedestrian_line"
            )
            self.fcgeometry.append_pedestrian(in_feature=pedestrian_line_split_dissolve)


# TODO HIGHWAY rétegen semmi extra(még mindig lassúnak tűnik)
# TODO HIGHWAY_egyben: Delete 144-en nem látszó elemeket. Dissolve