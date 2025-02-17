function addToCart() {
      const cart_btn = document.getElementById('buy');
      const cart_counter = document.getElementById('cart-counter')
      if (cart_btn) {
         cart_btn.addEventListener('click', () => {
            cart_counter.classList.toggle('active-cart');
            console.log('active')
         });
      }

}

addToCart();