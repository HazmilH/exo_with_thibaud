# import necessary modules
import argparse
import pandas as pd


# list of column names

column_names = ['festival_name', 'project', 'notification_date', 'submission_status', 'judging_status'] 

def load_df(path_to_file):
    """Load dataframe from csv file

    Parameters
    ----------
    path_to_file : str
        Location of csv file


    Returns
    -------
    pandas dataframe 
    with df.columns = ['festival_name', 'project', 'notification_date', 'submission_status', 'judging_status'] 
    """
    try:
        df = pd.read_csv(path_to_file, names=column_names, header = None, index_col=False)
        return df
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        print("An error occurred while loading the data:", e)
        return None



def df_aggregation(df):
    """Aggregate and group by dataframe based on year and month

    Parameters
    ----------
    df : pandas dataframe 
    with df.columns = ['festival_name', 'project', 'notification_date', 'submission_status', 'judging_status'] 


    Returns
    -------
    pandas dataframe 
    with df_aggregated.columns = ['notification_date_year', 'notification_date_month', 'festival_count'] 
    """
    # cast 'notification_date' column to datetime format
    df['notification_date'] = pd.to_datetime(df['notification_date'])
    
    # extract year and month from it
    df['notification_date_year'] = pd.DatetimeIndex(df['notification_date']).year
    df['notification_date_month'] = pd.DatetimeIndex(df['notification_date']).month    

    # count festival number based on year and month
    df_aggregated = pd.DataFrame(df.groupby(by=['notification_date_year', 'notification_date_month'])['festival_name'] \
                             .count() \
                             .reset_index()
                             )
    # rename column  
    df_aggregated.rename(columns={'festival_name' : 'festival_count'}, inplace=True)

    # order by year and then month
    df_aggregated.sort_values([	'notification_date_year', 'notification_date_month'], inplace=True)
    
    return df_aggregated



def df_completion(df_aggregated):
    """Generate data for the remaining years and months without festival

    Parameters
    ----------
    df_aggregated : pandas dataframe 
    with df_aggregated.columns = ['notification_date_year', 'notification_date_month', 'festival_count'] 


    Returns
    -------
    pandas dataframe 
    with df_completed.columns = ['notification_date_year', 'notification_date_month', 'festival_count'] 
    """

    # 1st step : convert to df_aggregated to dictionary in this form --> {(year, month): festival_count}
    # Set the combination of 'notification_date_year' and 'notification_date_month' as index
    df_aggregated.set_index(['notification_date_year', 'notification_date_month'], inplace=True)

    # 2nd step : convert to a dictionary
    festival_count_dict = df_aggregated['festival_count'].to_dict()

    # 3rd step :
    # Create a list to hold all rows
    festival = []

    # 4th step :
    # Loop through years and months
    for year in range(2020, 2025):
        for month in range(1, 13):
            # Check if festival count is available for the given year and month
            if (year, month) in festival_count_dict:
                festival_count = festival_count_dict[(year, month)]
            else:
                festival_count = 0
            festival.append([year, month, festival_count])

    # dataframe with every year and month including non festival year-month
    df_completed = pd.DataFrame(festival, columns=['notification_date_year', 'notification_date_month', 'festival_count'])

    return df_completed    



def quality_check(df_completed):
    """Execute quality check - 
    In this case, the confition is to
        - find year-month without festival
        - ....

    Parameters
    ----------
    df_completed : pandas dataframe 
    with df_completed.columns = ['notification_date_year', 'notification_date_month', 'festival_count'] 


    Returns
    -------
    string : year-month without festival

    """

    print('year-month without festival :')
    print('-------------------------------')
    for i in range(len(df_completed)):
        if df_completed['festival_count'][i] == 0 :
            print(f"{df_completed['notification_date_year'][i]} - {df_completed['notification_date_month'][i]}")



def main():
    parser = argparse.ArgumentParser(description="Load data from a CSV file")
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    path_to_file = args.file_path
    df = load_df(path_to_file)
    df_aggregated = df_aggregation(df) 
    df_completed = df_completion(df_aggregated)

    if df is not None:
        print("\n\nData loaded successfully :")
        print('---------------------------')
        print(df.head(24).to_string(index=False))  # Display the first 24 rows of the loaded data
        
        print("\n\nData aggregated by year and month :")
        print('----------------------------------------')
        print(df_completed.head(24).to_string(index=False)) # Display the first 24 rows of the loaded data

        print("\n\nQuality check :")
        print('--------------------')
        quality_check(df_completed) # Display all months without festival

if __name__ == "__main__":
    main()
