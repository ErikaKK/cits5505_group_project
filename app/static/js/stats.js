document.getElementById("upload-btn").addEventListener("click",handleFileUpload);

const requiredFields = [
  "ts",
  "platform",
  "ms_played",
  "conn_country",
  "master_metadata_track_name",
  "master_metadata_album_artist_name",
  "spotify_track_uri"
];

function handleFileUpload() {

  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
    
  if (!file) {
    alert('Please select a JSON file.');
    return;
  }
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const jsonData = JSON.parse(e.target.result);
      const isValid = jsonData.every(entry =>
        requiredFields.every(field => field in entry)
      );
      if (isValid) {
        localStorage.setItem('uploadedJsonData', JSON.stringify(jsonData));
      alert('Data successfully stored in local storage.');
      } else {
        alert("Missing required fields");
      }
      
    
    } catch (error) {
      console.error('Error parsing JSON:', error);
      alert('Invalid JSON file.');
    }
  };
  reader.readAsText(file);
     
}

const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');

fileInput.addEventListener('change', function() {
  if (fileInput.files.length > 0) {
    fileLabel.textContent = fileInput.files[0].name;
  } else {
    fileLabel.textContent = 'Select a file';
  }
});


document.getElementById('history-data').addEventListener("click",function(event){
  if (localStorage.getItem('uploadedJsonData')) {
    // go to the dashboard
  }else{
    alert("Couldn't get data. Please upload!")
  }
})