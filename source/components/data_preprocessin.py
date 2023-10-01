
import pandas as pd
from source.logger import logging
from source.exception import CustomException

def create_RUL_column(df):
    try:
        """
        Creates a new column in the dataframe called 'RUL' which is the 
        difference between the maximum value of the 'time_cycles' column and 
        the current value of the 'time_cycles' column.
        
        Parameters:
        df (pandas.DataFrame): The dataframe to add the RUL column to.
        
        Returns:
        pandas.DataFrame: The dataframe with the new RUL column added.
        """
    
        df['RUL'] =  df.groupby(['unit_number'])['time_cycles'].transform('max')-df['time_cycles']
        return df
    
    except Exception as e:
        raise exception.CustomException(e,sys)


def drop_constant_columns(df):
    try:
        logging.info("Dropping of constant columns initiated")
        """Drops columns from the dataframe that have only one unique value. 

        Parameters:
        df (pandas.DataFrame): The dataframe to drop columns from.

        Returns:
        pandas.DataFrame: The dataframe with constant columns dropped. 
        """
    
        constant_columns = [col for col in df.columns if df[col].nunique() == 1]
        df = df.drop(constant_columns, axis=1)
        return df
    except Exception as e:
        raise exception.CustomException(e,sys)
def feature_engineer(df):
    logging.info("Feature Engineering started")
    try:
        "create new columns to improve model perfomance"
        # Create a new column for the mean of the LPC outlet temperature and HPC outlet temperature
        df['mean_temp'] = df[['(LPC outlet temperature) (◦R)', '(HPC outlet temperature) (◦R)']].mean(axis=1)

        # Create a new column for the mean of the Physical fan speed and Physical core speed
        df['mean_speed'] = df[['(Physical fan speed) (rpm)', '(Physical core speed) (rpm)']].mean(axis=1)

        # Create a new column for the mean of the HPC outlet pressure and Bypass-duct pressure
        df['mean_pressure'] = df[['(HPC outlet pressure) (psia)', '(bypass-duct pressure) (psia)']].mean(axis=1)
        df['temp_diff'] = df['(HPC outlet temperature) (◦R)'] - df['(LPC outlet temperature) (◦R)']

    # Calculate the ratio of fuel flow to Ps30
        df['fuel_ratio'] = df['(Ratio of fuel flow to Ps30) (pps/psia)'] / df['(HPC outlet pressure) (psia)']

        # Calculate the ratio of corrected fan speed to physical fan speed
        df['fan_ratio'] = df['(Corrected fan speed) (rpm)'] / df['(Physical fan speed) (rpm)']

        # Calculate the ratio of corrected core speed to physical core speed
        df['core_ratio'] = df['(Corrected core speed) (rpm)'] / df['(Physical core speed) (rpm)']

        return df
    except Exception as e:
            raise exception.CustomException(e,sys)
# Create a module that has a function that creates RUL column, 
# function that searches for columns with .nunique()==1 and drops them 
def preprocess(df):
    
    """ 
    Preprocesses the dataframe by creating a RUL column and dropping 
    columns with only one unique value. 

    Parameters: 
    df (pandas.DataFrame): The dataframe to preprocess. 

    Returns: 
    pandas.DataFrame: The preprocessed dataframe. 
    """ 

    # Create RUL column 
    df = create_RUL_column(df) 
    #engineer new features
    #df=feature_engineer(df)

    # Drop constant columns 
    df = drop_constant_columns(df) 

    return df 

  
# Preprocess the dataframe dd 
 

