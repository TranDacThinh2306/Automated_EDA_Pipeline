import pandas as pd
import numpy as np
import json
import ast
from typing import List

from utils import Utils
from script import SceneTypeProcessor

# sys.path.append('..')

class EDA:
    def __init__(self, data: json, history: list = []):
        """
        Initialize the EDA pipeline with a DataFrame.
        Args:
            data (json): The JSON data to analyze.
            history (list): A list to keep track of operations performed.
        
        """
        self.utils = Utils()
        self.processor = SceneTypeProcessor()
        self.df = self.utils.convert_to_csv(data)
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
                    sample_val = df_temp.loc[0,col]
                    if isinstance(sample_val, (list, dict)):
                        df_temp[col] = df_temp[col].astype(str)
            
            df_temp.drop_duplicates(inplace=True)
            self.df = self.df.loc[df_temp.index]

    def _filter_invalid(self):
        """
        Convert columns to appropriate types.
        Filters out rows where list columns are valid.
        """

        def is_invalid_row(row):
            try:
                row_lists = row.tolist()

                if not all(isinstance(x, list) for x in row_lists):
                    return True

                if any(len(x) == 0 for x in row_lists):
                    return True
                
                lengths = [len(x) for x in row_lists]
                return len(set(lengths)) != 1  # True nếu độ dài không đều

            except Exception:
                return True  # Nếu có lỗi thì cũng coi như không hợp lệ
            
        for col in self.utils.get_numeric_columns():
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        for col in self.utils.get_str_columns():
            self.df[col] = self.df[col].astype(str)

        mask = self.df[self.utils.get_list_columns()[:5]].apply(is_invalid_row, axis=1)
        self.df = self.df[~mask]

    # @ Main function to clean the DataFrame
    # Clean the DataFrame by removing NaN values and duplicates.    
    def _clean_data(self):
        """        
        Clean the DataFrame by removing NaN values and duplicates.
        Handles columns with lists by converting to string for duplicate detection.
        """
        self.df.dropna(inplace=True, axis=0)
        self._drop_duplicates()
        self._filter_invalid()
        self.df.dropna(inplace=True, axis=0) # Việc này đảm bảo sau khi thực hiện convert không thực hiện dropna lại sẽ không có NaN nào còn sót lại
        self.df.reset_index(drop=True, inplace=True)

    def _get_statistics_overview_data(self):
        return {
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
        """
        Create label columns based on the median value of specified columns.
        Args:
            columns (List[str]): A list of column names to create label columns for.
        """
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
        """
        Create label columns based on the median value of columns that start with a specific prefix.
        Args:
            prefix (str): The prefix to filter columns by.
            If prefix is not provided, skip prefix filtering.
        Calls:
            _create_label_columns: To create label columns based on the median value.
        """
        columns = self.df.select_dtypes(include=['number']).columns.tolist()
        if not columns:
            raise ValueError(f"No columns found with prefix: {prefix}")
        
        self._create_label_columns(columns, type)

    def run(self, type: str = 'median', prefix: str = None) -> None:
        print("Running EDA pipeline...")

        # Step 1: Data Cleaning
        self._clean_data()

        # Step 2: Process scene types
        self.df = self.processor.process(self.df)

        # Step 3: Process to get score answers based on the specified type 
        self._get_score_answers_type(type)

        # Step 4: Labelize numeric columns with median threshold
        self._create_label_columns_from_prefix(type, prefix)

        # Step 5: Generate statistics report pdf file (Optional)
        # self._get_statistics_report()
        # self._get_explicit_statistics_data()

        print("EDA pipeline completed.")

    def get_dataframe(self):
        return self.df
    