from abc import ABC

from manipulation.feature_class_geometry import FeatureClassGeometry

# from enum import Enum
#
# class FeatureEnum(Enum):
#     LANDUSE_AREA = "landuse_area"
#

class AbstractFeatureClass(ABC):
    def __init__(self, feature: str) -> None:
        """
        Parent class of the Concrete Feature Layer processor classes
        """
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.duplicate = f"{self.name}_1"
        self.fcgeometry = FeatureClassGeometry(name=self.name, geometry=self.geometry)
