# Assignment

I decided to use the pandas library (I had some experience with it, using that for a course in University) and create a DataFrame for each dataset.

Project uses Python 3.8.19 and the requirements.txt file contains all dependencies (run `pip install -r requirements.txt`). First unzip the datasets.zip file. Run main.py to produce the output directory.

### Reading data:

* Given there were some parsing errors (related to separators and escaping characters) with facebook and google sets, 
as some column content had a mix of single and double quotes and unescaped comas, 
such that the read_csv() method was interpreting them as extra columns; To fix this I worked out
one solution for the facebook DataFrame (to specify quotechar and escapechar parameters) and
a different one for google (using the on_bad_lines specifier to skip
the wrongly formatted rows); the solutions work interchangeably;
* The website dataset was easier to manage, since it only had a different separator format;

### Processing:
* I extracted the variables (columns) for each dataframe;
* To help me select a field for merging the data, I thought one way is
to determine, for each set, what column has the least percentage of missing values, thinking that holds
the key to determine the best common candidate(s);
* The function missing_values_table() does this and the results for each DataFrame is available in output directory;
* The results indicated that the domain column (or “root_domain” for website dataset) ranked highest, with various others for each dataset subsequently;
* I decided to merge the facebook and google datasets on domain (method being “inner” similar to the SQL inner join) and append suffixes for each set’s column accordingly, to aid in further analysis); for this purpose I wrote a renaming_columns() function (I chose not to use the “suffixes” parameter for the pandas.merge() in order to keep track correctly of the column's origin).
* The result for this merge is available in the output directory ("fb_google_merged.csv");
* Next I opted for merging this intermediary dataframe on domain column again (I renamed the “root_domain” column in the website dataset for readability) with website_df using an “inner” merge; also used the renaming function before this to add the appropriate suffix to the website_df columns;
* The final resulting dataset (“final_merged.csv”) can be found in the output directory.
* The reason for choosing "inner" merge both times, was to get the most complete dataset from the 3 inputs and limit data loss;
#### I can note some ideas that I have given this final quite large dataset:
1. I ended up with this dataset thinking that, it’s better to have all the variables there(with proper origin suffixes for each column);
2. Duplicates can be eliminated from the result depending on more detailed requirements, for example:
   * keeping a single phone number column with the international format (most complete) by comparing columns from all 3 sets; In the google dataset, the "raw_phone" has the least incidence of missing values (8.1%) but is not very nicely formatted. Compared to the website dataset where the "phone" column has about 8.9% missing values (but the format is better) and the facebook data where "phone" is missing in about 38% of cases, makes me likely to decide between the google and website data for best accuracy;
   * regarding the addresses, we can keep only the lowercase country name as a column and decide based on multiple validation using other fields such as: country_code, phone_country_code or even domain_suffix (as this has the least missing values % at 0.2% in the website dataset); another option here can also be to keep both country and country_code to help with querying the data easier;
   * for Categories, I see that it can be extracted from the "text" column in google data (since this looks like an aggregated description from scraping typical google details) that has just 1% missing values, and compare that to the "s_category" in website data at 2% missing values; 
3. Employ some tools for text comparison in all those cases; I did some research and found certain libraries in python, like fuzzywuzzy, that can aid in deciding what columns to drop or keep, not based on boolean comparison (not that helpful in those cases), but rather on a probability [0, 1] that two patterns match.
