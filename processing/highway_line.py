import arcpy
import arcpy.management

from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.highway_area import FeatureClassHighwayArea


class FeatureClassHighwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Highway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)
        if self.name != "highway_egyben_line":
            if self.name.find("egyben") > -1:
                delete_features = ["unclassified", "bridleway", "cycleway", "footway", "living_street", "path",
                                   "pedestrian", "platform", "raceway", "residential", "road", "service", "services",
                                   "steps", "track", "corridor", "tertiary_link", "secondary_link"]
                for field in delete_features:
                    self.fcgeometry.delete_features(attribute="highway", field=field)


                arcpy.management.Append(
                    inputs=self.name,
                    target="highway_egyben_line",
                    schema_type="NO_TEST",
                    field_mapping="",
                    subtype="",
                    expression="",
                    match_fields=None,
                    update_geometry="NOT_UPDATE_GEOMETRY"
                )

            else:
                pedestrian_line = self.fcgeometry.select_features_by_attributes(
                    attribute="highway", field="pedestrian",
                )
                pedestrian_line_split = self.fcgeometry.split_line_at_vertices(in_feature=pedestrian_line)
                self.fcgeometry.delete_features(attribute="highway", field="pedestrian")
                highway_area = FeatureClassHighwayArea(feature="highway_area", helper=True)
                pedestrian_area = highway_area.fcgeometry.select_features_by_attributes(
                    attribute="highway", field="pedestrian"
                )
                self.fcgeometry.delete_features(
                    in_view=self.fcgeometry.select_feature_by_locations(
                        in_layer=pedestrian_line_split,
                        overlap_type="WITHIN",
                        target=pedestrian_area,
                        invert=False
                    )
                )
                pedestrian_line_split_dissolve = self.fcgeometry.dissolve(
                    in_feature=pedestrian_line_split,
                    fields="geom_type;name;highway;bridge;tunnel;ref",
                    diff_name=f"pedestrian_{self.name.split('_')[1]}_line"
                )
                self.fcgeometry.append_pedestrian(in_feature=pedestrian_line_split_dissolve)

                self.fcgeometry.calculate_field(
                    field="highway",
                    expression="highway_level(!highway!,!bridge!,!tunnel!)",
                    code_block="""def highway_level(highway,bridge,tunnel):
                    if bridge != 'None' and bridge != 'no':
                        return highway+"_hid"
                    if tunnel != 'None' and tunnel != 'no':
                        return highway+"_alagut"
                    else:
                        return highway
                """,
                )
                self.fcgeometry.append_highway_line_hid(in_feature=self.name)
                self.fcgeometry.delete_features(
                    in_view=self.fcgeometry.select_features_by_attributes(
                        where_clause="""highway LIKE '%hid'""",
                    ))
                self.fcgeometry.delete_fields(
                    input_feature=fr"{arcpy.env.workspace}\highway_line_hid",
                    delete_field=["tunnel", "bridge"])

                if self.name != "highway_line":
                    arcpy.management.Append(
                        inputs=self.name,
                        target="highway_line",
                        schema_type="NO_TEST",
                        field_mapping="",
                        subtype="",
                        expression="",
                        match_fields=None,
                        update_geometry="NOT_UPDATE_GEOMETRY"
                    )
        else:
            self.fcgeometry.dissolve(in_feature=self.name,
                                     fields="highway;ref",
                                     multi_part="MULTI_PART")