from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.waterway_line import FeatureClassWaterwayLine


class FeatureClassWaterwayPoint(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Waterway Point feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__()
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.duplicate = f"{self.name}_1"
        self.fcgeometry = FeatureClassGeometry(name=self.name, geometry=self.geometry)
        waterway_line = FeatureClassWaterwayLine(feature="waterway_line", helper=True)
        waterway_line_fc = FeatureClassGeometry(waterway_line.name,geometry=waterway_line.geometry)

        waterway_points = self.fcgeometry.select_features_by_attributes(
            attribute="waterway",
            field="dock",
            invert="INVERT",
        )

        self.fcgeometry.buffer(in_feature=waterway_points)
        self.fcgeometry.clip(in_feature=waterway_line_fc.name, clippe=f"{self.name}_buffer")
        waterway_line_fc.multipart_to_singlepart(in_feature=f"{waterway_line_fc.name}_clipped")
        waterway_line_fc.dissolve(in_feature=f"{waterway_line_fc.name}_clipped_singlepart", fields="name")
        waterway_line_fc.delete_features(in_view=waterway_line_fc.select_feature_by_locations(
            in_layer=f"{waterway_line_fc.name}_clipped_singlepart_dissolve",
            target=waterway_points
        ))

        waterway_line_fc.calculate_field(
            in_table=f"{waterway_line_fc.name}_clipped_singlepart_dissolve",
            field="angle",
            expression="math.degrees(function(!SHAPE!))",
            code_block="""import math
        
def function(shape):

    
    radian = math.atan2(shape.lastpoint.y - shape.firstpoint.y, 
                        shape.lastpoint.x - shape.firstpoint.x)
    
    if (radian<0):
        radian = (radian+math.pi)*(-1)+math.pi
    else:
        radian=(radian-math.pi)*(-1)+math.pi
    return radian""",
            field_type="FLOAT",
        )
        self.fcgeometry.spatial_join_waterway_angle()
