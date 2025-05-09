
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

      const request = indexedDB.open("MyDatabase", 2);

      request.onerror = function (event) {
        handleError("Failed to open database: " + event.target.errorCode);
      };

      request.onsuccess = function (event) {
        const db = event.target.result;
        statusMessage.textContent = "Database opened, retrieving data...";


        try {
          const tx = db.transaction("jsonStore", "readonly");
          const store = tx.objectStore("jsonStore");
          const getRequest = store.get("myBigData");

          getRequest.onerror = function (event) {
            handleError("Error retrieving data: " + event.target.errorCode);
          };

          getRequest.onsuccess = function () {
            const data = getRequest.result;
            if (!data) {
              handleError("No Spotify data found in database");
              return;
            }

            statusMessage.textContent = "Data retrieved, validating...";
    

            // Validate data has required fields
            if (!validateData(data)) {
              handleError("Data is missing required fields");
              return;
            }

            statusMessage.textContent = "Sending data to server...";
      

            fetch("/dashboard", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrfToken,
              },
              body: JSON.stringify(data),
            })
              .then((response) => {
                if (!response.ok) {
                  throw new Error(
                    `Server responded with status: ${response.status}`
                  );
                }
                return response.json();
              })
              .then((responseData) => {
                if (responseData.success && responseData.redirect_url) {
                    // Redirect to the Dash app
                    window.location.href = responseData.redirect_url;
                } else {
                    throw new Error('Invalid response from server');
                }
            })
              .catch((err) => {
                handleError("Error sending to Flask: " + err.message);
              });
          };
        } catch (e) {
          handleError("Transaction error: " + e.message);
        }
      };
    }

    function validateData(data) {
      // Check if data is an array
      if (!Array.isArray(data)) {
        console.error("Data is not an array");
        return false;
      }

      // Check if first element has required fields
      if (data.length > 0) {
        const firstItem = data[0];
        for (const field of requiredFields) {
          if (!(field in firstItem)) {
            console.error(`Missing required field: ${field}`);
            return false;
          }
        }
        return true;
      }

      return data.length > 0;
    }

    function handleError(message) {
      console.error(message);
      statusMessage.textContent = message;
      statusMessage.className = "alert alert-danger";

      visualizeBtn.disabled = false;
    }
