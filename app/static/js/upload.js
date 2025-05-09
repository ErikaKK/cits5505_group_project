const statusDiv = document.getElementById('status');
        
// Required fields for validation
const requiredFields = [
    "ts",
    "platform",
    "ms_played",
    "conn_country",
    "master_metadata_track_name",
    "master_metadata_album_artist_name",
    "spotify_track_uri"
];


document.getElementById("upload-btn").addEventListener("click", handleFileUpload);


// Handle file upload
function handleFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    statusDiv.textContent = "Processing file...";
    
    
    if (!file) {
        statusDiv.textContent = 'Please select a JSON file.';
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const jsonData = JSON.parse(e.target.result);
            
            // Validate it's an array
            if (!Array.isArray(jsonData)) {
                throw new Error("JSON data must be an array");
            }
            
            const isValid = jsonData.every(entry =>
                requiredFields.every(field => field in entry)
            );
            
            if (isValid) {
                // Store the entire array directly
                const cleanedJsonData = cleanSpotifyData(jsonData);
                createOrOpenDatabase(cleanedJsonData);
            } else {
                statusDiv.textContent = "Missing required fields in the JSON data";
            }
        } catch (error) {
            console.error('Error parsing JSON:', error);
            statusDiv.textContent = `Error: ${error.message}`;
            return
        }
    };
    
    reader.readAsText(file);
    // window.location.href = '/account/dashboard';
}

// Function to create or open database with correct versioning
function createOrOpenDatabase(data) {
    const dbName = "MyDatabase";
    const storeName = "jsonStore";
    const key = "myBigData";
    
    const checkRequest = indexedDB.open(dbName);
    
    checkRequest.onerror = function(event) {
        console.error("Error checking database:", event.target.error);
        statusDiv.textContent = `Database check error: ${event.target.error.message}`;
    };
    
    checkRequest.onsuccess = function(event) {
        const db = event.target.result;
        const currentVersion = db.version;
        
        // Check if our store exists
        const storeExists = Array.from(db.objectStoreNames).includes(storeName);
       
        // Close current connection
        db.close();
        
        if (!storeExists) {
            // Need to increment version to trigger upgrade
            const newVersion = currentVersion + 1;
            openAndSave(dbName, storeName, key, data, newVersion);
        } else {
            // Store exists, use current version
            openAndSave(dbName, storeName, key, data, currentVersion);
        }
    };
}

// Function to open DB with correct version and save data
function openAndSave(dbName, storeName, key, data, version) {
    statusDiv.textContent = `Opening database (version ${version})...`;
    
    const request = indexedDB.open(dbName, version);
    
    request.onupgradeneeded = function(event) {
        statusDiv.textContent = "Creating object store...";
        const db = event.target.result;
        
        // Create the object store if it doesn't exist
        if (!db.objectStoreNames.contains(storeName)) {
            db.createObjectStore(storeName);
        }
    };
    
    request.onerror = function(event) {
        console.error("Database error:", event.target.error);
        statusDiv.textContent = `Database error: ${event.target.error.message}`;
    };
    
    request.onsuccess = function(event) {
        statusDiv.textContent = "Database opened, saving data...";
        const db = event.target.result;
        
        try {
            // Start a transaction
            const transaction = db.transaction([storeName], "readwrite");
            
            transaction.onerror = function(event) {
                console.error("Transaction error:", event.target.error);
                statusDiv.textContent = `Transaction error: ${event.target.error.message}`;
            };
            
            const objectStore = transaction.objectStore(storeName);
            
            // Delete any existing data with the same key
            const deleteRequest = objectStore.delete(key);
            
            deleteRequest.onsuccess = function() {
                
                // Add the new data
                const addRequest = objectStore.add(data, key);
                
                addRequest.onsuccess = function() {
                    statusDiv.textContent = "✅ Data successfully stored in IndexedDB!";
                };
                
                addRequest.onerror = function(event) {
                    console.error("Error saving data:", event.target.error);
                    statusDiv.textContent = `Error saving data: ${event.target.error.message}`;
                };
            };
            
            deleteRequest.onerror = function(event) {
                console.error("Error deleting old data:", event.target.error);
                const addRequest = objectStore.add(data, key);
                
                addRequest.onsuccess = function() {
                    statusDiv.textContent = "✅ Data successfully stored in IndexedDB!";
                };
            };
        } catch (err) {
            console.error("Error in database operations:", err);
            statusDiv.textContent = `Error: ${err.message}`;
        }
    };
}

function cleanSpotifyData(jsonData) {
    if (!Array.isArray(jsonData)) {
        throw new Error('Data must be an array');
    }

    const cleanedData = jsonData.map(item => {
        // Basic validation and cleaning
        const ts = item.ts ? item.ts.trim() : null;
        const ms_played = parseInt(item.ms_played);
        const track_name = item.master_metadata_track_name ? 
            item.master_metadata_track_name.trim() : null;
        const artist_name = item.master_metadata_album_artist_name ? 
            item.master_metadata_album_artist_name.trim() : null;

        return {
            ts,
            ms_played,
            master_metadata_track_name: track_name,
            master_metadata_album_artist_name: artist_name
        };
    }).filter(item => 
        // Remove invalid entries
        item.ts && 
        !isNaN(item.ms_played) && 
        item.ms_played > 0 &&
        item.master_metadata_track_name && 
        item.master_metadata_album_artist_name
    );

    return cleanedData;
}

// change the label of the file input field
const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');

fileInput.addEventListener('change', function() {
  if (fileInput.files.length > 0) {
    fileLabel.textContent = fileInput.files[0].name;
  } else {
    fileLabel.textContent = 'Select a file';
  }
});