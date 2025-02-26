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