const statusDiv = document.getElementById("status");

// Required fields for validation
const requiredFields = [
    "ts",
    "platform",
    "ms_played",
    "conn_country",
    "master_metadata_track_name",
    "master_metadata_album_artist_name",
    "spotify_track_uri",
];

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

document
    .getElementById("upload-btn")
    .addEventListener("click", handleFileUpload);

async function handleFileUpload(e) {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    statusDiv.textContent = "Processing file...";

    if (!file) {
        statusDiv.textContent = "Please select a JSON file.";
        return;
    }

    if (file.type !== "application/json") {
        statusDiv.textContent = "Please upload a JSON file.";
        return;
    }

    try {
        const jsonData = await readFileAsJSON(file);

        // Validate contents
        if (!Array.isArray(jsonData)) {
            throw new Error("Invalid JSON format: please read through the instructions.");
        }

        const isValid = jsonData.every((entry) =>
            requiredFields.every((field) => field in entry)
        );

        if (!isValid) {
            throw new Error("Missing required fields in JSON data.");
        }

        // Upload via endpoint
        const formData = new FormData();
        formData.append("json_file", file);

        const response = await fetch("/account/upload-file", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData,
            credentials: 'same-origin'
        });

        const result = await response.json();

        if (response.status === 409) {
            // Handle data overlap with conflicts
            const shouldReplace = await showConflictDialog(result.details);
            if (shouldReplace) {
                // Send request to replace data
                const replaceResponse = await fetch("/account/replace-data", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({ new_data: jsonData }),
                    credentials: 'same-origin'
                });

                const replaceResult = await replaceResponse.json();
                if (replaceResult.success) {
                    statusDiv.textContent = "Data replaced successfully!";
                } else {
                    throw new Error(replaceResult.error);
                }
            } else {
                statusDiv.textContent = "Upload cancelled due to data conflict.";
            }
        } else if (result.success) {
            let message = result.message;
            if (result.details) {
                if (result.details.new_entries_added) {
                    message += ` (${result.details.new_entries_added} new entries added)`;
                }
                if (result.details.overlapping_dates) {
                    message += `, ${result.details.overlapping_dates} overlapping dates with identical data`;
                }
            }
            statusDiv.textContent = message;
        } else {
            throw new Error(result.error || 'Unknown error occurred');
        }
    } catch (error) {
        statusDiv.textContent = `Error: ${error.message}`;
    }
}

function readFileAsJSON(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const jsonData = JSON.parse(e.target.result);
                resolve(jsonData);
            } catch (error) {
                reject(new Error("Invalid JSON format"));
            }
        };
        reader.onerror = () => reject(new Error("Error reading file"));
        reader.readAsText(file);
    });
}

function showConflictDialog(details) {
  return new Promise((resolve) => {
      if (!details) {
          resolve(false);
          return;
      }

      const message = `
          Found different data in ${details.overlapping_dates} overlapping dates.
          
          Would you like to:
          - OK: Replace existing data with new data
          - Cancel: Keep existing data
      `;

      const shouldReplace = confirm(message);
      resolve(shouldReplace);
  });
}

// File input label update
const fileInput = document.getElementById("fileInput");
const fileLabel = document.getElementById("fileLabel");

fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name;
    } else {
        fileLabel.textContent = "Select a file";
    }
});
