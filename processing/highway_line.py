from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


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
                               "steps", "track", "corridor"]
            for field in delete_features:
                self.fcgeometry.delete_features(attribute="highway", field=field)

            self.fcgeometry.dissolve(in_feature=self.name,
                                     fields="highway;ref",
                                     multi_part="MULTI_PART")

# TODO HIGHWAY rétegen semmi extra(még mindig lassúnak tűnik)
# TODO HIGHWAY_egyben: Delete 144-en nem látszó elemeket. Dissolve

