# ETL Pipeline for Environmental Crime Analysis in Colombia
This project implements an ETL (Extract, Transform, Load) pipeline to process environmental crime data in Colombia. It is designed to extract data from a public JSON source, transform it for analysis, and load it into both a PostgreSQL database and Amazon S3 for cloud storage.

# Data Source
The data used in this ETL pipeline comes from the [Environmental Crimes Dataset](https://www.datos.gov.co/Seguridad-y-Defensa/DELITOS-CONTRA-EL-MEDIO-AMBIENTE/9zck-qfvc/about_data), which provides information on various environmental crimes reported across Colombia.

# Steps and technologies
## 1. Data Extraction
  * **API Integration:** Uses the ```requests``` library to retrieve data from the open API, ensuring data freshness with each pipeline run.
  * **Error Handling:** Implements robust exception handling to manage connectivity issues and data inconsistencies during extraction.

## 2. Data Transformation
  * **DataFrame Manipulation:** Applies ```pandas``` to clean and reshape the data for analysis. Column names are standardized, and data types are adjusted to enhance usability.
  * **Date Parsing:** Converts date fields into a consistent format, facilitating accurate analysis and storage.

## 3. Data Loading
  * **PostgreSQL Loading:** Configures and loads transformed data into a PostgreSQL database using ```psycopg2```. If the table does not exist, it is created, ensuring seamless integration.
  * ** AWS S3 Storage:** Uploads processed data to an Amazon S3 bucket, making it accessible for downstream applications and analytics.

## 4. Logging and Monitoring
  * **Centralized Logging:** Sets up a logging system to track the progress of each ETL step. Logs are saved both to the console and to a file, enabling troubleshooting and monitoring.

## 5. Unit Testing
  * **Automated Testing for ETL Stages:** Uses ```unittest``` and ```unittest.mock``` to validate each ETL phase, ensuring data integrity and reliability. The tests cover extraction, transformation, and loading functions, simulating various scenarios.

## 6. AWS Lambda Integration
The ```aws-etl``` directory contains code to deploy the ETL pipeline on AWS Lambda, enabling automatic data updates in the cloud.
