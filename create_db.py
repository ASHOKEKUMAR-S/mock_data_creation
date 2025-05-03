import mysql.connector
import random
import uuid
import dotenv
import os
dotenv.load_dotenv()


# Sample data pools
applications = ['sales', 'order', 'web', 'inventory', 'support']
environments = ['dev', 'qa', 'prod', 'stage']
os_types = ['linux', 'windows']
os_versions = {
    'linux': ['7.9', '8.1', '8.2', '8.5', '9.0'],
    'windows': ['2016', '2019', '2022']
}
tech_stacks = ['Oracle', 'WebLogic', 'Kafka', 'ElasticSearch', 'MySQL', 'Tomcat']
mysql_password=os.getenv('MYSQL_PASSWORD')

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',      # Change as needed
    user='admin',      # Change as needed
    password=mysql_password,  # Change as needed 
    database='cmdb'
)

cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(64),
    hostname VARCHAR(64),
    application VARCHAR(32),
    environment VARCHAR(16),
    os_type VARCHAR(16),
    os_version VARCHAR(16),
    tech_stack VARCHAR(64)
)
""")

# Insert 1000 records
for _ in range(1000):
    device_id = str(uuid.uuid4())
    hostname = f"host-{random.randint(1000, 9999)}"
    application = random.choice(applications)
    environment = random.choice(environments)
    os_type = random.choice(os_types)
    os_version = random.choice(os_versions[os_type])  # Logical mapping
    tech_stack = random.choice(tech_stacks)

    cursor.execute("""
        INSERT INTO devices (device_id, hostname, application, environment, os_type, os_version, tech_stack)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (device_id, hostname, application, environment, os_type, os_version, tech_stack))

conn.commit()
cursor.close()
conn.close()

print("✅ 1000 logically consistent records inserted.")
