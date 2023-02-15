function createTableRow(data) {
    const tr = document.createElement('tr');
  
    const originalUrlTd = document.createElement('td');
    originalUrlTd.textContent = data.original_url;
  
    const shortenUrlTd = document.createElement('td');
    const a = document.createElement('a');
    a.setAttribute('href', data.shorten_url);
    a.setAttribute('target', '_blank');
    a.textContent = data.shorten_url;
    shortenUrlTd.appendChild(a);
  
    const timeTd = document.createElement('td');
    timeTd.textContent = data.time;
  
    tr.appendChild(originalUrlTd);
    tr.appendChild(shortenUrlTd);
    tr.appendChild(timeTd);
  
    return tr;
  }
  
  const searchForm = document.getElementById('search-form');
  const resultTable = document.getElementById('result-table');
  
  searchForm.addEventListener('submit', async (event) => {
    event.preventDefault();
  
    // Get form input values
    const searchInput = document.getElementById('search-input').value;
    const dateInput = document.getElementById('date-input').value;
    const pageInput = document.getElementById('page-input').value;
    const itemsPerPageInput = document.getElementById('items-per-page-input').value;
  
    // Build query string from form data
    const queryString = `search=${searchInput}&date=${dateInput}&page=${pageInput}&per_page=${itemsPerPageInput}`;
  
    // Fetch data from API using query string
    const response = await fetch(`http://127.0.0.1:5000/urls?${queryString}`);
    const data = await response.json();
  
    // Extract data from 'urls' array
    const dataArray = data.urls;
  
    // Clear existing table rows
    resultTable.querySelectorAll('tr').forEach(tr => {
      if (tr.parentNode !== resultTable.querySelector('thead')) {
        tr.remove();
      }
    });
  
    // Create new table rows from API data
    dataArray.forEach(dataObject => {
      const tr = createTableRow(dataObject);
      resultTable.appendChild(tr);
    });
  });
  