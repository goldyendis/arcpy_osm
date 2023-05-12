from datetime import date

from arcgis.geometry import arcpy

from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.railway_line import FeatureClassRailwayLine


class FeatureClassRailwayPoint(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Railway Point feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__()
        self.name = feature
        self.geometry = feature.split("_")[-1]
        self.duplicate = f"{self.name}_1"
        self.fcgeometry = FeatureClassGeometry(name=self.name, geometry=self.geometry)
        railway_line = FeatureClassRailwayLine(feature="railway_egyben_line", helper=True)
        railway_line_fc = FeatureClassGeometry(name=railway_line.name, geometry=railway_line.geometry)
        self.fcgeometry.snap_railway_stations_to_line(line=railway_line_fc)
        snaped_all_points = self.fcgeometry.select_feature_by_locations(
            target=railway_line_fc.name, invert=False
        )
        railway_points = self.fcgeometry.select_features_by_attributes(
            in_view=snaped_all_points,
            attribute="railway",
            field="tram_stop",
            selection_type="REMOVE_FROM_SELECTION",
        )
        self.fcgeometry.buffer(in_feature=railway_points)
        self.fcgeometry.clip(in_feature=railway_line_fc.name, clippe=f"{self.name}_buffer")

        railway_line_fc.multipart_to_singlepart(in_feature=f"{railway_line_fc.name}_clipped")
        railway_line_fc.dissolve(in_feature=f"{railway_line_fc.name}_clipped_singlepart", fields="railway")

        self.fcgeometry.delete_features(in_view=self.fcgeometry.select_feature_by_locations(
            in_layer=f"{railway_line_fc.name}_clipped_singlepart_dissolve",
            target=railway_points
        ))
        self.fcgeometry.delete_features(in_view=self.fcgeometry.select_features_by_attributes(
            in_view=f"{railway_line_fc.name}_clipped_singlepart_dissolve",
            attribute="railway",
            field="platform"
        ))
        railway_narrow = railway_line_fc.select_features_by_attributes(
            in_view=f"{railway_line_fc.name}_clipped_singlepart_dissolve",
            attribute="railway",
            field="narrow_gauge",
        )
        railway_none_station = self.fcgeometry.select_features_by_attributes(
            attribute="station", field="None"
        )
        railway_narrow_gauge_stations = self.fcgeometry.select_feature_by_locations(
            in_layer=railway_none_station,
            target=railway_narrow,
            invert=False,
        )
        self.fcgeometry.calculate_field(
            in_table=railway_narrow_gauge_stations,
            field="railway",
            code_block="""def function():
                             return "narrow_gauge" """,
        )

        railway_line_fc.calculate_field(
            in_table=f"{railway_line_fc.name}_clipped_singlepart_dissolve",
            field="angle",
            expression="math.degrees(function(!SHAPE!))",
            field_type="FLOAT",
            code_block="""import math

def function(shape):

    
    radian = math.atan2(shape.lastpoint.y - shape.firstpoint.y, 
                        shape.lastpoint.x - shape.firstpoint.x)
    
    if (radian<0):
        radian = (radian+math.pi)*(-1)+math.pi
    else:
        radian=(radian-math.pi)*(-1)+math.pi
    return radian""",

        )
        self.fcgeometry.spatial_join_railway_angle()
