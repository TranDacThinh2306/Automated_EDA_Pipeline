import pandas as pd
from typing import List

# def get_idp_report(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Generate a report for IDP (Image Description Pipeline) data.
    
#     Args:
#         df (pd.DataFrame): The DataFrame containing IDP data.
        
#     Returns:
#         pd.DataFrame: A DataFrame with the IDP report.
#     """
#     # Filter columns related to IDP
#     idp_columns = [
#         'idp_Img_scene_type',
#         'idp_Img_main_object',
#         # 'idp_Cultural_context',
#         # 'idp_Demographic_signals'
#     ]
    
#     # Create a report DataFrame with the selected columns
#     report_df = df[idp_columns].copy()


#     # Get main object counts and report
#     main_object_counts = df['idp_Img_main_object'].value_counts().reset_index()
#     main_object_counts.columns = ['Main Object', 'Count']
#     report_df = pd.merge(report_df, main_object_counts, on='Main Object', how='left')

#     return report_df

class SceneTypeProcessor:
    """
    A class to process scene types in IDP data.
    """
    def __init__(self):
        self.freq_dict = None

    def _get_freq_dict(self, df: pd.DataFrame, column: str) -> dict:
        freq_dict = df[column].explode().value_counts().to_dict()
        return freq_dict

    def _get_freq_item(self, list_mainobj: List) -> str:
        """
        Returns the item from the list with the highest frequency.
        
        Args:
            list_mainobj (List): A list of objects to check frequencies for
            
        Returns:
            str: The item with the highest frequency, or None if the list is empty
        """
        if self.freq_dict is None: 
            raise ValueError("Frequency dictionary is not initialized.")
        # Return item with highest frequency
        return max(list_mainobj, key=lambda x: self.freq_dict[x])

    # @ Main function to process the scene_type
    def process(self, df: pd.DataFrame, column: str = 'idp_Img_scene_type') -> pd.DataFrame:
        """
        Process the scene type column in the DataFrame.
        
        Returns:
            pd.DataFrame: A DataFrame with processed scene type data.
        """
        df_tmp = df.copy()

        df_tmp[column] = df_tmp[column] \
                .apply(lambda x: x \
                        .replace(',', '') \
                        .replace('(', '') \
                        .replace(')', ''))
        

        df_tmp[column] = df_tmp[column].str.split(' ').apply(lambda x: [item.strip().lower() for item in x if item.strip()])

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