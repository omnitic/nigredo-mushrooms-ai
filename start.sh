#!/bin/bash

echo "🍄 Iniciando el cerebro (FastAPI)..."
# Arranca FastAPI en segundo plano (&) y lo expone al exterior (0.0.0.0)
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "📱 Iniciando el puente móvil (Telegram)..."
# Arranca el bot de Telegram en segundo plano (&)
python app/telegram_bot.py &

echo "🖥️ Iniciando la interfaz visual (Streamlit)..."
# Arranca Streamlit en primer plano para mantener el contenedor vivo
streamlit run app/ui.py --server.port 8501 --server.address 0.0.0.0
