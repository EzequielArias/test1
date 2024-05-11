# Abstract class
from typing import Optional

class Connector():
    information_found: Optional[list] = []
    connector_data : Optional[dict] = {}
    audit_data : Optional[dict] = {"created_at" : "", "updated_at" : "", "elapsed time" : ""}
    information_connector : Optional[dict]
    

    def __init__(self) -> None:
        pass

    def search(self) -> None:
        pass

    def normalize(self, data) -> None:
        pass

    def transform_search_query_data(self) -> None:
        pass

