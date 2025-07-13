import streamlit as st
import plotly.graph_objects as go
from core.data_fetcher import MarketDataFetcher


def launch_trading_dashboard():
    """Запуск интерактивной торговой панели"""
    st.set_page_config(page_title="NeuroCrypto Nexus V.2", layout="wide")

    st.title("NeuroCrypto Nexus V.2 - Торговая Панель")
    st.markdown("### Режим реального времени с нейроморфными вычислениями")

    # Выбор актива
    asset = st.selectbox("Выберите актив:", ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD"])

    # Получение данных
    data = MarketDataFetcher.fetch_realtime_data(asset)

    # Визуализация
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close']
    )])

    fig.update_layout(
        title=f"{asset} Ценовое движение",
        xaxis_title="Время",
        yaxis_title="Цена",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Отображение прогнозов
    st.subheader("Нейросетевые прогнозы")
    prediction = NeuralEngine().predict(data)
    st.metric("Следующий 15-минутный прогноз", f"{prediction:.2f}%")

    # Кнопки управления
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Активировать торговую стратегию", type="primary"):
            NeuralEngine().activate_trading_strategy(asset)

    with col2:
        if st.button("Экстренная остановка", type="secondary"):
            NeuralEngine().emergency_stop()