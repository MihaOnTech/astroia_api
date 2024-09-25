import swisseph as swe
import pandas as pd
from . import utils as utl
import numpy as np
from . import constants as ct

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
    print(cusps_df)
    return cusps_df
   
def aspects_calc(planet_positions_df, house_positions_df):
    # Crear un DataFrame para guardar las diferencias
    aspect_matrix = pd.DataFrame("", index=planet_positions_df['Planeta'], columns=planet_positions_df['Planeta'])

    # Calcular las diferencias de posición
    for i in range(len(planet_positions_df)):
        aspect_matrix.loc[planet_positions_df['Planeta'][i], planet_positions_df['Planeta'][i]] = 'X'
        for j in range(i+1, len(planet_positions_df)):
            # Calcular la diferencia circular mínima
            diff = abs(planet_positions_df['Posicion'][i] - planet_positions_df['Posicion'][j])
            if diff > 180:
                diff = 360 - diff
            # Asignar la diferencia al DataFrame en ambas direcciones
            aspect_matrix.loc[planet_positions_df['Planeta'][i], planet_positions_df['Planeta'][j]] = 'X'
            aspect_matrix.loc[planet_positions_df['Planeta'][j], planet_positions_df['Planeta'][i]] = diff
    
    aspect_matrix.iloc[0:, 0:] = aspect_matrix.iloc[0:, 0:].map(lambda x: utl.encontrar_aspecto(x) if isinstance(x, (int, float)) else x)
    aspect_matrix = aspect_matrix.fillna('-')
    #print(aspect_matrix)
    return aspect_matrix
    

