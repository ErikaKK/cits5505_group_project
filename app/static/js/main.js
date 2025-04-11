const menu = document.getElementById('navbar-menu');
const menuItems = document.getElementById('navbar-menu-items');

document.getElementById('menu-toggle').addEventListener('click', function () {
    menu.classList.remove('hidden');
  });

menu.addEventListener('click', (event) => {
    if (!menuItems.contains(event.target) && menu.classList.contains('fixed')) {    
        menu.classList.toggle('hidden');
    }
  });