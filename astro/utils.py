from . import constants as ct

## Apartir de la distancia respecto al punto de Aries (degrees)
## Calcula la posicion en cuanto a signo zodiacal para planetas y cuspides
def zodiac_position(degrees):
    sign_index = int(degrees / 30)
    sign_names = ct.get_SignosArrayNombre()
    sign = sign_names[sign_index]
    sign_degrees = degrees % 30
    return (sign, sign_degrees)

def encontrar_aspecto(diferencia):
    for aspecto, (grado, orbe) in ct.get_AspectosOrbesStandard().items():
        if grado - orbe <= diferencia <= grado + orbe:
            return aspecto
    return 
