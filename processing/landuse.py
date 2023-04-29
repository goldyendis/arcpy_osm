from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassLanduseArea(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Landuse Area feature layer
        :param feature: str | The name of the feature layer
        """
        super().__init__()
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.fcgeometry = FeatureClassGeometry(name=self.name, geometry=self.geometry)
        self.fcgeometry.simplify_to_scale()
        self.fcgeometry.calculate_area()

    def test(self):
        pass
