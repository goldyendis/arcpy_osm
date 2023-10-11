from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassPlacePoint(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Place Point feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)
        budapest_point = self.fcgeometry.select_features_by_attributes(
            attribute="name",
            field="Budapest"
        )
        self.fcgeometry.calculate_field(
            in_table=budapest_point,
            field="place",
            expression="capitol",
            code_block="",
        )
