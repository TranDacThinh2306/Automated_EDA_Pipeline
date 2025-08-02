import pandas as pd
import numpy as np
import sys
from utils import Utils
import json
from typing import List
sys.path.append('..')

class EDA:
    def __init__(self, data: json, history: list = []):
        """
        Initialize the EDA pipeline with a DataFrame.
        Args:
            data (json): The JSON data to analyze.
            history (list): A list to keep track of operations performed.
        
        """
        self.parser = Utils()
        self.df = self.parser.convert_to_csv(data)
        self.history = []

    def _drop_duplicates(self):
        """
        Drop duplicate rows in the DataFrame.
        Handles columns with lists by converting to string for duplicate detection.
        """
        try:
            self.df.drop_duplicates(inplace=True)
        except TypeError:
            df_temp = self.df.copy()
            
            # Find columns with list/dict values and convert to string
            for col in df_temp.columns:
                if df_temp[col].dtype == 'object':
                    # Check if column contains lists or dicts
                    sample_val = df_temp[col].dropna().iloc[0] if not df_temp[col].dropna().empty else None
                    if isinstance(sample_val, (list, dict)):
                        df_temp[col] = df_temp[col].astype(str)
            
            # Drop duplicates on the temp dataframe
            df_temp.drop_duplicates(inplace=True)
            
            # Use the index from temp df to filter original df
            self.df = self.df.loc[df_temp.index]
<<<<<<< HEAD

    def _convert_type(self):
        """
        Convert columns to appropriate types.
        Numeric columns are converted to float, string columns are converted to str.
        """
        for col in self.df.columns:
            if col in self.parser.get_numeric_columns():
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

            if col in self.parser.get_str_columns():
                self.df[col] = self.df[col].astype(str)

    # @ Main function to clean the DataFrame
    # Clean the DataFrame by removing NaN values and duplicates.    
=======
        
>>>>>>> parent of 989ebe4 (Update statistical report func)
    def _clean_data(self):
        """        
        Clean the DataFrame by removing NaN values and duplicates.
        Handles columns with lists by converting to string for duplicate detection.
        """
        self.df.dropna(inplace=True, axis=0)
        self._drop_duplicates()
<<<<<<< HEAD
        self._convert_type()
=======
        # self.df.drop_duplicates(inplace=True)
>>>>>>> parent of 989ebe4 (Update statistical report func)
        self.df.reset_index(drop=True, inplace=True)

    def get_metadata(self):
        return {
<<<<<<< HEAD
            'missing_values': [ (key, value) for key,value in self.df.isnull().sum().to_dict().items() if value > 0],
            'number_of_rows': self.df.shape[0],
            'number_of_columns': self.df.shape[1],
            'category': len(self.df.select_dtypes(include=['object']).columns.tolist()),
            'numeric': len(self.df.select_dtypes(exclude=['object']).columns.tolist()),
        }

    def _get_explicit_statistics_data(self):
        pass

    # @ Main function to statistics report
    # Generate a statistics report from the current DataFrame.
    def _get_statistics_report(self) -> None:
        """
        Generate a statistics report from the DataFrame.
        """
        overview_data = self._get_statistics_overview_data()
        statdf = pd.DataFrame(self.df.describe(include='all').to_dict())
        statdf.to_csv('eda_statistics_report.csv', index=True)
        with open('eda_statistics_report.json', 'w', encoding='utf-8') as f:
            json.dump(overview_data, f, indent=4, ensure_ascii=False)

    def _get_score_answers_type(self, type: str) -> None:
        """
        Get score answers based on the specified type.
        Args:
            type (str): The type of score to calculate (e.g., 'median', 'mean', 'max', 'min').
        """
        columns = [col for col in self.df.columns if "Score_for_answers" in col]
        if not columns:
            raise ValueError(f"No columns found with 'Score_for_answers' in type: {type}")
        
        for col in columns:
            col_type_name = col.replace("Score_for_answers", f"Score_answers_{type}")
            if type == "median":
                self.df[col_type_name] = self.df[col].apply(lambda x: np.median(x))
            elif type == "mean":
                self.df[col_type_name] = self.df[col].apply(lambda x: np.mean(x))
            elif type == "max":
                self.df[col_type_name] = self.df[col].apply(lambda x: np.max(x))
            elif type == "min":
                self.df[col_type_name] = self.df[col].apply(lambda x: np.min(x))

    def _create_label_columns(self, columns: List[str], type: str) -> None:
=======
            'columns': self.df.columns.tolist(),
            'shape': self.df.shape,
            'missing_values': self.df.isnull().sum().to_dict(),
            'unique_values': {col: self.df[col].nunique() for col in self.df.columns}
        }

    def _get_columns_with_prefix(self, prefix: str = None) -> List[str]:
        """
        Get columns that start with a specific prefix or contain 'score'.
        Args:
            prefix (str): The prefix to filter columns by. If None, defaults to 'score'.
        Returns:
            list: A list of column names that match the criteria.
        """
        if prefix is None:
            return [col for col in self.df.columns if 'score' in col.lower()]
        return [col for col in self.df.columns if col.startswith(prefix) and 'score' in col.lower()]

    def _create_label_columns(self, columns: List[str]) -> None:
>>>>>>> parent of 989ebe4 (Update statistical report func)
        """
        Create label columns based on the median value of specified columns.
        Args:
            columns (List[str]): A list of column names to create label columns for.
        """
<<<<<<< HEAD
        type_value = None
        for col in columns:
            col_label = col + '_Label'

            if type == "median":
                type_value = self.df[col].median()
            elif type == "mean":
                type_value = self.df[col].mean()
            elif type == "max":
                type_value = self.df[col].max()
            elif type == "min":
                type_value = self.df[col].min()

            self.df[col_label] = self.df[col].apply(lambda x: 'Passed' if x >= type_value else 'Failed')

    # @ Main function to create label columns
    def _create_label_columns_from_prefix(self, type: str, prefix: str=None) -> None:
=======
        df = self.df.copy()
        for col in columns:
            col_label = col + '_Label'
            median_value = df[col].median()
            df[col_label] = np.where(df[col] >= median_value, 'Passed', 'Failed')
            
        self.df = df

    def _create_label_columns_from_prefix(self, prefix: str=None) -> None:
>>>>>>> parent of 989ebe4 (Update statistical report func)
        """
        Create label columns based on the median value of columns that start with a specific prefix.
        Args:
            prefix (str): The prefix to filter columns by.
            If prefix is not provided, skip prefix filtering.
<<<<<<< HEAD
        Calls:
            _create_label_columns: To create label columns based on the median value.
=======
>>>>>>> parent of 989ebe4 (Update statistical report func)
        """
        columns = self.df.select_dtypes(include=['number']).columns.tolist()
        columns = [col for col in columns if "Score_for_answers" not in col]
        print(f"Columns to create labels: {columns}")
        if not columns:
            raise ValueError(f"No columns found with prefix: {prefix}")
        
        self._create_label_columns(columns)

    def run_pipeline(self, prefix: str=None) -> None:
        print("Running EDA pipeline...")
        self._clean_data()
<<<<<<< HEAD
        self._get_score_answers_type(type)
        self._create_label_columns_from_prefix(type)
        self._get_statistics_report()
        # self._get_explicit_statistics_data()

=======
        self._create_label_columns_from_prefix(prefix)
>>>>>>> parent of 989ebe4 (Update statistical report func)
        print("EDA pipeline completed.")

    def get_dataframe(self):
        return self.df
    