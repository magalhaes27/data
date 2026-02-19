# Premier League Data Pipeline

This project automates the process of extracting data from football website, converting it to Parquet format, and uploading it to Azure Blob Storage. The pipeline is designed to work with multiple data extraction functions, making it modular and reusable.

## Features
- Extracts data using user-defined functions.
- Converts data (Pandas DataFrame) to Parquet format using Apache Arrow.
- Uploads the Parquet file to Azure Blob Storage.
- Supports environment variables for secure configuration.

## How It Works
1. Define your data extraction functions (e.g., `top_scorers`, `player_table`).
2. Use the `to_blob` function to process the data:
   - Converts the data to an Arrow Table.
   - Serializes the Arrow Table to Parquet format.
   - Uploads the Parquet file to Azure Blob Storage.
3. The function name is used as the blob name in the storage container.

## Prerequisites
- Python 3.9 or higher
- Azure Blob Storage account
- Required Python packages (see `requirements.txt`)

## Installation
1. Clone the repository:
   ```bash git clone 
