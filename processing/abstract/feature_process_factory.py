from processing.barrier_point import FeatureClassBarrierPoint
from processing.highway_line import FeatureClassHighwayLine
from processing.landuse import FeatureClassLanduseArea
from processing.man_made_line import FeatureClassManMadeLine
from processing.man_made_point import FeatureClassManMadePoint
from processing.railway_line import FeatureClassRailwayLine
from processing.railway_point import FeatureClassRailwayPoint
from processing.waterway_point import FeatureClassWaterwayPoint


class FeatureProcessFactory:
    @staticmethod
    def create_factory(feature):
        if feature == "landuse_area":
            print("LANDUSE AREA")
            FeatureClassLanduseArea(feature = feature)
        if feature == "barrier_point":
            print("BARRIER_POINT")
            FeatureClassBarrierPoint(feature = feature)
        if feature == "man_made_point":
            print("man_made_POINT")
            FeatureClassManMadePoint(feature = feature)
        if feature == "railway_point":
            print("RAILWAY_POINT")
            FeatureClassRailwayPoint(feature = feature)
        if feature == "waterway_point":
            print("WATERWAY_POINT")
            FeatureClassWaterwayPoint(feature = feature)
        if feature == "highway_egyben_line":
            print("HIGHWAY_EGYBEN_LINE")
            FeatureClassHighwayLine(feature = feature)
        if feature == "highway_line":
            print("HIGHWAY_LINE")
            FeatureClassHighwayLine(feature=feature)
        if feature == "man_made_line":
            print("MAN_MADE_LINE")
            FeatureClassManMadeLine(feature=feature)
        if feature == "railway_egyben_line":
            print("RAILWAY_EGYBEN_LINE")
            FeatureClassRailwayLine(feature = feature)
        if feature == "railway_line":
            print("HIGHWAY_LINE")
            FeatureClassRailwayLine(feature=feature)