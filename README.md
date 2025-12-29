# ☁️ Enhanced ETL Workflow with Python, AWS S3, RDS, and Glue

## 📌 Project Overview
This project implements an **enhanced ETL (Extract, Transform, Load) pipeline** using **Python** and **AWS cloud services**, executed on **Google Colab**.  
The pipeline processes data from multiple file formats (**CSV, JSON, XML**), applies transformations, and loads the processed data into **AWS S3** and **AWS RDS** for persistent storage and further analytics.

The project optionally leverages **AWS Glue** to automate schema discovery and transformation, demonstrating a scalable and production-oriented cloud ETL workflow.

---

## 🧰 Technologies Used
- **Programming Language:** Python  
- **Execution Platform:** Google Colab  
- **Cloud Provider:** AWS  

### AWS Services
- **Amazon S3** – Raw and transformed data storage  
- **Amazon RDS (MySQL / PostgreSQL)** – Relational data storage  
- **AWS Glue (Optional)** – Schema inference and ETL automation  

### Libraries
- `pandas` – Data manipulation  
- `boto3` – AWS SDK for S3 and RDS interaction  
- `sqlalchemy` – Database connectivity  
- `logging` – ETL process monitoring  

---

## 📊 Data Formats
- CSV  
- JSON  
- XML  

---

## 🎯 Project Objectives
By completing this project, the following objectives are achieved:
- Extract data from CSV, JSON, and XML files
- Transform raw data, including unit conversions:
  - Height: inches ➜ meters  
  - Weight: pounds ➜ kilograms  
- Load transformed data into **AWS S3** and **AWS RDS**
- (Optional) Automate transformations using **AWS Glue**
- Implement logging for ETL traceability and monitoring

---

## 📥 Dataset
The dataset used in this project is provided by **IBM Skills Network**.

### Download Dataset
```bash
Data source - https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/source.zip

Extract Dataset
bash
unzip source.zip -d unzipped_folder
Note: In Google Colab, use !wget and !unzip commands.

📂 Project Structure
powershell
enhanced-etl-aws/
│
├── content/            #colab folder 
│   └── Source/        # Raw CSV, JSON, XML files
|   └── Destination/ 
│
├── logs/
│   └── etl_data-pipeline.log              # ETL execution logs
│
├── scripts/
│   └── etl_data_pipeline.py          # Main ETL pipeline
│
├── final_transformed_data.csv         # Final transformed output
└── README.md                    # Project documentation

🛠️ Step-by-Step Workflow

1️⃣ Step 1: Data Collection
Download ZIP dataset
Extract CSV, JSON, and XML files locally
Upload raw files to Amazon S3

2️⃣ Step 2: AWS Setup
Amazon S3
Create an S3 bucket (e.g., my-etl-project-bucket)
Store:
Raw input files
Transformed output files
Optional ETL logs
Amazon RDS
Create RDS instance (MySQL / PostgreSQL
Configure security groups for access
Create target table for transformed data
AWS Glue (Optional)
Configure Glue crawler for schema detection
Automate transformation jobs from S3

3️⃣ Step 3: ETL with AWS Integration
Extraction
Download raw files from S3
Read CSV, JSON, and XML data using pandas
Transformation
Apply unit conversions
Clean and standardize data
Prepare data for relational storage
Loading
Upload transformed CSV to S3
Load transformed data into AWS RDS using SQLAlchemy

4️⃣ Step 4: Logging
Log each ETL phase:
Extraction
Transformation
Loading
Store logs locally and optionally upload to S3

5️⃣ Step 5: Execution Sequence
Upload raw data to S3
Extract and transform data from S3
Upload transformed output to S3
Load final dataset into AWS RDS
Monitor logs for pipeline health

▶️ How to Run the Project (Google Colab)
Open Google Colab
Upload the project files
Configure AWS credentials using environment variables
Run dataset download and extraction cells
Execute the ETL pipeline script
Verify:
Transformed data in S3
Data loaded into RDS
Logs generated successfully

📈 Output
Amazon S3
Raw data files
transformed_data.csv
Amazon RDS
Relational table with transformed data

Logs
Timestamped ETL execution logs


👤 Author
Gayatri
Python Backend Engineer | Data Engineer
