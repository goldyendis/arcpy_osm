from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassHighwayPoint(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Highway Point feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__()
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.duplicate = f"{self.name}_1"
        self.fcgeometry = FeatureClassGeometry(name=self.name, geometry=self.geometry)
        self.duplicate = self.fcgeometry.select_by_attribute(attribute="motorway_junction", out_name=f"{self.name}_motorway")
        self.fcgeometry.integrate(layer = self.duplicate, distance= 500)
        self.fcgeometry.add_x_y(self.duplicate)
        self.dissolve_duplicate = self.fcgeometry.dissolve_point(fields=["POINT_X;POINT_Y"], layer=self.duplicate)
        self.fcgeometry.spatial_join_highway_motorway_junction(
            target = self.dissolve_duplicate,
            join = self.duplicate)