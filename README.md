# astroPy-api-v2

## Description
`astroPy-api-v2` is a simple yet powerful project that leverages the Swiss Ephemeris package to compute essential astrological data necessary for creating an astral chart. This data includes positions of planets, zodiac signs, houses, and aspects between planets. The project is structured around a Flask API, which offers a single route where users can submit their birth data and receive back computed astrological results.

## Installation

To set up `astroPy-api-v2` locally, follow these steps:

### Clone the Repository
1. Ensure you have Git installed on your machine. If not, you can install it from [Git's official site](https://git-scm.com/).
2. Open your command line interface (CLI).
3. Clone the repository:
   ```
   git clone https://github.com/MihaOnTech/astroPy-api-v2.git
   ```
4. Navigate to the cloned directory:
   ```
   cd astroPy-api-v2
   ```

### Install Dependencies
1. Ensure you have Python and pip installed on your system.
2. Install the required packages from the `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the API:
1. Start the Flask server:
   ```
   python app.py
   ```
2. Execute the test script to call the service and save the result data in `output.json`:
   ```
   python test.py > output.json
   ```

## API Specifications

- **Endpoint**: `http://127.0.0.1:5000/natal_chart`
- **Method**: POST
- **Headers**:
  - `Content-Type`: `application/json`
  - `Custom-Header`: `value`  (Example of a custom header)
- **Input Data**:
  ```json
  {
    "date": "05/02/93",
    "time": "03:30",
    "location": "Barcelona, España"
  }
  ```
- **Responses**:
  - **Planets**:
    ```json
    [
        {
            "Grados_Signo": 16.304187295696693,
            "Planeta": "Sun",
            "Posicion": 316.3041872956967,
            "Retrogrado": "Direct",
            "Signo": "Acuario"
        },
        ...
    ]
    ```
  - **Houses**:
    ```json
    [
        {
            "Casa": "House 1",
            "Grados": 6.5794807007623035,
            "Posicion": 246.5794807007623,
            "Signo": "Sagitario"
        },
        ...
    ]
    ```
  - **Aspects**:
    ```json
    [
        {
            "Jupiter": "X",
            "Mars": "X",
            ...
        },
        ...
    ]
    ```

## Contributing

Contributions to `astroPy-api-v2` are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-sourced under the [MIT License](LICENSE).

## Contact

For more information or if you have any questions, feel free to reach out to me at [mihaontech@gmail.com](mailto:mihaontech@gmail.com).
