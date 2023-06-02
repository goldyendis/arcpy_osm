from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassCommon(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process common feature layers
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)
