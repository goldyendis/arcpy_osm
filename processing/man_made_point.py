from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassManMadePoint(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Man_Made Point feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__()
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.duplicate = f"{self.name}_1"
        self.fcgeometry = FeatureClassGeometry(name=self.name, geometry=self.geometry)
        self.fcgeometry.select_by_attribute(attribute="tower", out_name=self.duplicate, inverse=True)
        tower: str = self.fcgeometry.select_by_attribute(attribute="tower", out_name=f"{self.name}_tower")
