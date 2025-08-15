/**
 * Automatically calculates and updates the price preview
 * based on the selected design type and size from the inputs.
 */

document.addEventListener('DOMContentLoaded', function (){
    const designInput = document.getElementById('id_design_type');
    const sizeInput = document.getElementById('id_size');
    const pricePreview = document.getElementById('price-preview');

    function updatePrice() {
        let price = 0;

        switch(designInput.value) {
            case 'icon':
            price += 15.55;
            break;
            case 'logo':
            price +=25.55;
            break;
            case 'poster':
            price +=35.55;
            break;
        }

         switch(sizeInput.value) {
            case 'small':
            price += 5;
            break;
            case 'medium':
            price +=10;
            break;
            case 'large':
            price +=20;
            break;
        }

        pricePreview.textContent = price.toFixed(2);
    }

    
    designInput.addEventListener('change', updatePrice);
    sizeInput.addEventListener('change', updatePrice);
    updatePrice();
});