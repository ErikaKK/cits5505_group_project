const requiredFields = [
    "ts",
    "ms_played",
    "master_metadata_track_name",
    "master_metadata_album_artist_name",
];
const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
const statusMessage = document.getElementById("status-message");

const visualizeBtn = document.getElementById("loadDashboard");
visualizeBtn.addEventListener("click", sendDataToFlask);

async function sendDataToFlask() {
    statusMessage.textContent = "Opening database...";
    visualizeBtn.disabled = true;

    try {
        const request = indexedDB.open("MyDatabase", 2);
        
        request.onerror = function(event) {
            handleError("Failed to open database: " + event.target.errorCode);
        };

        request.onsuccess = async function(event) {
            const db = event.target.result;
            statusMessage.textContent = "Database opened, retrieving data...";

            try {
                const tx = db.transaction("jsonStore", "readonly");
                const store = tx.objectStore("jsonStore");
                const getRequest = store.get("myBigData");

                getRequest.onerror = function(event) {
                    handleError("Error retrieving data: " + event.target.errorCode);
                };

                getRequest.onsuccess = async function() {
                    const data = getRequest.result;
                    if (!data) {
                        handleError("No Spotify data found in database");
                        return;
                    }

                    statusMessage.textContent = "Data retrieved, generating visualization...";

                    try {
                        const response = await fetch("/account/dashboard", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-Requested-With": "XMLHttpRequest",
                                "X-CSRFToken": csrfToken,
                            },
                            body: JSON.stringify(data),
                        });

                        if (!response.ok) {
                            throw new Error(`Server responded with status: ${response.status}`);
                        }

                        // Get the image blob
                        const imageBlob = await response.blob();
                        
                        // Create image URL and display it
                        const imageUrl = URL.createObjectURL(imageBlob);
                        const img = document.createElement('img');
                        img.src = imageUrl;
                        img.style.maxWidth = '100%';
                        
                        // Clear any existing content and add the new image
                        const container = document.getElementById('dashboardContainer');
                        container.innerHTML = '';
                        container.appendChild(img);
                        
                        statusMessage.textContent = "Visualization complete!";
                    } catch (error) {
                        handleError("Error generating visualization: " + error.message);
                    }
                };
            } catch (error) {
                handleError("Transaction error: " + error.message);
            }
        };
    } catch (error) {
        handleError(error.message);
    } finally {
        visualizeBtn.disabled = false;
    }
}

function handleError(message) {
    console.error(message);
    statusMessage.textContent = message;
    statusMessage.className = "alert alert-danger";
    visualizeBtn.disabled = false;
}
