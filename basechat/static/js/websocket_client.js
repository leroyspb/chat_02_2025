document.addEventListener("DOMContentLoaded", function () {
    const messagesContainer = document.querySelector("#messages_container");
    const messageInput = document.querySelector('[name=message_input]');
    const sendMessageButton = document.querySelector('[name=send_message_button]');

    const username = "User" + Math.floor(Math.random() * 1000); // Генерируем временное имя пользователя
    const chat_id = "123"; // Название комнаты, можно менять динамически

    let socket = new WebSocket(`ws://localhost:8000/ws/chat/${chat_id}/`);

    // Соединение установлено
    socket.onopen = function () {
        console.log("WebSocket соединение установлено!");
    };

    // Получение сообщений от сервера
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        displayMessage(`${data.username}: ${data.message}`, 'received');
    };

    // Ошибка WebSocket
    socket.onerror = function (error) {
        console.error("Ошибка WebSocket:", error);
    };

    // Соединение закрыто
    socket.onclose = function () {
        console.log("WebSocket соединение закрыто");
    };

    // socket.onclose = (event) => {
    //     console.log('WebSocket соединение закрыто. Код:', event.code, 'Причина:', event.reason);
    // };

    // Кнопка отправки сообщения
    sendMessageButton.onclick = function () {
        if (socket.readyState === WebSocket.OPEN) {
            const message = messageInput.value.trim();
            if (message) {
                socket.send(JSON.stringify({
                    message: message,
                    username: username
                }));
                displayMessage(`Вы: ${message}`, 'sent');
                messageInput.value = '';
            }
        } else {
            console.log("WebSocket не подключен!");
        }
    };

    // Функция отображения сообщений
    function displayMessage(message, type) {
        const messageElement = document.createElement("div");
        messageElement.classList.add(type);
        messageElement.textContent = message;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});
