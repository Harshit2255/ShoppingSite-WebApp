$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

jQuery.noConflict();

jQuery(document).ready(
    function($) {
        $('.plus-cart').click(function() {
            let id = $(this).attr('pid').toString();
            var eml = this.parentNode.children[2];
            $.ajax({
                type: "GET",
                url: "/pluscart",
                data: {
                    prod_id : id
                },
                success: function (data) {
                    eml.innerText = data.quantity;   
                    document.getElementById('curAmt').innerText = data.amount;
                    document.getElementById('curTot').innerText = data.total;
                }
            });
        }) 
    }
)

jQuery(document).ready(
    function($) {
        $('.minus-cart').click(function() {
            let id = $(this).attr('pid').toString();
            var eml = this.parentNode.children[2];
            $.ajax({
                type: "GET",
                url: "/minuscart",
                data: {
                    prod_id : id
                },
                success: function (data) {
                    eml.innerText = data.quantity;   
                    document.getElementById('curAmt').innerText = data.amount;
                    document.getElementById('curTot').innerText = data.total;
                }
            });
        }) 
    }
)

jQuery(document).ready(
    function($) {
        $('.remove-cart').click(function() {
            let id = $(this).attr('pid').toString();
            var elm = this;
            $.ajax({
                type: "GET",
                url: "/removecart",
                data: {
                    prod_id : id
                },
                success: function (data) {  
                    document.getElementById('curAmt').innerText = data.amount;
                    document.getElementById('curTot').innerText = data.total;
                    elm.parentNode.parentNode.parentNode.parentNode.remove();
                }
            });
        }) 
    }
)

