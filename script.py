import pandas as pd
def get_idp_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a report for IDP (Image Description Pipeline) data.
    
    Args:
        df (pd.DataFrame): The DataFrame containing IDP data.
        
    Returns:
        pd.DataFrame: A DataFrame with the IDP report.
    """
    # Filter columns related to IDP
    idp_columns = [
        'idp_Img_scene_type',
        'idp_Img_main_object',
        # 'idp_Cultural_context',
        # 'idp_Demographic_signals'
    ]
    
    # Create a report DataFrame with the selected columns
    report_df = df[idp_columns].copy()


    # Get main object counts and report
    main_object_counts = df['idp_Img_main_object'].value_counts().reset_index()
    main_object_counts.columns = ['Main Object', 'Count']
    report_df = pd.merge(report_df, main_object_counts, on='Main Object', how='left')

    return report_df