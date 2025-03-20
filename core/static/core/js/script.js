document.addEventListener("DOMContentLoaded", function () {
        // Получаем элементы
        const hoursElement = document.getElementById('hours');
        const hiddenHoursInput = document.getElementById('hidden-hours'); // Скрытое поле для передачи в форму
        const displayHoursElement = document.getElementById('display-hours');
        const totalCostElement = document.getElementById('total-cost');
        const decreaseButton = document.getElementById('decrease-hours');
        const increaseButton = document.getElementById('increase-hours');

        // Получаем цену оборудования
        const equipmentPricePerHour = parseInt(document.getElementById('equipment-price').textContent);

        // Функция для обновления стоимости
        function updateCost() {
            let hours = parseInt(hoursElement.textContent);
            hiddenHoursInput.value = hours; // Обновляем скрытое поле
            const totalCost = hours * equipmentPricePerHour;
            displayHoursElement.textContent = `${hours}ч`;
            totalCostElement.textContent = `${totalCost.toLocaleString()} р`;
            console.log("Обновлено: hours =", hours);
        }

        // Уменьшение срока аренды
        decreaseButton.addEventListener('click', () => {
            let hours = parseInt(hoursElement.textContent);
            if (hours > 1) {
                hours--;
                hoursElement.textContent = hours;
                updateCost();
            }
        });

        // Увеличение срока аренды
        increaseButton.addEventListener('click', () => {
            let hours = parseInt(hoursElement.textContent);
            hours++;
            hoursElement.textContent = hours;
            updateCost();
        });

        // Обновляем скрытое поле перед отправкой формы
        document.querySelector('form').addEventListener('submit', function () {
            hiddenHoursInput.value = parseInt(hoursElement.textContent);
            console.log("Форма отправлена с hours =", hiddenHoursInput.value);
        });

        // Инициализация стоимости при загрузке страницы
        updateCost();
    });