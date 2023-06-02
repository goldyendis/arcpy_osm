from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassManMadePoint(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Man_Made Point feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)
        self.fcgeometry.delete_features(attribute=self.name[:self.name.rfind('_')],field="None")
