from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassRailwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper:bool = False) -> None:
        """
        Concrete class to process Railway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)

        if not helper:
            print("RAILWAY LINE")
            if self.name.find("egyben") > -1:
                delete_features = ["funicular", "light_rail", "miniature", "narrow_gauge", "platform", "subway","tram"]
                for field in delete_features:
                    self.fcgeometry.delete_features(attribute="railway", field=field)

                self.fcgeometry.delete_features(attribute="usage",field="tourism")

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

                self.fcgeometry.delete_fields(
                    input_feature=self.name,
                    delete_field=["service", "usage","station","bridge","tunnel"])
