from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from astro import models as mod
from waitress import serve
from openai import OpenAI
import os 

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
 
app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def serve_root():
    return render_template('server_page.html')

@app.route("/natal_chart", methods=['POST'])
def natal_chart_endpoint():
    data = request.get_json(cache=True)
    print(f"Datos recibidos: {data}")  # Agrega un print para ver los datos en el servidor
    chart = mod.NatalChart(data['name'], data['date'], data['time'], data['location'])
    chart.calculate_all()
    planets = chart.get_planet_positions().to_dict(orient='records')
    houses = chart.get_house_positions().to_dict(orient='records'),
    aspects = chart.get_aspect_matrix().to_dict(orient='records'),
    response = jsonify({
        'nombre': data['name'],
        'date': data['date'], 
        'time': data['time'], 
        'location': data['location'],
        'planets': planets,
        'houses': houses
    })
    print(response)
    return response
    

@app.route("/ia/planeta-signo-casa", methods=['POST'])
def generate_openai_response():
    data = request.get_json(cache=True)
    print(f"Datos recibidos: {data}")
    user_message = data['userInput'] #"Mercurio-Acuario-III"
    system_message = """
        Eres un maestro astrólogo y necesito que me ayudes a escribir unos textos para enseñar los conceptos astrológicos de tal manera que se entienda a la perfección lo que simboliza dicho arquetipo. 
    La estructura es la siguiente:
    1. Planeta
    2. Planeta en Signo
    3. Planeta en Signo en Casa

    En el primer punto, explicar lo que simboliza el arquetipo del planeta en astrología con todos sus matices y variantes, de una manera que se note que es de un profesor que ha estudiado y no de revista del corazón, pero que a la vez que expresa todo lo posible la totalidad del arquetipo, también sea claro y conciso. En el segundo punto, explicar cómo se interpreta o cómo se manifiesta el planeta en el signo proporcionado. Finalmente, lo mismo para la situación concreta que caiga en una casa determinada. Quiero que te centres unicamente en generar el punto 3. A continuacion te presento como seria una respuesta para todos los puntos:
    ### 1. Mercurio
    Mercurio es el planeta de la comunicación, el pensamiento y el intelecto. Representa la forma en que procesamos la información, nos comunicamos y tomamos decisiones. Este arquetipo es dual, abarcando tanto la lógica y el análisis (Mercurio en su aspecto racional), como la curiosidad y la adaptabilidad (Mercurio en su faceta más inquieta). Mercurio es también el mensajero de los dioses en la mitología, lo que simboliza su conexión con el intercambio de ideas, el aprendizaje y la movilidad. A nivel personal, Mercurio nos muestra cómo interactuamos con nuestro entorno, cómo aprendemos y cómo compartimos nuestros pensamientos y emociones. Es un planeta que nos invita a explorar la variedad de perspectivas y a cuestionar las normas establecidas.
    ### 2. Mercurio en Acuario
    Cuando Mercurio se encuentra en Acuario, el enfoque de la comunicación y el pensamiento se vuelve innovador, original y a menudo poco convencional. Acuario es un signo de aire asociado con la libertad, la creatividad y el humanitarismo. Las personas con este posicionamiento tienden a pensar de manera independiente, a desafiar las normas y a buscar nuevas formas de entender el mundo. Su forma de comunicarse puede ser bastante progresista, a menudo utilizando un lenguaje que refleja ideas futuristas y vanguardistas. La curiosidad intelectual es una característica clave, así como un deseo de conectar con los demás en un nivel más amplio y abstracto. Sin embargo, esta energía puede llevar a una falta de atención a los detalles, ya que el enfoque a menudo se dirige hacia el panorama general y las posibilidades. 
    ### 3. Mercurio en Acuario en Casa III
    La Casa III es la esfera de la comunicación, los pensamientos cotidianos, el aprendizaje y las interacciones con el entorno cercano, incluyendo hermanos y vecinos. Cuando Mercurio en Acuario se sitúa en esta casa, la persona puede experimentar un enfoque único y revolucionario en su manera de comunicarse. Su estilo de aprendizaje es independiente y puede verse impulsado por un deseo de compartir ideas progresistas o innovadoras con su entorno. La persona puede ser vista como un pensador original entre sus pares, a menudo introduciendo conceptos nuevos en conversaciones cotidianas o en el ámbito educativo. Además, este posicionamiento puede fomentar un interés en la tecnología y las nuevas formas de comunicación, como las redes sociales o la mensajería instantánea, reflejando un deseo de conectar con una comunidad más amplia y diversa. Sin embargo, es importante que no se pierda en la abstracción y que también se mantenga en contacto con las realidades cotidianas y los detalles prácticos de la comunicación.     
    
    Ya tengo generados todos los textos para los primeros dos puntos de todas las combinaciones, necesito que me ayudes con el punto 3 que las combinaciones posibles son muchisimas, por eso para la configuracion que te de como input: Planeta-Signo-Casa, redacta unicamente el punto 3. Es decir para el input: Mercurio-Acuario-III, tu respuesta deberia ser algo tipo: 
    
    ### 3. Mercurio en Acuario en Casa III
    La Casa III es la esfera de la comunicación, los pensamientos cotidianos, el aprendizaje y las interacciones con el
    entorno cercano, incluyendo hermanos y vecinos. Cuando Mercurio en Acuario se sitúa en esta casa, la persona puede
    experimentar un enfoque único y revolucionario en su manera de comunicarse. Su estilo de aprendizaje es independiente y
    puede verse impulsado por un deseo de compartir ideas progresistas o innovadoras con su entorno. La persona puede ser
    vista como un pensador original entre sus pares, a menudo introduciendo conceptos nuevos en conversaciones cotidianas o
    en el ámbito educativo. Además, este posicionamiento puede fomentar un interés en la tecnología y las nuevas formas de
    comunicación, como las redes sociales o la mensajería instantánea, reflejando un deseo de conectar con una comunidad más
    amplia y diversa. Sin embargo, es importante que no se pierda en la abstracción y que también se mantenga en contacto
    con las realidades cotidianas y los detalles prácticos de la comunicación.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # El modelo que deseas usar, puede ser ajustado
            messages=[
                {"role": "system", "content": system_message},  # Mensaje del sistema
                {"role": "user", "content": user_message}       # Comando del usuario
            ],
            max_tokens=2000,  # Puedes ajustar este valor
            temperature=0.7    # Controla la creatividad de las respuestas
        )

        text = response.choices[0].message.content
        lines = text.splitlines()
        print(f"Respuesta Servidor: {text}")
        result = jsonify({
            'texto': "\n".join(lines[1:])
        })
        return result
    except Exception as e:
        print(f"Error al generar respuesta de OpenAI: {str(e)})
        return f"Error al generar respuesta de OpenAI: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
    #serve(app, host='0.0.0.0', port=8080)