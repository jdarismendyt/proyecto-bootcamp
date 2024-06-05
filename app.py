import io
import os
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import psycopg2
import joblib

app = Flask(__name__)
CORS(app)

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="bootcamp",
    user="postgres",
    password="daniel2001",
    host="localhost",
    port="5432",
    client_encoding="UTF8"
)

# Cargar modelos
RN = joblib.load("mlp_model.joblib")
SVM = joblib.load("svm_model.joblib")
RL = joblib.load("rl_model.joblib")

@app.route('/predict', methods=['POST'])
def predict():
    # Recibir el archivo CSV y la técnica del frontend
    file = request.files['file']
    tecnica = request.form['tecnica']

    # Leer el archivo CSV
    df = pd.read_csv(file)
    df = df.drop(columns=['ADMITIDO'])

    # Seleccionar el modelo correspondiente
    if tecnica == 'Red Neuronal':
        modelo = RN
    elif tecnica == 'SVM':
        modelo = SVM
    elif tecnica == 'Regresión':
        modelo = RL
    else:
        return jsonify({'error': 'Técnica no válida'}), 400

    # Aplicar el modelo al DataFrame
    predictions = modelo.predict(df)

    # Agregar las predicciones al DataFrame
    df['predictions'] = predictions

    # Guardar el DataFrame modificado a un nuevo archivo CSV en memoria
    csv_output = io.StringIO()
    df.to_csv(csv_output, index=False)
    csv_output.seek(0)

    # Contar las predicciones
    prediction_counts = pd.Series(predictions).value_counts().to_dict()

    # Crear una fila con las columnas "tecnica", "bueno" y "malo"
    bueno = prediction_counts.get(1, 0)
    malo = prediction_counts.get(0, 0)

    # Guardar los datos en la base de datos
    cursor = conn.cursor()
    cursor.execute("INSERT INTO predicciones (tecnica, malo, bueno) VALUES (%s, %s, %s)", (tecnica, malo, bueno))
    conn.commit()
    cursor.close()

    # Devolver el archivo CSV original con las predicciones y el conteo en formato JSON
    return jsonify({'predictions_csv': csv_output.getvalue(), 'prediction_counts': prediction_counts}), 200

if __name__ == '__main__':
    app.run(debug=True)
