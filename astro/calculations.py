import swisseph as swe
import pandas as pd
from . import utils as utl
import numpy as np
from . import constants as ct

ORBS = {
    'Conjuncion': 10,
    'Oposicion': 8,
    'Trigono': 8,
    'Cuadratura': 8,
    'Sextil': 6,
#    'Quincuncio': 6
}

# Aspectos por ángulo
ASPECTS_ANGLES = {
    'Conjuncion': 0,
    'Oposicion': 180,
    'Trigono': 120,
    'Cuadratura': 90,
    'Sextil': 60,
 #   'Quincuncio': 150
}

def get_planets_pos(input_date, longitude, latitude):
    # Set the geoposition for topocentric calculations
    swe.set_topo(lon=longitude, lat=latitude)

    # get positions
    planet_positions = []
    for planet, id in zip(ct.get_PlanetNameStandard(), ct.get_PlanetIDStandard()):
        pos, ret  = swe.calc_ut(input_date, id)
        sign, degrees = utl.zodiac_position(pos[0])
        retrograde = 'Retrograde' if (pos[3] < 0 ) else 'Direct'
        planet_positions.append([planet, sign, degrees, retrograde, pos[0]])

    # Create DataFrame
    planets_df = pd.DataFrame(planet_positions, columns=['Planeta', 'Signo', 'Grados_Signo', 'Retrogrado','Posicion'])
    return planets_df

def get_house_cusps(input_date, longitude, latitude):
    # Set the geoposition for topocentric calculations
    swe.set_topo(lon=longitude, lat=latitude)
    # Get the cusps and ascendant/MC
    cusps, ascmc = swe.houses(input_date, latitude, longitude, b'P')  # 'P' for Placidus
    # List of house cusps
    cusp_positions = []
    for i, cusp_degree in enumerate(cusps, start=1):
        sign, degrees = utl.zodiac_position(cusp_degree)
        cusp_positions.append([f"House {i}", sign, degrees, cusp_degree])

    cusps_df = pd.DataFrame(cusp_positions, columns=['Casa', 'Signo', 'Grados','Posicion'])
    return cusps_df
   
def calculate_aspects(planet_positions_df):
    aspects_list = []
    
    # Iterar sobre los planetas para calcular los aspectos entre ellos
    for i in range(len(planet_positions_df)):
        for j in range(i + 1, len(planet_positions_df)):
            planet1 = planet_positions_df.iloc[i]
            planet2 = planet_positions_df.iloc[j]
            
            # Calcular la diferencia circular mínima
            diff = abs(planet1['Posicion'] - planet2['Posicion'])
            if diff > 180:
                diff = 360 - diff
            
            # Buscar si el ángulo está cerca de algún aspecto conocido
            for aspect_name, aspect_angle in ASPECTS_ANGLES.items():
                if abs(diff - aspect_angle) <= ORBS[aspect_name]:
                    aspects_list.append({
                        'Planeta 1': planet1['Planeta'],
                        'Planeta 2': planet2['Planeta'],
                        'Aspecto': aspect_name,
                        'Angulo': diff
                    })

    # Convertir a DataFrame para mejor visualización
    
    aspects_df = pd.DataFrame(aspects_list)
    print(aspects_df)
    return aspects_df
    

