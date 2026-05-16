import os
import json
import sqlite3
import pandas as pd
from pypdf import PdfReader
from langchain_core.documents import Document

DATA_DIR = os.path.join("data")
METADATA_FILE = os.path.join(DATA_DIR, "master_metadata.json")

def load_metadata():
    with open(METADATA_FILE, "r") as f:
        return json.load(f)

def parse_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def parse_sqlite(file_path):
    text = "Employee Payroll Records:\n"
    try:
        conn = sqlite3.connect(file_path)
        df = pd.read_sql_query("SELECT * FROM payroll", conn)
        conn.close()
        
        records = df.to_dict(orient="records")
        for row in records:
            text += f"EmpID: {row['emp_id']}, Name: {row['name']}, Dept: {row['department']}, Salary: ${row['salary']}\n"
    except Exception as e:
        print(f"Error reading SQLite {file_path}: {e}")
    return text

def parse_json(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            text = f"Action: {data.get('action')} | Status: {data.get('status')} | "
            text += f"User: {data.get('user_id')} | IP: {data.get('ip_address')} | Time: {data.get('timestamp')}"
            return text
    except Exception as e:
        print(f"Error reading JSON {file_path}: {e}")
        return ""

def load_all_documents():
    metadata_records = load_metadata()
    documents = []

    for record in metadata_records:
        source_type = record.get("source_type")
        file_path = record.get("path")

        if not os.path.exists(file_path):
            print(f"Warning: File not found - {file_path}")
            continue

        content = ""
        if source_type == "pdf":
            content = parse_pdf(file_path)
        elif source_type == "sqlite":
            content = parse_sqlite(file_path)
        elif source_type == "json":
            content = parse_json(file_path)

        if content.strip():
            doc = Document(
                page_content=content,
                metadata={
                    "doc_id": record["doc_id"],
                    "source_type": source_type,
                    "allowed_roles": record["allowed_roles"],
                    "description": record["description"]
                }
            )
            documents.append(doc)

    return documents

if __name__ == "__main__":
    docs = load_all_documents()
    print(f"Successfully parsed {len(docs)} documents.")
    if docs:
        print(f"Sample Metadata: {docs[0].metadata}")
        print(f"Sample Content: {docs[0].page_content[:100]}...")