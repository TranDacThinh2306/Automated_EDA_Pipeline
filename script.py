import re
import pandas as pd
from typing import List

class ReportGenerator:

    @staticmethod
    def generate_report(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Generate a report on the main objects in the DataFrame.
        
        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str): The column name to analyze.
        
        Returns:
            pd.DataFrame: A DataFrame with the main object report.
        """
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        report = df[column].value_counts().reset_index()
        report.columns = [column, 'Frequency']
        return report

class SceneTypeProcessor:
    """
    A class to process scene types in IDP data.
    """
    def __init__(self):
        self.freq_dict = None

    # This method is used to get the frequency dictionary for scene types
    def _get_freq_dict(self, df: pd.DataFrame, column: str) -> dict:
        """
        Returns a frequency dictionary for the specified column in the DataFrame.
        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str): The column name to analyze.
        Returns:
            dict: A dictionary with items as keys and their frequencies as values.
        """
        freq_dict = df[column].explode().value_counts().to_dict()
        return freq_dict

    # This method is used to get the item with the highest frequency from a list
    def _get_freq_item(self, list_scenetype: List) -> str:
        """
        Returns the item from the list with the highest frequency.
        
        Args:
            list_scenetype (List): A list of objects to check frequencies for
            
        Returns:
            str: The item with the highest frequency, or None if the list is empty
        """
        if self.freq_dict is None: 
            raise ValueError("Frequency dictionary is not initialized.")
        
        # Return item with highest frequency
        return max(list_scenetype, key=lambda x: self.freq_dict[x])

    # @ Main function to process the scene_type
    def process(self, df: pd.DataFrame, column: str = 'idp_Img_scene_type') -> pd.DataFrame:
        """
        Process the scene type column in the DataFrame.
        
        Returns:
            pd.DataFrame: A DataFrame with processed scene type data.
        """
        df_tmp = df.copy()

        df_tmp[column] = df_tmp[column].apply(lambda x: [word.strip() 
                                                         for word in re.split(r'[ /:;@!,_\\]+', x.lower()) 
                                                         if word.strip()])

        self.freq_dict = self._get_freq_dict(df_tmp, column)
        df_tmp[column] = df_tmp[column].apply(lambda x: self._get_freq_item(x))

        return df_tmp
    
    # @ Method to get the frequency dictionary
    def get_freq_dict(self) -> dict:
        """
        Get the frequency dictionary of scene types.
        
        Returns:
            dict: A dictionary with scene types and their frequencies.
        """
        if self.freq_dict is None:
            print("Frequency dictionary is not initialized. Please run the process method first.")
        return self.freq_dict
    
    @staticmethod
    def generate_report(df: pd.DataFrame, column: str = 'idp_Img_scene_type') -> pd.DataFrame:
        return ReportGenerator.generate_report(df, column)
        
class MainObjProcessor:
    """
    A class to process main objects in IDP data.
    """
    def process(df: pd.DataFrame, column: str = 'idp_Img_main_object') -> pd.DataFrame:
        """
        Process the main object column in the DataFrame.
        
        Returns:
            pd.DataFrame: A DataFrame with processed main object data.
        """
        df_tmp = df.copy()
        
        # Convert the column to lowercase and split by spaces
        df_tmp[column] = df_tmp[column].apply(lambda x: x.lower() if isinstance(x, str) else None)
        
        return df_tmp

    @staticmethod
    def generate_report(df: pd.DataFrame, column: str = 'idp_Img_main_object') -> pd.DataFrame:
        return ReportGenerator().generate_report(df, column)
        