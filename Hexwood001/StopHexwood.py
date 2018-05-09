import mysql.connector
import sys
import time

# open connection with the database
def openDB():

	cnx = mysql.connector.connect(user='hex', password='hex0nmysQl', host='localhost')
	cursor = cnx.cursor()
	cnx.database = 'hexwood001'
	
	return cnx, cursor

if __name__ == '__main__':

	cnx, cursor = openDB()
	
	planets = [ "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto" ]
	planetName = str(sys.argv[1])
	
  # if command line argument is one of planet names, set kill flag for that planet to true and update database
	if planetName in planets:
		query = ('UPDATE status SET `dead` = %s WHERE name = %s')
		data  = (True, planetName)
		cursor.execute(query, data)
		cnx.commit()
		output = planetName + " Stopped"
		print output

    # reset the kill flag to true to prepare for the next time the script is run
		time.sleep(0.3)
		query = ('UPDATE status SET `dead` = %s WHERE name = %s')
		data = (False, planetName)
		cursor.execute(query, data)
		cnx.commit()
    
  # if command line argument is "All", set kill flag for all planets to true and update database
	elif planetName == "All":
		query = ('UPDATE status SET `dead` = %s WHERE id = %s')
		data  = (True, 0)
		cursor.execute(query, data)
		cnx.commit()
		print "All Planets Stopped"

    # reset the kill flag to true to prepare for the next time the script is run
		time.sleep(0.3)
		query = ('UPDATE status SET `dead` = %s WHERE id = %s')
		data = (False, 0)
		cursor.execute(query, data)
		cnx.commit()
	else:
		print "No Match Found"

	cursor.close()
	cnx.close()
