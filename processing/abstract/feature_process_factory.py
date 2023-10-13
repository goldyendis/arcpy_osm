from processing.barrier_point import FeatureClassBarrierPoint
from processing.building_area import FeatureClassBuildingArea
from processing.highway_line import FeatureClassHighwayLine
from processing.landuse import FeatureClassLanduseArea
from processing.man_made_line import FeatureClassManMadeLine
from processing.man_made_point import FeatureClassManMadePoint
from processing.place_point import FeatureClassPlacePoint
from processing.railway_line import FeatureClassRailwayLine
from processing.railway_point import FeatureClassRailwayPoint
from processing.water_area import FeatureClassWaterArea
from processing.waterway_line import FeatureClassWaterwayLine
from processing.waterway_point import FeatureClassWaterwayPoint




class FeatureProcessFactory:
    @staticmethod
    def create_factory(feature):
        name_parts = feature.split("_")
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
        if feature == "man_made_line":
            print("MAN_MADE_LINE")
            FeatureClassManMadeLine(feature=feature)
        # if feature == "railway_egyben_line":
        #     print("RAILWAY_EGYBEN_LINE")
        #     FeatureClassRailwayLine(feature = feature)
        if feature == "railway_line":
            print("RAILWAY_LINE")
            FeatureClassRailwayLine(feature=feature)
        if feature == "waterway_line":
            print("WATERWAY_LINE")
            FeatureClassWaterwayLine(feature=feature)
        if feature == "water_area":
            print("WATER_AREA")
            FeatureClassWaterArea(feature=feature)
        if len(name_parts) == 3 and name_parts[0] == "building" and name_parts[2] == "area":
            print("_".join(name_parts))
            FeatureClassBuildingArea(feature=feature)
        if len(name_parts) == 4 and name_parts[0] == "highway" and name_parts[1] == "egyben":
            print("HIGHWAY_EGYBEN_LINE")
            FeatureClassHighwayLine(feature = feature)
        if len(name_parts) == 3 and name_parts[0] == "highway" and name_parts[2] == "line" and name_parts[1] != "egyben":
            print("HIGHWAY_LINE")
            FeatureClassHighwayLine(feature=feature)
        if feature == "place_point":
            print("PLACE_POINT")
            FeatureClassPlacePoint(feature=feature)



