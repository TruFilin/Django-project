function sortTable(tableId, column) {
    const table = document.getElementById(tableId);
    const rows = Array.from(table.rows).slice(1); // Исключаем заголовок
    const isNumeric = !isNaN(rows[0].cells[column].innerText);

    let sortedRows = rows.sort((a, b) => {
        const aValue = a.cells[column].innerText.trim();
        const bValue = b.cells[column].innerText.trim();

        if (isNumeric) {
            return parseFloat(aValue) - parseFloat(bValue);
        } else {
            return aValue.localeCompare(bValue, 'ru');
        }
    });

    // Переключение порядка сортировки
    if (table.getAttribute('data-sort-column') === column.toString()) {
        sortedRows.reverse();
    }

    table.setAttribute('data-sort-column', column);

    // Очистка tbody и добавление отсортированных строк
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}
function filterTable(tableId, column) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const filterValue = event.target.value.toLowerCase(); // Получаем значение из input
    const rows = table.getElementsByTagName('tr'); // Все строки таблицы

    for (let i = 1; i < rows.length; i++) { // Пропускаем первую строку (заголовки)
        const cell = rows[i].getElementsByTagName('td')[column]; // Ячейка в указанном столбце
        if (cell) {
            const cellText = cell.textContent || cell.innerText; // Текст ячейки
            if (cellText.toLowerCase().includes(filterValue)) {
                rows[i].style.display = ''; // Показываем строку
            } else {
                rows[i].style.display = 'none'; // Скрываем строку
            }
        }
    }
}
document.addEventListener('DOMContentLoaded', function () {
  console.log('Скрипт загружен');

  // Проверяем, были ли найдены данные о погрузчике
  const forkliftDataFound = document.getElementById('forklift-data-found');
  if (forkliftDataFound && forkliftDataFound.dataset.found === 'true') {
    showButton('show-forklift-info'); // Показываем кнопку "Общая информация"
  }

  // Функция для показа кнопки
  function showButton(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
      button.style.display = 'block';
    }
  }

  // Обработчики для кнопок
const showToInfoButton = document.getElementById('show-to-info');
if (showToInfoButton) {
    console.log('Кнопка ТО найдена'); // Проверяем, что кнопка найдена
    showToInfoButton.addEventListener('click', function () {
        console.log('Кнопка ТО нажата'); // Лог, когда кнопка нажата
        toggleBlockVisibility('to-info-block');
    });
} else {
    console.log('Кнопка ТО не найдена'); // Лог, если кнопка не найдена
}

  const showComplaintInfoButton = document.getElementById('show-complaint-info');
  if (showComplaintInfoButton) {
    showComplaintInfoButton.addEventListener('click', function () {
      toggleBlockVisibility('complaint-info-block');
    });
  }

  const showForkliftInfoButton = document.getElementById('show-forklift-info');
  if (showForkliftInfoButton) {
    showForkliftInfoButton.addEventListener('click', function () {
      toggleBlockVisibility('forklift-info-block');
    });
  }

  // Функция для переключения видимости блока
  function toggleBlockVisibility(blockId) {
    const block = document.getElementById(blockId);
    if (block) {
      block.style.display = block.style.display === 'none' || block.style.display === '' ? 'block' : 'none';
    } else {
      console.error(`Блок с ID "${blockId}" не найден.`);
    }
  }
});