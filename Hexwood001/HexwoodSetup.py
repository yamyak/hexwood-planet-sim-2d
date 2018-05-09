import mysql.connector


# connect to the mysql database
def openDB():
	cnx = mysql.connector.connect(user='', password='', host='')
	cursor = cnx.cursor()
	return cnx, cursor
	
# create database tables
def createTables(cursor):
  # create table for planet data
	table_cmd = ('CREATE TABLE `data` '
                 '( `id` INTEGER, `name` VARCHAR(30), `period_time` FLOAT, `mean_anomaly` FLOAT, `eccentric_anomaly` FLOAT, '
                 '`radius` FLOAT, `angle` FLOAT, `x_location` FLOAT, `y_location` FLOAT )')
	cursor.execute(table_cmd)
  # create table for thread status
	table_cmd = ('CREATE TABLE `status` '
                 '( `id` INTEGER, `name` VARCHAR(30), `dead` BOOLEAN )')
	cursor.execute(table_cmd)
	
# insert planet and thread data into database
def loadData(cursor):
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (1, "Mercury", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (2, "Venus", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (3, "Earth", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (4, "Mars", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (5, "Jupiter", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (6, "Saturn", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (7, "Uranus", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (8, "Neptune", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `data` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
	row_data = (9, "Pluto", 0, 0, 0, 0, 0, 0, 0)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (0, "All", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (1, "Mercury", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (2, "Venus", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (3, "Earth", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (4, "Mars", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (5, "Jupiter", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (6, "Saturn", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (7, "Uranus", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (8, "Neptune", False)
	cursor.execute(row_cmd, row_data)
	
	row_cmd = ('INSERT INTO `status` VALUES (%s, %s, %s)')
	row_data = (9, "Pluto", False)
	cursor.execute(row_cmd, row_data)

# create database tables and insert data
def loadDatabase(cnx, cursor):
	cnx.database = ''
	createTables(cursor)
	cnx.commit()
	loadData(cursor)
	cnx.commit()

# initialize the database
if __name__ == '__main__':
	cnx, cursor = openDB()
	loadDatabase(cnx, cursor)
	cursor.close()
	cnx.close()
