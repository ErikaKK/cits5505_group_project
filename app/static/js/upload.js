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
function handleFileUpload() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  statusDiv.textContent = "Processing file...";

  if (!file) {
    statusDiv.textContent = "Please select a JSON file.";
    return;
  }

  const reader = new FileReader();
  reader.onload = function (e) {
    try {
      const jsonData = JSON.parse(e.target.result);

      // Validate it's an array
      if (!Array.isArray(jsonData)) {
        throw new Error("JSON data must be an array");
      }

      const isValid = jsonData.every((entry) =>
        requiredFields.every((field) => field in entry)
      );

      if (isValid) {
        // Store the entire array directly

        createOrOpenDatabase(jsonData);
      } else {
        statusDiv.textContent = "Missing required fields in the JSON data";
      }
    } catch (error) {
      console.error("Error parsing JSON:", error);
      statusDiv.textContent = `Error: ${error.message}`;
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
