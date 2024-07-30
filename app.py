import subprocess
import sqlite3

# Configure db
connection = sqlite3.connect("sysinfo.db")

# Cursor 
crsr = connection.cursor()

print("Connected to database!")

def get_sysinfo():
    # Run the systeminfo command
    systeminfo_cmd = "systeminfo"
    output = subprocess.Popen(systeminfo_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = output.communicate()
    
    if stderr:
        print("Error occurred while fetching system info:", stderr.decode())
        return
    
    # Decode the byte output to string
    output_str = stdout.decode()
    
    # Split the output into lines
    lines = output_str.splitlines()
    
    # Create a dictionary to hold the system info
    system_info = {}
    
    # Populate the dictionary with key-value pairs
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            system_info[key.strip()] = value.strip()
    
    return system_info

def get_cpu_info():
    # Run the wmic command to get CPU info
    cpu_info_cmd = "wmic cpu get Name, NumberOfCores, Status /format:list"
    output = subprocess.Popen(cpu_info_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = output.communicate()
    
    if stderr:
        print("Error occurred while fetching CPU info:", stderr.decode())
        return
    
    # Decode the byte output to string
    output_str = stdout.decode()
    
    # Split the output into lines
    lines = output_str.splitlines()
    
    # Create a dictionary to hold the CPU info
    cpu_info = {}
    
    # Populate the dictionary with key-value pairs
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            cpu_info[key.strip()] = value.strip()
    
    return cpu_info

def get_specific_info(key):
    system_info = get_sysinfo()
    if system_info:
        return system_info.get(key, "Key not found")

def get_specific_cpu_info(key):
    cpu_info = get_cpu_info()
    if cpu_info:
        return cpu_info.get(key, "Key not found")

hostname = get_specific_info("Host Name")

os_name = get_specific_info("OS Name")

sys_model = get_specific_info("System Model")

cpu_name = get_specific_cpu_info("Name")
cpu_status = get_specific_cpu_info("Status")
cpu_cores = get_specific_cpu_info("NumberOfCores")

ram_name = get_specific_info("Total Physical Memory")

sql_createTable = """
CREATE TABLE IF NOT EXISTS computer (
id INTEGER PRIMARY KEY AUTOINCREMENT,
hostname VARCHAR(30),
OS_Name VARCHAR(30),
System_Model VARCHAR(30),
CPU_Name VARCHAR(30),
CPU_Status VARCHAR(30),
CPU_Cores VARCHAR(30),
ram_name VARCHAR(30)
);
"""
crsr.execute(sql_createTable)
print("Table created!")

# Insert data
insert_data = (
    hostname,
    os_name,
    sys_model,
    cpu_name,
    cpu_status,
    cpu_cores,
    ram_name
)

sql_insert = """
INSERT INTO computer (hostname, OS_Name, System_Model, CPU_Name, CPU_Status, CPU_Cores, ram_name)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""
crsr.execute(sql_insert, insert_data)
print("Data has been inserted successfully into the database!")

connection.commit()
connection.close()
print("Changes have been committed!")
