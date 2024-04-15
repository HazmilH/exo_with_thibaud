# import necessary modules
import argparse
import pandas as pd


# load file to a df 
column_names = ['festival_name', 'project', 'notification_date', 'submission_status', 'judging_status'] 

def load_df(path_to_file):
    try:
        df = pd.read_csv(path_to_file, names=column_names, header = None)
        return df
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        print("An error occurred while loading the data:", e)
        return None


def df_aggregation(df):
    # cast to datetime format
    df['notification_date'] = pd.to_datetime(df['notification_date'])
    # extract year and month 
    df['notification_date_month'] = pd.DatetimeIndex(df['notification_date']).month
    df['notification_date_year'] = pd.DatetimeIndex(df['notification_date']).year
    df_aggregated = pd.DataFrame(df.groupby(by=['notification_date_year', 'notification_date_month'])['festival_name'] \
                             .count() \
                             .reset_index()
                             )
    # rename column  
    df_aggregated.rename(columns={'festival_name' : 'festival_count'}, inplace=True)

    # order by year and then month
    df_aggregated.sort_values([	'notification_date_year', 'notification_date_month'], inplace=True)
    
    return df_aggregated

# Generate data for the remaining years and months without festival
def df_completion(df_aggregated):
    # 1st step : convert to df_aggregated to dictionary in this form --> {(year, month): festival_count}
    # Set the combination of 'notification_date_year' and 'notification_date_month' as index
    df_aggregated.set_index(['notification_date_year', 'notification_date_month'], inplace=True)

    # Convert to a dictionary
    festival_count_dict = df_aggregated['festival_count'].to_dict()

    # 2nd step :
    # Create a list to hold all rows
    festival = []

    # 3rd step :
    # Loop through years and months
    for year in range(2020, 2025):
        for month in range(1, 13):
            # Check if festival count is available for the given year and month
            if (year, month) in festival_count_dict:
                festival_count = festival_count_dict[(year, month)]
            else:
                festival_count = 0
            festival.append([year, month, festival_count])

    # recreate df but this time complete with each year and month
    df_complete = pd.DataFrame(festival, columns=['notification_date_year', 'notification_date_month', 'festival_count'])

    return df_complete    





def quality_check(df_complete):
    # do a "quality check"
    # s'il y a des mois sans festival
    print('year-month without festival :')
    print('-------------------------------')
    for i in range(len(df_complete)):
        if df_complete['festival_count'][i] == 0 :
            print(f"{df_complete['notification_date_year'][i]} - {df_complete['notification_date_month'][i]}")


def main():
    parser = argparse.ArgumentParser(description="Load data from a CSV file")
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    file_path = args.file_path
    df = load_df(file_path)
    df_aggregated = df_aggregation(df) 
    df_complete = df_completion(df_aggregated)

    if df is not None:
        print("Data loaded successfully :")
        print('---------------------------')
        print(df.head(12))  # Example: Display the first few rows of the loaded data
        
        print("\n\nData aggregated by year and month :")
        print('----------------------------------------')
        print(df_complete.head(12))

        print("\n\nQuality check :")
        quality_check(df_complete)

if __name__ == "__main__":
    main()



# # set file location
# path_to_file = '../data/filmfreeway_archived_submission_2024-04-02.csv'

# # load file to a df 
# column_names = ['festival_name', 'project', 'notification_date', 'submission_status', 'judging_status'] 
# df = pd.read_csv(path_to_file, names=column_names, header = None)

# # cast notification_date to datetime
# df['notification_date'] = pd.to_datetime(df['notification_date'])

# # extract year and month 
# df['notification_date_month'] = pd.DatetimeIndex(df['notification_date']).month
# df['notification_date_year'] = pd.DatetimeIndex(df['notification_date']).year

# # count number of festival for each month of each year
# df_aggregated = pd.DataFrame(df.groupby(by=['notification_date_year', 'notification_date_month'])['festival_name'] \
#                              .count() \
#                              .reset_index()
#                              )

# # rename column  
# df_aggregated.rename(columns={'festival_name' : 'festival_count'}, inplace=True)

# # order by year and then month
# df_aggregated.sort_values([	'notification_date_year', 'notification_date_month'], inplace=True)

# Generate data for the remaining years and months without festival

# # 1st step : convert to df_aggregated to dictionary in this form --> {(year, month): festival_count}
# # Set the combination of 'notification_date_year' and 'notification_date_month' as index
# df_aggregated.set_index(['notification_date_year', 'notification_date_month'], inplace=True)
# # Convert to a dictionary
# festival_count_dict = df_aggregated['festival_count'].to_dict()

# # 2nd step :
# # Create a list to hold all rows
# festival = []

# # 3rd step :
# # Loop through years and months
# for year in range(2020, 2025):
#     for month in range(1, 13):
#         # Check if festival count is available for the given year and month
#         if (year, month) in festival_count_dict:
#             festival_count = festival_count_dict[(year, month)]
#         else:
#             festival_count = 0
#         festival.append([year, month, festival_count])

# # recreate df but this time complete with each year and month
# df_complete = pd.DataFrame(festival, columns=['notification_date_year', 'notification_date_month', 'festival_count'])

# # do a "quality check"
# # s'il y a des mois sans festival
# print('year-month without festival : \n---------------------------')
# for i in range(len(df_complete)):
#     if df_complete['festival_count'][i] == 0 :
#         print(f"{df_complete['notification_date_year'][i]} - {df_complete['notification_date_month'][i]}")