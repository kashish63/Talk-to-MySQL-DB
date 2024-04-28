import mysql.connector

# Replace with your connection details

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="DATABASE"
)


print(mydb.get_server_info())

# Create a cursor object
mycursor = mydb.cursor()

myquery = "UPDATE USERS SET PASSWORD='1234567' WHERE NAME='Vibhu'"

mycursor.execute(myquery)

# Fetch results (optional)
# Depending on your query type, you might need to use fetch methods
# like fetchone(), fetchall(), or fetchmany()

# Example: fetch all rows
myresult = mycursor.fetchall()

print(mycursor.rowcount)

# Print the results (optional)
for row in myresult:
  print(row)

# Close the connection
mydb.close()


