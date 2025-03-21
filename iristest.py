import iris

# Open a connection to the server
args = {
	'hostname':'127.0.0.1', 
	'port': 56117,
	'namespace':'IRISAPP', 
	'username':'SuperUser', 
	'password':'SYS'
}
conn = iris.connect(**args)

# Create an iris object
irispy = iris.createIRIS(conn)

try:
    # Create a global array in the USER namespace on the server
    irispy.set('teste', 'myGlobal2') 
    # Read the value from the database and print it
    print(irispy.get("myGlobal2"))
    # Delete the global array and terminate
    #irispy.kill("myGlobal") 
except Exception as e:
    print(f"Error performing Intersystems IRIS operation: {str(e)}")

conn.close()