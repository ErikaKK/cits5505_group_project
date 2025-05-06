const accountMenu = document.getElementById('account-menu');
const accountMenuItems = document.getElementById('account-menu-items');

function hideAccountMenu(event) {
    if (!accountMenuItems.contains(event.target)) {
        accountMenu.classList.add('hidden');
        document.removeEventListener('click', hideAccountMenu);
    }
}

function showAccountMenu() {
    accountMenu.classList.remove('hidden');
    document.addEventListener('click', hideAccountMenu);
}

document.getElementById('account-menu-toggle').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent the click from reaching the document
    if (accountMenu.classList.contains('hidden')) {
        showAccountMenu();
    } else {
        hideAccountMenu(event);
    }
});

document.getElementById('logout').addEventListener('click',deleteDatabase);
// Function to delete the database for a fresh start
function deleteDatabase() {
    const dbName = "MyDatabase";
    
    if (confirm("Are you sure to log out?")) {
       
        console.log(`Attempting to delete database: ${dbName}`);
        
        const deleteRequest = indexedDB.deleteDatabase(dbName);
        
        deleteRequest.onsuccess = function() {
            console.log(`Database "${dbName}" deleted successfully`);
           
        };
        
        deleteRequest.onerror = function(event) {
            console.error("Error deleting database:", event.target.error);
           
        };
    }
}