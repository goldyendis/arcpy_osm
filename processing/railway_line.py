from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass
from processing.railway_area import FeatureClassRailwayArea


class FeatureClassRailwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Railway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)

        if not helper:
            print("RAILWAY LINE")
            if self.name.find("egyben") > -1:
                delete_features = ["funicular", "light_rail", "miniature", "narrow_gauge", "platform", "subway", "tram"]
                for field in delete_features:
                    self.fcgeometry.delete_features(attribute="railway", field=field)

                self.fcgeometry.delete_features(attribute="usage", field="tourism")

                dissolve_feature = self.fcgeometry.dissolve(in_feature=self.name,
                                                            fields="railway;service;usage",
                                                            unsplit_lines="UNSPLIT_LINES",
                                                            )
                self.fcgeometry.calculate_field(
                    in_table=dissolve_feature,
                    field="railway",
                    expression="railway_type(!service!,!usage!)",
                    code_block="""def railway_type(service,usage):
                                      if service == "None":
                                          return "main"
                                      else:
                                          return "side" """,
                )
            else:
                self.fcgeometry.calculate_field(
                    field="railway",
                    expression="railway_calculate(!railway!,!usage!)",
                    code_block="""def railway_calculate(railway,usage):
                    if railway == "rail":
                        if usage in ["main","branch"]:
                            return "rail_main"
                        else:
                            return "rail_side"
                    else:
                        return railway""",

                )
                self.fcgeometry.calculate_field(
                    field="railway",
                    expression="railway_level(!railway!,!bridge!,!tunnel!)",
                    code_block="""def railway_level(railway,bridge,tunnel):
                                if bridge != 'None' and bridge != 'no':
                                    return railway+"_hid"
                                if tunnel != 'None' and tunnel != 'no':
                                    return railway+"_alagut"
                                else:
                                    return railway
                            """,
                )

                platform_line = self.fcgeometry.select_features_by_attributes(
                    attribute="railway", field="platform",
                )
                platform_line_split = self.fcgeometry.split_line_at_vertices(in_feature=platform_line)
                self.fcgeometry.delete_features(attribute="railway", field="platform")
                railway_area = FeatureClassRailwayArea(feature="railway_area", helper=True)
                platform_area = railway_area.fcgeometry.select_features_by_attributes(
                    attribute="railway", field="platform"
                )
                self.fcgeometry.delete_features(
                    in_view=self.fcgeometry.select_feature_by_locations(
                        in_layer=platform_line_split,
                        overlap_type="WITHIN",
                        target=platform_area,
                        invert=False
                    )
                )
                platform_line_split_dissolve = self.fcgeometry.dissolve(
                    in_feature=platform_line_split,
                    fields="geom_type;name;railway;bridge;tunnel;service;usage;station",
                    diff_name="platform_line"
                )
                self.fcgeometry.append(
                    in_feature=platform_line_split_dissolve,
                    target="railway_line",
                    exp_column="railway",
                    exp_value="platform",
                )
                self.fcgeometry.export_railway_line_alagut()
                self.fcgeometry.delete_features(
                    in_view=self.fcgeometry.select_features_by_attributes(
                        where_clause="""railway LIKE '%alagut'""",
                    ))

                self.fcgeometry.delete_fields(
                    input_feature=self.name,
                    delete_field=["service", "usage", "station", "bridge", "tunnel"])
