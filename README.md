# Visualizing-Scraped-Google-Play-Store-Data-to-Gain-Insight-into-Android-App-Market

**Introduction:**

The increasing use of smartphones has encouraged developers to create more and more mobile apps, on both platforms; android and ios. Around 70% of the mobile phones used by people are based on Android, making it more popular among people. In this project, we will be exploring data from the Google Play Store to gain insights regarding the apps and their popularity based on their specifications.

**Exporting and Import dataset using GridDB:**

GridDB is a highly scalable and in-memory No SQL database that allows parallel processing for higher performance and efficiency, especially for our vast dataset. It is optimized for time-series databases for IoT and big data technologies. We can easily connect GridDB to python and use it to import or export data in real-time, with the help of the GridDB-python client.

Setup GridDB:

First and foremost, we need to make sure that we have properly installed GridDB on our system. Our step-by-step guide available on the website can assist you with setting up GridDB on different operating systems.

Dataset:

We will be using the dataset from the google play store stored in the CSV &#39;apps.csv&#39;. It contains all the details of the applications on Google Play. 13 features describe a given app, including its rating, size, and number of downloads.

Preprocessing:

Before exporting the data to the GridDB platform, we will perform some preprocessing tasks to clean our data for optimal performance by GridDB. We will read the raw data available to us as CSV file.

```python
apps_with_duplicates = pd.read_csv('datasets/apps.csv')    
```

We have our dataset saved as a dataframe to start the cleaning process. We would be removing some duplicates and null values from the apps dataset. We would also drop some columns that are not required for our analysis in this project and reset the index column to avoid discrepancies in our data.

```python
apps = apps_with_duplicates.drop_duplicates()
apps.dropna(inplace=True)
apps.drop_columns(['Content Rating', 'Last Updated', 'Current Ver', 'Android Ver'])   
apps.reset_index(drop=True, inplace=True)
apps.index.name = 'ID' 
```

The last step before storing the dataset is to remove the special characters from our dataset to be able to easily read our numerical data. We have a list of special characters already known that we would remove from our numerical columns.


```python
# List of characters to remove
chars_to_remove = ['+', ',', 'M', '$']
# List of column names to clean
cols_to_clean = ['Installs', 'Size', 'Price']



# Loop for each column
for col in cols_to_clean:
    # Replace each character with an empty string
    for char in chars_to_remove:
        #print(col)
        #print(char)
        apps[col] = apps[col].astype(str).str.replace(char, '')
    apps[col] = pd.to_numeric(apps[col])

```
We will save the dataframes as local copies on our device before uploading them on GridDB.

```python
apps.to_csv("apps_processed.csv")
```

Exporting Dataset into GridDB:

Now we will upload the data to GridDB. For that, we will read the processed CSV files from the local drive and save them to different dataframes.

Now, we will create a container to pass our column info of apps to the GridDB to be able to generate the design of the database before inserting the row information.

After completing the schema, we will insert our row-wise data into the GridDB.

The data is now successfully uploaded to the GridDB platform.

Importing Dataset from GridDB:

We can easily extract the data from GridDB by creating the container and querying the relevant rows using TQL commands, a query language similar to SQL. We will use different containers and variables to store the two datasets separately.

Our data is now ready to be used for analysis.

**Data Analysis and Visualization:**

We will start our analysis by exploring the dataset and understanding a few characteristics of the dataset.

1. The Total number of distinct apps in our dataset.
2. Most expensive app
3. Total number of categories in our dataset
4. Average app rating

We will continue our analysis by plotting some graphs against different specifications of an application. For example, we will start by dividing the apps into categories and then plotting the number of apps in each category to explore the most popular category among apps on the play store.

We would then use our dataset to gain insights about user preference for the cost of the app. There are two types of apps available on Google Playstore, mostly are free which means they cost $0, while some are paid apps. Let us compare the number of installs for paid applications vs free applications.

The results are as expected. People tend to download applications that are free and are usually reluctant to pay for them unless necessary.

We will compare the price of the app across different categories. Selecting a few popular categories out of our dataset then plotting it across the apps with prices lesser than $100 would give us a better understanding of the pricing strategy used while developing mobile applications.

We can see that most of the expensive apps belong to the business or medical field, while apps belonging to games, tools, or photography categories lie under $20. This is because of the selected users for which the application is specified. Most of the games of tools or photography applications are designed for leisure purposes and people tend to think twice to spend money on these applications. They generate revenues mostly through ads and/or third-party collaborations.

**Conclusion:**

We can conclude that the developing application is as important as other aspects of the product management including setting the price and targeting the audience. All of the analysis was done using the GridDB database at the backend, making the integration seamless and efficient.
