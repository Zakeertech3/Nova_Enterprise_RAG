import os
import json
import sqlite3
import random
import pandas as pd
from fpdf import FPDF
from faker import Faker

fake = Faker()

DATA_DIR = os.path.join("data")
HR_DIR = os.path.join(DATA_DIR, "hr_legal")
FIN_DIR = os.path.join(DATA_DIR, "finance_ops")
IT_DIR = os.path.join(DATA_DIR, "it_security")
METADATA_FILE = os.path.join(DATA_DIR, "master_metadata.json")

metadata = []

def setup_dirs():
    for d in [HR_DIR, FIN_DIR, IT_DIR]:
        os.makedirs(d, exist_ok=True)

def generate_hr_pdfs(num_docs=5):
    roles = [["Standard_Employee", "Finance_Analyst", "IT_Admin", "Super_Admin"], ["Super_Admin"]]
    for i in range(num_docs):
        doc_id = f"hr_doc_{i}"
        is_confidential = random.choice([True, False])
        allowed = roles[1] if is_confidential else roles[0]
        title = "Executive Compensation Contract" if is_confidential else "Employee Handbook Update"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=title, ln=1, align='C')
        pdf.multi_cell(0, 10, txt=fake.text(max_nb_chars=1000))
        
        filepath = os.path.join(HR_DIR, f"{doc_id}.pdf")
        pdf.output(filepath)
        
        metadata.append({
            "doc_id": doc_id,
            "source_type": "pdf",
            "path": filepath,
            "allowed_roles": allowed,
            "description": title
        })

def generate_finance_data(num_rows=50):
    db_path = os.path.join(FIN_DIR, "nova_corp.db")
    conn = sqlite3.connect(db_path)
    
    data = []
    for _ in range(num_rows):
        data.append({
            "emp_id": fake.unique.random_number(digits=5),
            "name": fake.name(),
            "department": random.choice(["Engineering", "Sales", "Marketing", "HR"]),
            "salary": random.randint(50000, 150000)
        })
    
    df = pd.DataFrame(data)
    df.to_sql("payroll", conn, if_exists="replace", index=False)
    
    csv_path = os.path.join(FIN_DIR, "payroll_export.csv")
    df.to_csv(csv_path, index=False)
    
    conn.close()
    
    doc_id = "finance_db_0"
    metadata.append({
        "doc_id": doc_id,
        "source_type": "sqlite",
        "path": db_path,
        "allowed_roles": ["Finance_Analyst", "Super_Admin"],
        "description": "Employee Payroll Database"
    })

def generate_it_logs(num_logs=10):
    for i in range(num_logs):
        doc_id = f"it_log_{i}"
        log_data = {
            "timestamp": fake.iso8601(),
            "ip_address": fake.ipv4(),
            "user_id": fake.user_name(),
            "action": random.choice(["VPN_LOGIN", "SERVER_ACCESS", "FAILED_LOGIN", "DATA_EXPORT"]),
            "status": random.choice(["SUCCESS", "FAILURE"])
        }
        
        filepath = os.path.join(IT_DIR, f"{doc_id}.json")
        with open(filepath, "w") as f:
            json.dump(log_data, f, indent=4)
            
        metadata.append({
            "doc_id": doc_id,
            "source_type": "json",
            "path": filepath,
            "allowed_roles": ["IT_Admin", "Super_Admin"],
            "description": f"System log for {log_data['action']}"
        })

def save_metadata():
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    setup_dirs()
    generate_hr_pdfs()
    generate_finance_data()
    generate_it_logs()
    save_metadata()