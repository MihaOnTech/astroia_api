import swisseph as swe

def get_AspectosOrbesStandard(): 
    return  {
        'Conjuncion': (0, 8),
        'Oposicion': (180, 8),
        'Trigono': (120, 8),
        'Cuadratura': (90, 8),
        'Sextil': (60, 6)
    }

def get_SignosArrayNombre():
    return ["Aries", "Tauro", "Geminis", "Cancer", "Leo", "Virgo",
            "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"]
    
def get_PlanetNameStandard():
    return ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto','Node']
    
    
def get_PlanetIDStandard():
    return [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
                  swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO, swe.MEAN_NODE]