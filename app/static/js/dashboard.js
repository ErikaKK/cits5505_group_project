const visualiseBtn = document.getElementById('loadDashboard');
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
            if(response.status === 404){
                throw new Error('No data found.');
            }
            throw new Error('Failed to fetch date range.');
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
        visualiseBtn.disabled = false;

        // Update info text
        dateInfo.textContent = `Data available from ${formatDate(data.min_date)} to ${formatDate(data.max_date)}`;

    } catch (error) {
        dateInfo.textContent = 'Error loading date range. '+error;
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
        visualiseBtn.disabled = true;
        return false;
    }

    // Check if dates are within min and max range
    if (startDate < new Date(startDateInput.min) || 
        startDate > new Date(startDateInput.max) ||
        endDate < new Date(endDateInput.min) || 
        endDate > new Date(endDateInput.max)) {
        statusMessage.textContent = "Selected dates must be within available data range";
        visualiseBtn.disabled = true;
        return false;
    }
    
    visualiseBtn.disabled = false;
    statusMessage.textContent = "";
    return true;
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString();
}

visualiseBtn.addEventListener('click', async function() {
    if (!validateDates()) return;
    
    statusMessage.textContent = "Fetching data...";
    visualiseBtn.disabled = true;
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
        
        statusMessage.textContent = "Visualisation complete!";

    } catch (error) {
        handleError("Error generating Visualisation: " + error.message);
    } finally {
        visualiseBtn.disabled = false;
        loading.style.display = 'none';
    }
});

function handleError(message) {
    console.error(message);
    statusMessage.textContent = message;
    loading.style.display = 'none';
    visualiseBtn.disabled = false;
}

const shareButton = document.getElementById('shareData');
    const sharePopover = document.getElementById('sharePopover');
    const shareForm = document.getElementById('shareForm');
    const cancelButton = document.getElementById('cancelShare');


    // Show popover when share button is clicked
    shareButton.addEventListener('click', () => {
        if (!startDateInput.value || !endDateInput.value) {
            alert('Please select a date range first');
            return;
        }
        sharePopover.classList.remove('hidden');
    });

    // Hide popover when cancel is clicked
    cancelButton.addEventListener('click', () => {
        sharePopover.classList.add('hidden');
        shareForm.reset();
    });

    // Hide popover when clicking outside
    sharePopover.addEventListener('click', (e) => {
        if (e.target === sharePopover) {
            sharePopover.classList.add('hidden');
            shareForm.reset();
        }
    });

    // Handle form submission
    shareForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const receiverEmail = document.getElementById('receiverEmail').value;
        const message = document.getElementById('message').value;
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        try {
            const response = await fetch('/account/share-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                },
                body: JSON.stringify({
                    receiverEmail,
                    message,
                    startDate,
                    endDate
                })
            });

            const result = await response.json();

            if (response.ok) {
                alert('Data shared successfully!');
                sharePopover.classList.add('hidden');
                shareForm.reset();
            } else {
                throw new Error(result.error || 'Failed to share data');
            }
        } catch (error) {
            alert('Error sharing data: ' + error.message);
        }
    });