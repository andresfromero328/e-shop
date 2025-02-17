function dropMenu() {
   const dropdown_btn = document.querySelector('#menu-btn');
   const drop_menu = document.querySelector('#drop-menu')
   if (dropdown_btn) {
      dropdown_btn.addEventListener('click', () => {
         drop_menu.classList.toggle('show');
      })
   }
}

dropMenu();