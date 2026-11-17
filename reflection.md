For this assignment, I created a Fake Trillionaire E-Commerce API and a unified ETL pipeline using Python. I started by setting up the source API to provide item and order information through REST and SOAP services. I then created the ETL pipeline to retrieve the data, transform it, and store it in a SQLite database.

One challenge I encountered was getting the Spyne library to work correctly. I had to troubleshoot compatibility errors before the source API would run. I also learned how important it is to keep the original source data unchanged while applying transformations in the unified database.

I updated the database model to store SKU IDs as strings and modified the transformation code to add the prefix “SPTBG-” to each ID. I used curl commands to test the APIs and confirmed that both items and orders returned the transformed values successfully.

This assignment helped me better understand how REST, SOAP, and ETL pipelines work together. I would like to learn more about handling larger datasets and automating ETL processes.