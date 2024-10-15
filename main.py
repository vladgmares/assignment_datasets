import pandas as pd

fb_df = pd.read_csv('./datasets/facebook_dataset.csv', sep=',',
                    quotechar='"', escapechar='\\', doublequote=False)
fb_df_2 = pd.read_csv('./datasets/facebook_dataset.csv', sep=',',
                      on_bad_lines='skip')
google_df = pd.read_csv('./datasets/google_dataset.csv', sep=',',
                        on_bad_lines='skip',
                        dtype={'phone': str})
website_df = pd.read_csv('./datasets/website_dataset.csv',
                         sep=';', on_bad_lines='skip')

fb_variables = fb_df.columns.tolist()
google_variables = google_df.columns.to_list()
website_variables = website_df.columns.to_list()


def missing_values_table(df):
    missing_values = df.isnull().sum()
    total_rows = len(df)
    percent_missing = (missing_values / total_rows) * 100

    result = pd.concat(
        [missing_values, percent_missing],
        axis=1,
        keys=["# Missing", "% of Total"]
    )
    result = result[result["% of Total"] != 0]
    result = result.sort_values("% of Total",
                                ascending=False).round(1)

    columns_without_missing_values = list(df.columns[missing_values == 0])
    # Print a summary message
    num_columns = df.shape[1]
    num_missing_columns = result.shape[0]
    print(f"The DataFrame has {num_columns} columns.")
    print(f"There are {num_missing_columns} columns that have missing values.")
    print(f"Best candidates: {columns_without_missing_values} "
          f"without any missing values")
    return result


print("-" * 10 + "Facebook" + "-" * 10)
pd.DataFrame.to_csv(missing_values_table(fb_df),
                    "./output/fb_missing_results.csv")
print("-" * 10 + "Google" + "-" * 10)
pd.DataFrame.to_csv(missing_values_table(google_df),
                    "./output/gg_missing_results.csv")
print("-" * 10 + "Website" + "-" * 10)
pd.DataFrame.to_csv(missing_values_table(website_df),
                    "./output/wb_missing_results.csv")


def renaming_columns(df: pd.DataFrame, suffix, excluded):
    df_columns = df.columns.to_list()
    renaming_dict = {x: x + suffix for x in df_columns if x not in excluded}
    df.rename(columns=renaming_dict, inplace=True)


renaming_columns(fb_df, "_fb", ["domain"])
renaming_columns(google_df, "_gg", ["domain"])

# First merge
fb_google_merged_by_domain = fb_df.merge(google_df, left_on="domain",
                                         right_on="domain")
fb_google_merged_by_domain.to_csv("./output/fb_google_merged.csv",
                                  sep=",", quotechar='"')

# 2nd merge
website_df.rename(columns={"root_domain": "domain"}, inplace=True)
renaming_columns(website_df, "_wb", ["domain"])

final_merge_df = fb_google_merged_by_domain.merge(website_df, left_on="domain",
                                                  right_on="domain")
final_merge_df.to_csv("./output/final_merged.csv",
                      sep=",", quotechar='"', index=False)
