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
