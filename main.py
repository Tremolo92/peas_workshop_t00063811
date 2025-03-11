import pandas as pd
import requests
import numpy as np

# Configuración de la API (ejemplo con Alpha Vantage)
API_KEY = '0ISARYWKONXJ3BTN'
SYMBOL = 'EURUSD'  # Par de divisas EUR/USD
FUNCTION = 'FX_DAILY'  # Función para obtener datos diarios de FOREX

# Obtener datos históricos del mercado FOREX
url = f'https://www.alphavantage.co/query?function={FUNCTION}&from_symbol=EUR&to_symbol=USD&apikey={API_KEY}&datatype=csv'
response = requests.get(url)
data = pd.read_csv(url)

# Procesar los datos
data['Date'] = pd.to_datetime(data['timestamp'])
data.set_index('Date', inplace=True)
data.sort_index(inplace=True)

# Calcular indicadores técnicos
data['MA_50'] = data['close'].rolling(window=50).mean()
data['MA_200'] = data['close'].rolling(window=200).mean()
data['RSI'] = 100 - (100 / (1 + (data['close'].diff(1).clip(lower=0).rolling(window=14).mean() / 
                     -data['close'].diff(1).clip(upper=0).rolling(window=14).mean())))

# Función de toma de decisiones basada en FOL
def tomar_decision(data):
    rsi = data['RSI'].iloc[-1]
    macd_tendencia = "Alcista" if data['MA_50'].iloc[-1] > data['MA_200'].iloc[-1] else "Bajista"

    if rsi < 30 and macd_tendencia == "Alcista":
        return "Comprar EUR/USD"
    elif rsi > 70 and macd_tendencia == "Bajista":
        return "Vender EUR/USD"
    else:
        return "Mantener posición (Hold)"

# Generar y mostrar la decisión
decision = tomar_decision(data)
print("Decisión del agente basada en Lógica de Primer Orden (FOL):")
print(decision)