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
    console.log("Processing file...");
    
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
                console.log("JSON is valid, proceeding to save");
                createOrOpenDatabase(jsonData);
            } else {
                statusDiv.textContent = "Missing required fields in the JSON data";
            }
        } catch (error) {
            console.error('Error parsing JSON:', error);
            statusDiv.textContent = `Error: ${error.message}`;
        }
    };
    
    reader.readAsText(file);
}

// Function to create or open database with correct versioning
function createOrOpenDatabase(data) {
    const dbName = "MyDatabase";
    const storeName = "jsonStore";
    const key = "myBigData";
    
    console.log("Checking if database exists");
    
    // First open without version to check current state
    const checkRequest = indexedDB.open(dbName);
    
    checkRequest.onerror = function(event) {
        console.error("Error checking database:", event.target.error);
        statusDiv.textContent = `Database check error: ${event.target.error.message}`;
    };
    
    checkRequest.onsuccess = function(event) {
        const db = event.target.result;
        const currentVersion = db.version;
        console.log("Current database version:", currentVersion);
        
        // Check if our store exists
        const storeExists = Array.from(db.objectStoreNames).includes(storeName);
        console.log("Store exists:", storeExists);
        
        // Close current connection
        db.close();
        
        if (!storeExists) {
            // Need to increment version to trigger upgrade
            const newVersion = currentVersion + 1;
            console.log(`Store doesn't exist. Opening with new version: ${newVersion}`);
            openAndSave(dbName, storeName, key, data, newVersion);
        } else {
            // Store exists, use current version
            console.log("Store exists. Using current version");
            openAndSave(dbName, storeName, key, data, currentVersion);
        }
    };
}

// Function to open DB with correct version and save data
function openAndSave(dbName, storeName, key, data, version) {
    statusDiv.textContent = `Opening database (version ${version})...`;
    console.log(`Opening database ${dbName} with version ${version}`);
    
    const request = indexedDB.open(dbName, version);
    
    request.onupgradeneeded = function(event) {
        statusDiv.textContent = "Creating object store...";
        console.log("Database upgrade needed");
        const db = event.target.result;
        
        // Create the object store if it doesn't exist
        if (!db.objectStoreNames.contains(storeName)) {
            console.log(`Creating object store: ${storeName}`);
            db.createObjectStore(storeName);
        }
    };
    
    request.onerror = function(event) {
        console.error("Database error:", event.target.error);
        statusDiv.textContent = `Database error: ${event.target.error.message}`;
    };
    
    request.onsuccess = function(event) {
        console.log("Database opened successfully");
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
                console.log("Deleted old data (if any)");
                
                // Add the new data
                console.log("Adding new data...");
                const addRequest = objectStore.add(data, key);
                
                addRequest.onsuccess = function() {
                    console.log("Data saved successfully!");
                    statusDiv.textContent = "✅ Data successfully stored in IndexedDB!";
                    // You could call verifyDataSaved here
                };
                
                addRequest.onerror = function(event) {
                    console.error("Error saving data:", event.target.error);
                    statusDiv.textContent = `Error saving data: ${event.target.error.message}`;
                };
            };
            
            deleteRequest.onerror = function(event) {
                console.error("Error deleting old data:", event.target.error);
                // Continue anyway, try to add the new data
                const addRequest = objectStore.add(data, key);
                
                addRequest.onsuccess = function() {
                    console.log("Data saved successfully!");
                    statusDiv.textContent = "✅ Data successfully stored in IndexedDB!";
                };
            };
        } catch (err) {
            console.error("Error in database operations:", err);
            statusDiv.textContent = `Error: ${err.message}`;
        }
    };
}

// Function to verify data was saved (for debugging)
function verifyDataSaved(db, storeName, key) {
    const transaction = db.transaction([storeName], "readonly");
    const objectStore = transaction.objectStore(storeName);
    const getRequest = objectStore.get(key);
    
    getRequest.onsuccess = function(event) {
        const result = event.target.result;
        if (result) {
            console.log("Verification successful: Data is in the database");
            if (Array.isArray(result) && result.length > 0) {
                console.log("Sample data:", result[0]);
            }
        } else {
            console.error("Verification failed: No data found with key:", key);
        }
    };
}

// Function to check what's in the database
function checkDataInIndexedDB() {
    const dbName = "MyDatabase";
    const storeName = "jsonStore";
    const key = "myBigData";
    
    statusDiv.textContent = "Checking database...";
    console.log("Checking IndexedDB database...");
    
    // List all databases (only works in some browsers)
    if (indexedDB.databases) {
        indexedDB.databases().then(databases => {
            console.log("Available databases:", databases);
        }).catch(err => {
            console.log("Could not list databases (might be unsupported in this browser)");
        });
    }
    
    const request = indexedDB.open(dbName);
    
    request.onerror = function(event) {
        console.error("Error opening database:", event.target.error);
        statusDiv.textContent = `Error opening database: ${event.target.error.message}`;
    };
    
    request.onsuccess = function(event) {
        const db = event.target.result;
        console.log("Database opened successfully:", db.name);
        console.log("Database version:", db.version);
        console.log("Object stores:", Array.from(db.objectStoreNames));
        
        let statusMessage = `Database "${db.name}" (version ${db.version})<br>`;
        statusMessage += `Object stores: ${Array.from(db.objectStoreNames).join(", ") || "none"}<br>`;
        
        if (!db.objectStoreNames.contains(storeName)) {
            statusMessage += `⚠️ Object store "${storeName}" does not exist!`;
            statusDiv.innerHTML = statusMessage;
            return;
        }
        
        try {
            const transaction = db.transaction([storeName], "readonly");
            const objectStore = transaction.objectStore(storeName);
            const getRequest = objectStore.get(key);
            
            getRequest.onsuccess = function(event) {
                const result = event.target.result;
                if (result) {
                    console.log("Data found with key:", key);
                    if (Array.isArray(result)) {
                        console.log("Data is an array with", result.length, "items");
                        if (result.length > 0) {
                            console.log("First item sample:", result[0]);
                        }
                        statusMessage += `✅ Found data: Array with ${result.length} items`;
                    } else {
                        console.log("Data found but is not an array:", typeof result);
                        statusMessage += `✅ Found data (type: ${typeof result})`;
                    }
                } else {
                    console.log("No data found with key:", key);
                    statusMessage += `⚠️ No data found with key "${key}"`;
                }
                statusDiv.innerHTML = statusMessage;
            };
            
            getRequest.onerror = function(event) {
                console.error("Error getting data:", event.target.error);
                statusMessage += `⚠️ Error getting data: ${event.target.error.message}`;
                statusDiv.innerHTML = statusMessage;
            };
        } catch (err) {
            console.error("Error in transaction:", err);
            statusMessage += `⚠️ Error: ${err.message}`;
            statusDiv.innerHTML = statusMessage;
        }
    };
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