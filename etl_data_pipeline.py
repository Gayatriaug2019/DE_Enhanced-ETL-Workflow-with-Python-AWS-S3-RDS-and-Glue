!pip install boto3
!pip install pymysql

import boto3
import pandas as pd
import sqlalchemy
import pymysql
import logging
import os
import zipfile
import xml.etree.ElementTree as ET
import glob
from datetime import datetime

# ---------------- LOGGING CONFIG ----------------
log_path = "/content/etl_data_pipeline.log"

for handler in logging.root.handlers[:]: 
  logging.root.removeHandler(handler)

logging.basicConfig( 
    filename=log_path, 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s", 
    filemode="w" )

console = logging.StreamHandler()
console.setLevel(logging.INFO) 
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s") 
console.setFormatter(formatter) 
logging.getLogger().addHandler(console)

# ---------------- AWS & RDS CONFIG ----------------
S3_BUCKET = "etl-worflow-3"
RAW_DATA_FOLDER = "Source/"
TRANSFORMED_DATA_FOLDER = "Destination/"

RDS_ENDPOINT = "database-1.c9umasosq86v.eu-north-1.rds.amazonaws.com"
RDS_PORT = "3306"
RDS_USER = "admin"
RDS_PASSWORD = "Canonpassing123"
RDS_DB = "miniproject3"

# ---------------- AWS CLIENT ----------------
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


# ---------------- DATABASE ENGINE ----------------
engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_ENDPOINT}:{RDS_PORT}/{RDS_DB}"
)

# ---------------- STEP 1: UNZIP ----------------
def unzip_local(zip_path, extract_path):
    logging.info("Extracting zip file")
    start = datetime.now()
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    logging.info("Extraction completed in %s", datetime.now() - start)

# ---------------- STEP 2: UPLOAD TO S3 ----------------
def upload_to_s3(file_path, bucket, object_name):
    s3.upload_file(file_path, bucket, object_name)
    logging.info("Uploaded %s to S3", object_name)

# ---------------- STEP 3: DOWNLOAD FROM S3 ----------------
def download_from_s3(bucket, object_name, file_path):
    s3.download_file(bucket, object_name, file_path)
    logging.info("Downloaded %s from S3", object_name)

# ---------------- STEP 4: EXTRACT FILES ----------------
def extract_csv(file_path):
    return pd.read_csv(file_path).to_dict(orient="records")

def extract_json(file_path):
    return pd.read_json(file_path, lines=True).to_dict(orient="records")

def extract_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return [{elem.tag: elem.text for elem in child} for child in root]

def extract_files(folder_path):
    combined_data = []
    for file in glob.glob(f"{folder_path}/*"):
        if file.endswith(".csv"):
            combined_data.extend(extract_csv(file))
        elif file.endswith(".json"):
            combined_data.extend(extract_json(file))
        elif file.endswith(".xml"):
            combined_data.extend(extract_xml(file))
    return combined_data

# ---------------- STEP 5: TRANSFORM ----------------
def transform(data):
    transformed = []
    for record in data:
        new_record = {}
        for k, v in record.items():
            if k == "height" and v:
                new_record[k] = float(v) * 0.0254
            elif k == "weight" and v:
                new_record[k] = float(v) * 0.453592
            else:
                new_record[k] = v
        transformed.append(new_record)
    return transformed

# ---------------- STEP 6: LOAD ----------------
def load_csv(data, output_file):
    pd.DataFrame(data).to_csv(output_file, index=False)
    logging.info("Saved transformed CSV")

def load_to_rds(data, table_name):
    conn = pymysql.connect( host=RDS_ENDPOINT, 
                           user=RDS_USER, 
                            password=RDS_PASSWORD,
                            port=int(RDS_PORT) ) 
    cursor = conn.cursor() 
    cursor.execute("CREATE DATABASE IF NOT EXISTS miniproject3;")
    conn.close()

    pd.DataFrame(data).to_sql(
        table_name,
        con=engine,
        if_exists="replace",
        index=False
    )
    logging.info("Loaded data into RDS table %s", table_name)

# ---------------- MAIN ETL ----------------
if __name__ == "__main__":

    zip_path = "/content/source.zip"       # uploaded zip file
    extract_path = "/content/extracted"
    download_path = "/content/downloaded"
    output_file = "final_transformed_data.csv"

    os.makedirs(extract_path, exist_ok=True)
    os.makedirs(download_path, exist_ok=True)

    unzip_local(zip_path, extract_path)

    # Upload raw files to S3
    for file in os.listdir(extract_path):
        local_path = os.path.join(extract_path, file)
        upload_to_s3(local_path, S3_BUCKET, RAW_DATA_FOLDER + file)

    # Download files back from S3
    for file in os.listdir(extract_path):
        download_from_s3(
            S3_BUCKET,
            RAW_DATA_FOLDER + file,
            os.path.join(download_path, file)
        )

    extracted_data = extract_files(download_path)
    transformed_data = transform(extracted_data)

    if transformed_data:
        load_csv(transformed_data, output_file)
        upload_to_s3(output_file, S3_BUCKET, TRANSFORMED_DATA_FOLDER + output_file)
        load_to_rds(transformed_data, "etl_table")

        logging.info("Data Uploaded to RDS check")

        df = pd.read_sql("SELECT * FROM etl_table LIMIT 10;", con=engine) 
        print(df.head())

    logging.info("ETL Pipeline Completed Successfully")
