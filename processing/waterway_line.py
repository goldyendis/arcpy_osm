from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassWaterwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper:bool = False) -> None:
        """
        Concrete class to process Waterway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)

        if not helper:
            print("WATERWAY LINE")
