import mysql.connector
import math
import time
import threading

class Satellite:
	G = 6.673848e-11
	timeStep = 1000000

  # initialize planet specific data
	def __init__(self, ids, name, meanAn, sMajAx, ecc, cenMass, m):

		self.__id = ids
		self.__name = name
    self.__meanAnomaly = meanAn
    self.__semiMajorAxis = sMajAx
    self.__eccentricity = ecc
    self.__centerMass = cenMass
    self.__mass = m
		self.__eccentricAnomaly = 0
		self.__meanMotion = 0
		self.__orbitalPeriod = 0
		self.__radius = 0
		self.__angle = 0
		self.__angleLast = 0
		self.__angleFinal = 0
		self.__xPosition = 0
		self.__yPosition = 0
		self.__currentTime = 0
		self.__timeStart = 0
		self.__timeDifference = 0
		self.__t = 0
		
  # open connection with the database
	def OpenDB(self):
	
		cnx = mysql.connector.connect(user='', password='', host='')
		cursor = cnx.cursor()
		cnx.database = ''

		return cnx, cursor
		
  # close connect with the database
	def CloseDB(self, cnx, cursor):
	
		cursor.close()
		cnx.close()
	
  # retrieve the thread kill flag from database
	def GetStatus(self, cnx, cursor):
	
    # retrieve this planet's specific thread kill flag 
		query = ('SELECT `dead` FROM status WHERE id = %s')
		data = (self.__id,);
		cursor.execute(query, data)
		for dead in cursor:
			killMe = dead[0]
			
    # retrieve the overall thread kill flag
		query = ('SELECT `dead` FROM status WHERE id = %s')
		data = (0,);
		cursor.execute(query, data)
		for dead in cursor:
			killAll = dead[0]
		
		return killMe, killAll
	
  # send update of planet data to the database
	def SendData(self, cnx, cursor):
	
		query = ('UPDATE data SET `period_time` = %s, `mean_anomaly` = %s, `eccentric_anomaly` = %s, `radius` = %s, `angle` = %s, `x_location` = %s, `y_location` = %s WHERE id = %s')
		data = (self.__currentTime, self.__meanAnomaly, self.__eccentricAnomaly, self.__radius, self.__angleFinal, self.__xPosition, self.__yPosition, self.__id)
		cursor.execute(query, data)
		cnx.commit()
	
  # calculate the latest set of planet data
	def Calculate(self):
	
    # calculate the time that's passed since last iteration
		self.__timeDifference = time.time() - self.__timeStart
    self.__currentTime += self.timeStep * self.__timeDifference
    
    # if orbital period time exceeded, reset time to 0
    if( self.__currentTime >= self.__orbitalPeriod ):
			self.__currentTime -= self.__orbitalPeriod
    
    # calculate current mean anomaly of planet 
    self.__meanAnomaly = self.__meanMotion * self.__currentTime
    
    self.__timeStart = time.time()
	
    # calculate current eccentric anomaly of planet
		self.__eccentricAnomaly = self.__meanAnomaly + self.__eccentricity * math.sin(self.__meanAnomaly) * (1 + self.__eccentricity * math.cos(self.__meanAnomaly))
    
    # calculate radius and angle of planet using Sun as the origin
    self.__radius = self.__semiMajorAxis * (1 - self.__eccentricity * math.cos(self.__eccentricAnomaly))
    self.__angle = math.acos((math.cos(self.__eccentricAnomaly) - self.__eccentricity) / (1 - self.__eccentricity * math.cos(self.__eccentricAnomaly)))
    
    # account for negative angles
    if( self.__angle < self.__angleLast ):
			self.__angleFinal = -1 * self.__angle
    if( self.__angle > self.__angleLast ):
			self.__angleFinal = self.__angle;
    self.__angleLast = self.__angle

    # calculate x and y position of planet using Sun as the origin
    self.__xPosition = self.__radius * math.cos(self.__angleFinal)
    self.__yPosition = self.__radius * math.sin(self.__angleFinal)

    time.sleep(0.1)
	
  # run through 1 time step and save data to database
	def Revolve(self, cnx, cursor):
		
		self.Calculate()
		self.SendData(cnx, cursor)
		
  # continue to iterate through planet revolution if kill flags not set
	def Update(self, cnx, cursor):
	
    # check if kill flags set
		killMe, killAll = self.GetStatus(cnx, cursor)
	
    # while kill flags not set in database, continue to revolve
		while((not killMe) and (not killAll)):
			self.Revolve(cnx, cursor)
      
			# check if kill flags set
			killMe, killAll = self.GetStatus(cnx, cursor)
		
		self.CloseDB(cnx, cursor)
		
  # start the planet thread
	def Start(self):
	
		cnx, cursor = self.OpenDB()
		
    # set up the planet thread
		self.__t = threading.Thread(target=self.Update, args=(cnx, cursor))

    # initialize the mean motion, orbital period, and current orbital period location
    self.__meanMotion = math.sqrt((self.G * (self.__centerMass + self.__mass))/pow(self.__semiMajorAxis, 3))
    self.__orbitalPeriod = 2 * math.pi * (1 / self.__meanMotion)
    self.__currentTime = self.__meanAnomaly / self.__meanMotion
    self.__timeStart = time.time()

    self.__eccentricAnomaly = self.__meanAnomaly + self.__eccentricity * math.sin(self.__meanAnomaly) * (1 + self.__eccentricity * math.cos(self.__meanAnomaly))
    self.__radius = self.__semiMajorAxis * (1 - self.__eccentricity * math.cos(self.__eccentricAnomaly))
    self.__angleLast = math.acos((math.cos(self.__eccentricAnomaly) - self.__eccentricity) / (1 - self.__eccentricity * math.cos(self.__eccentricAnomaly)))

    time.sleep(0.1)

    self.Calculate()
		self.SendData(cnx, cursor)
		
    # start the thread
		self.__t.start()
