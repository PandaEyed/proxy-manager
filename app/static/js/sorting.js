let currentSortColumn = -1;
let currentSortDirection = 'asc';

function sortTable(columnIndex) {
    const table = document.getElementById("dashboardTable");
    const rows = Array.from(table.rows).slice(1); // Exclude header row
    const isSameColumn = currentSortColumn === columnIndex;

    // Determine sort direction
    currentSortDirection = isSameColumn && currentSortDirection === 'asc' ? 'desc' : 'asc';
    currentSortColumn = columnIndex;

    // Sort rows
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].innerText.trim();
        const bText = b.cells[columnIndex].innerText.trim();

        // Attempt to parse values as numbers
        const aValue = isNaN(parseFloat(aText)) ? aText : parseFloat(aText);
        const bValue = isNaN(parseFloat(bText)) ? bText : parseFloat(bText);

        // Compare numbers or strings
        if (typeof aValue === 'number' && typeof bValue === 'number') {
            return currentSortDirection === 'asc' ? aValue - bValue : bValue - aValue;
        } else if (typeof aValue === 'string' && typeof bValue === 'string') {
            return currentSortDirection === 'asc'
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        } else {
            return 0; // Default to equal if types don't match
        }
    });

    // Rebuild table
    const tbody = table.tBodies[0];
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));

    // Update sort icons
    updateSortIcons(columnIndex);
}

function updateSortIcons(columnIndex) {
    const headers = document.querySelectorAll("#dashboardTable thead th i");
    headers.forEach((icon, idx) => {
        icon.className = 'fas fa-sort'; // Reset all icons
        if (idx === columnIndex) {
            icon.className = currentSortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
        }
    });
}