import mysql.connector
import sys
import time

def openDB():

	cnx = mysql.connector.connect(user='hex', password='hex0nmysQl', host='localhost')
	cursor = cnx.cursor()
	cnx.database = 'hexwood001'
	
	return cnx, cursor

if __name__ == '__main__':

	cnx, cursor = openDB()
	
	planets = [ "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto" ]
	planetName = str(sys.argv[1])
	
	if planetName in planets:
		query = ('UPDATE status SET `dead` = %s WHERE name = %s')
		data  = (True, planetName)
		cursor.execute(query, data)
		cnx.commit()
		output = planetName + " Stopped"
		print output

		time.sleep(0.3)
		query = ('UPDATE status SET `dead` = %s WHERE name = %s')
		data = (False, planetName)
		cursor.execute(query, data)
		cnx.commit()
	elif planetName == "All":
		query = ('UPDATE status SET `dead` = %s WHERE id = %s')
		data  = (True, 0)
		cursor.execute(query, data)
		cnx.commit()
		print "All Planets Stopped"

		time.sleep(0.3)
		query = ('UPDATE status SET `dead` = %s WHERE id = %s')
		data = (False, 0)
		cursor.execute(query, data)
		cnx.commit()
	else:
		print "No Match Found"

	cursor.close()
	cnx.close()
