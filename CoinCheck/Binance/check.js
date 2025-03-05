// Подключаемся к WebSocket серверу
const socket = new WebSocket('ws://localhost:8000/ws/socket-server/'); // Замените на адрес вашего сервера, если нужно

// Событие при открытии соединения
socket.onopen = function() {
    console.log('Соединение установлено! 🎉');

    // Указываем валюту после подключения
    const tickerMessage = JSON.stringify({ ticker: 'BTC' }); // Например, вы хотите получить цену ETH
    socket.send(tickerMessage);
};

// Событие при получении сообщения
socket.onmessage = function(event) {
    const data = JSON.parse(event.data); // Парсим полученные данные
    console.log('Получено сообщение:', data.message); // Выводим сообщение в консоль
};

// Событие при закрытии соединения
socket.onclose = function(event) {
    console.log('Соединение закрыто!', event);
};

// Событие при ошибке
socket.onerror = function(error) {
    console.error('Ошибка WebSocket:', error);
};
