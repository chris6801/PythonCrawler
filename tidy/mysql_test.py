import mysql.connector

# Establish a connection to the MySQL server
db = mysql.connector.connect(
    host='localhost',
    user='chris',
    password='password',
    database='chris'
)

# Create a cursor object
cursor = db.cursor()

cursor.execute("INSERT INTO test(name, age) values ('robin', 47)")

# Execute SQL query
cursor.execute("SELECT * FROM test")

# Fetch all rows
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
db.close()