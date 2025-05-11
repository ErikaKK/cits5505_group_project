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

document
  .getElementById("upload-btn")
  .addEventListener("click", handleFileUpload);

// Handle file upload
function handleFileUpload(e) {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  statusDiv.textContent = "Processing file...";

  if (!file) {
    statusDiv.textContent = "Please select a JSON file.";
    return;
  }

  // Validate file type
  if (file.type !== "application/json") {
    statusDiv.textContent = "Please upload a JSON file.";
  }

  const reader = new FileReader();
  reader.onload = function (e) {
    try {
      const jsonData = JSON.parse(e.target.result);

      // Validate it's contents
      if (!Array.isArray(jsonData)) {
        throw new Error(
          "Invalid JSON format: please read through the instructions."
        );
      }

      const isValid = jsonData.every((entry) =>
        requiredFields.every((field) => field in entry)
      );

      if (!isValid) {
        throw new Error("Missing required fields in JSON data.");
      }

      // upload via endpoint
      const formData = new FormData();
      formData.append("json_file", file);

      fetch("/account/shared_data/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((result) => {
          if (result.success) {
            statusDiv.textContent =
              "Uploaded file now has been successfully saved!";
          } else {
            throw new Error(result.error);
          }
        })
        .catch((error) => {
          statusDiv.textContent = `Upload failed due to: ${error.message}`;
        });
    } catch (error) {
      statusDiv.textContent = `Invalid JSON format: please read through the instructions. Error: ${error.message}`;
    }
  };

  reader.readAsText(file);
}

// change the label of the file input field
const fileInput = document.getElementById("fileInput");
const fileLabel = document.getElementById("fileLabel");

fileInput.addEventListener("change", function () {
  if (fileInput.files.length > 0) {
    fileLabel.textContent = fileInput.files[0].name;
  } else {
    fileLabel.textContent = "Select a file";
  }
});
