from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassRailwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper:bool = False) -> None:
        """
        Concrete class to process Railway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__()
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.duplicate = f"{self.name}_1"
        if not helper:
            print("RAILWAY LINE")
