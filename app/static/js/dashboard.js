const visualizeBtn = document.getElementById('loadDashboard');
const statusMessage = document.getElementById('status-message');
const loading = document.getElementById('loading');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const dateInfo = document.querySelector('.date-info');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Fetch date range when page loads
fetchDateRange();

async function fetchDateRange() {
    try {
        const response = await fetch('/account/visualise/date-range');
        if (!response.ok) {
            throw new Error('Failed to fetch date range');
        }

        const data = await response.json();

        // Set min and max dates for inputs
        startDateInput.min = data.min_date;
        startDateInput.max = data.max_date;
        endDateInput.min = data.min_date;
        endDateInput.max = data.max_date;

        // Set default values
        startDateInput.value = data.min_date;
        endDateInput.value = data.max_date;

        // Enable inputs
        startDateInput.disabled = false;
        endDateInput.disabled = false;
        visualizeBtn.disabled = false;

        // Update info text
        dateInfo.textContent = `Data available from ${formatDate(data.min_date)} to ${formatDate(data.max_date)}`;

    } catch (error) {
        dateInfo.textContent = 'Error loading date range';
        console.error('Error:', error);
    }
}

// Add date validation
startDateInput.addEventListener('change', validateDates);
endDateInput.addEventListener('change', validateDates);

function validateDates() {
    const startDate = new Date(startDateInput.value);
    const endDate = new Date(endDateInput.value);
    
    if (startDate > endDate) {
        statusMessage.textContent = "Start date cannot be after end date";
        visualizeBtn.disabled = true;
        return false;
    }

    // Check if dates are within min and max range
    if (startDate < new Date(startDateInput.min) || 
        startDate > new Date(startDateInput.max) ||
        endDate < new Date(endDateInput.min) || 
        endDate > new Date(endDateInput.max)) {
        statusMessage.textContent = "Selected dates must be within available data range";
        visualizeBtn.disabled = true;
        return false;
    }
    
    visualizeBtn.disabled = false;
    statusMessage.textContent = "";
    return true;
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString();
}

visualizeBtn.addEventListener('click', async function() {
    if (!validateDates()) return;
    
    statusMessage.textContent = "Fetching data...";
    visualizeBtn.disabled = true;
    loading.style.display = 'block';

    try {
        const response = await fetch("/account/visualise/dashboard", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                startDate: startDateInput.value,
                endDate: endDateInput.value
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error: ${errorText}`);
        }

        const imageBlob = await response.blob();
        const imageUrl = URL.createObjectURL(imageBlob);
        const img = document.createElement('img');
        img.src = imageUrl;
        img.style.maxWidth = '100%';
        
        const container = document.getElementById('dashboardContainer');
        container.innerHTML = '';
        container.appendChild(img);
        
        statusMessage.textContent = "Visualization complete!";

    } catch (error) {
        handleError("Error generating visualization: " + error.message);
    } finally {
        visualizeBtn.disabled = false;
        loading.style.display = 'none';
    }
});

function handleError(message) {
    console.error(message);
    statusMessage.textContent = message;
    loading.style.display = 'none';
    visualizeBtn.disabled = false;
}
