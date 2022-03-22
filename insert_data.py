import griddb_python as griddb
import sys
import pandas as pd

factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    
    
    apps_with_duplicates = pd.read_csv('datasets/apps.csv')
    reviews = pd.read_csv('datasets/user_reviews.csv')
    
    apps = apps_with_duplicates.drop_duplicates()
    apps.drop_columns(['Content Rating', 'Last Updated', 'Current Ver', 'Android Ver'])   
    apps.dropna(inplace=True)
    apps.reset_index(drop=True, inplace=True)
    apps.index.name = 'ID'

        
    apps.to_csv("appdata_processed.csv")

    #read the cleaned data from csv
    appdata = pd.read_csv("appdata_processed.csv")

    for row in appdata.itertuples(index=False):
            print(f"{row}")

    # View the structure of the data frames
    appdata.info()

    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    #Create container 
    appdata_container = "appdata_container"

    # Create containerInfo
    appdata_containerInfo = griddb.ContainerInfo(appdata_container,
                    [["ID", griddb.Type.INTEGER],
        		    ["App", griddb.Type.STRING],
         		    ["Category", griddb.Type.STRING],
                    ["Rating", griddb.Type.FLOAT],
                    ["Reviews", griddb.Type.FLOAT],
         		    ["Size", griddb.Type.FLOAT],
                    ["Installs", griddb.Type.STRING],
                    ["Type", griddb.Type.STRING],
                    ["Price", griddb.Type.FLOAT],
         		    ["Genres", griddb.Type.FLOAT]],
                    griddb.ContainerType.COLLECTION, True)
    
    appdata_columns = gridstore.put_container(appdata_containerInfo)
    
    # Put rows
    appdata_columns.put_rows(appdata)
    
    print("App Data Inserted using the DataFrame")

except griddb.GSException as e:
    print(e)
    for i in range(e.get_error_stack_size()):
        print(e)
        # print("[", i, "]")
        # print(e.get_error_code(i))
        # print(e.get_location(i))
        print(e.get_message(i))
