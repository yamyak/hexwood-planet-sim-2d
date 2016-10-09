from Satellite import Satellite

if __name__ == '__main__':

	mercury = Satellite(1, "Mercury", 3.05076571932, 5.790905e10, 0.20563, 1.98855e30, 6.4185e23)
	venus = Satellite(2, "Venus", 0.87467175463, 1.08208e11, 0.0067, 1.98855e30, 4.8676e24)
	earth = Satellite(3, "Earth", 6.25904740362, 1.49598e11, 0.016711230, 1.98855e30, 5.97219e24)
	mars = Satellite(4, "Mars", 0.33812263598, 2.27939e11, 0.0934, 1.98855e30, 3.3022e23)
	jupiter = Satellite(5, "Jupiter", 0.34941491624, 7.78547e11, 0.048775, 1.98855e30, 1.8986e27)
	saturn = Satellite(6, "Saturn", 5.53304279467, 1.43345e12, 0.055723219, 1.98855e30, 5.6846e26)
	uranus = Satellite(7, "Uranus", 2.48252142145, 2.87067e12, 0.047220087, 1.98855e30, 8.681e25)
	neptune = Satellite(8, "Neptune", 4.4720222358, 4.49854e12, 0.00867797, 1.98855e30, 1.0243e26)
	pluto = Satellite(9, "Pluto", 0.25359634031, 5.874e12, 0.244671664, 1.98855e30, 1.305e22)
	
	mercury.Start()
	venus.Start()
	earth.Start()
	mars.Start()
	jupiter.Start()
	saturn.Start()
	uranus.Start()
	neptune.Start()
	pluto.Start()
