import pandas as pd
import json
from config import (
    ETP_FIELD_CONFIG, 
    EIP_FIELD_CONFIG, 
    IDP_FIELD_CONFIG, 
    VQAC_FIELD_CONFIG, 
    NUMERIC_FIELD_CONFIG, 
    STR_FIELD_CONFIG, 
    LIST_FIELD_CONFIG, 
    )

class Utils:
    """
    A utils class for extracting structured data from DataFrame columns.
    """
    def __init__(self):
        """Initialize utils with field configurations."""
        self.patterns = [ETP_FIELD_CONFIG, EIP_FIELD_CONFIG, IDP_FIELD_CONFIG, VQAC_FIELD_CONFIG]

    def convert_to_csv(self, data: json, wanted_col: list = ['index']) -> pd.DataFrame:
        """Apply all patterns to parse the DataFrame."""
        df = pd.json_normalize(data, sep="_")
        return df[ETP_FIELD_CONFIG + EIP_FIELD_CONFIG + IDP_FIELD_CONFIG + VQAC_FIELD_CONFIG + wanted_col].copy()

    @staticmethod
    def get_columns(pattern: str = None) -> list:
        """Return the list of parsing patterns."""
        if pattern == "ETP":
            return ETP_FIELD_CONFIG
        elif pattern == "EIP":
            return EIP_FIELD_CONFIG
        elif pattern == "IDP":
            return IDP_FIELD_CONFIG
        elif pattern == "VQAC":
            return VQAC_FIELD_CONFIG
        return ETP_FIELD_CONFIG + EIP_FIELD_CONFIG + IDP_FIELD_CONFIG + VQAC_FIELD_CONFIG
    
    def get_numeric_columns(self) -> list:
        """Return numeric columns from the DataFrame."""
        return NUMERIC_FIELD_CONFIG
    
    def get_str_columns(self) -> list:
        """Return string columns from the DataFrame."""
        return STR_FIELD_CONFIG
    
    def get_list_columns(self) -> list:
        """Return list columns from the DataFrame."""
        return LIST_FIELD_CONFIG