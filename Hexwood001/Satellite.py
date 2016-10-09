import mysql.connector
import math
import time
import threading

class Satellite:
	G = 6.673848e-11
	timeStep = 1000000

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
		
	def OpenDB(self):
	
		cnx = mysql.connector.connect(user='hex', password='hex0nmysQl', host='localhost')
		cursor = cnx.cursor()
		cnx.database = 'hexwood001'

		return cnx, cursor
		
	def CloseDB(self, cnx, cursor):
	
		cursor.close()
		cnx.close()
		
	def GetStatus(self, cnx, cursor):
	
		query = ('SELECT `dead` FROM status WHERE id = %s')
		data = (self.__id,);
		cursor.execute(query, data)
		for dead in cursor:
			killMe = dead[0]
			
		query = ('SELECT `dead` FROM status WHERE id = %s')
		data = (0,);
		cursor.execute(query, data)
		for dead in cursor:
			killAll = dead[0]
		
		return killMe, killAll
		
	def SendData(self, cnx, cursor):
	
		query = ('UPDATE data SET `period_time` = %s, `mean_anomaly` = %s, `eccentric_anomaly` = %s, `radius` = %s, `angle` = %s, `x_location` = %s, `y_location` = %s WHERE id = %s')
		data = (self.__currentTime, self.__meanAnomaly, self.__eccentricAnomaly, self.__radius, self.__angleFinal, self.__xPosition, self.__yPosition, self.__id)
		cursor.execute(query, data)
		cnx.commit()
		
	def Calculate(self):
	
		self.__timeDifference = time.time() - self.__timeStart
	        self.__currentTime += self.timeStep * self.__timeDifference
	        if( self.__currentTime >= self.__orbitalPeriod ):
			self.__currentTime -= self.__orbitalPeriod
	        self.__meanAnomaly = self.__meanMotion * self.__currentTime
	        self.__timeStart = time.time()
	
		self.__eccentricAnomaly = self.__meanAnomaly + self.__eccentricity * math.sin(self.__meanAnomaly) * (1 + self.__eccentricity * math.cos(self.__meanAnomaly))
	        self.__radius = self.__semiMajorAxis * (1 - self.__eccentricity * math.cos(self.__eccentricAnomaly))
	        self.__angle = math.acos((math.cos(self.__eccentricAnomaly) - self.__eccentricity) / (1 - self.__eccentricity * math.cos(self.__eccentricAnomaly)))
	        if( self.__angle < self.__angleLast ):
			self.__angleFinal = -1 * self.__angle
	        if( self.__angle > self.__angleLast ):
			self.__angleFinal = self.__angle;
	        self.__angleLast = self.__angle
	        #print(self.__angleFinal)

	        self.__xPosition = self.__radius * math.cos(self.__angleFinal)
	        #print(self.__xPosition)
	        self.__yPosition = self.__radius * math.sin(self.__angleFinal)
	        #print(self.__yPosition)

	        time.sleep(0.1)
		
	def Revolve(self, cnx, cursor):
		
		self.Calculate()
		self.SendData(cnx, cursor)
		
	def Update(self, cnx, cursor):
	
		killMe, killAll = self.GetStatus(cnx, cursor)
	
		while((not killMe) and (not killAll)):
			self.Revolve(cnx, cursor)
			
			killMe, killAll = self.GetStatus(cnx, cursor)
			
		self.CloseDB(cnx, cursor)
		
	def Start(self):
	
		cnx, cursor = self.OpenDB()
		
		#self.__t = threading.Thread(target=Update)
		self.__t = threading.Thread(target=self.Update, args=(cnx, cursor))

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
		
		self.__t.start()
