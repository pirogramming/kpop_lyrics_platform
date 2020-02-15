$('#searchbox').hover(function () {
    // $('#main_wrap_2').css({'background': 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5))'});
}, function () {
    // $('#main_wrap_2').css({'background': 'transparent'})
});

$('.main-searchbox').hover(
    function () {
        $('#main_wrap_2').css({'background-color': 'black', 'opacity': '0.5'});
        $(this).css({'box-shadow': '0px 0px 7px 2px white'})
    }, function () {
        $('#main_wrap_2').css({'background-color': 'transparent', 'opacity': '1'});
        $(this).css("background-color", "white");
        $(this).css({'box-shadow': 'none'})

    });


var myTimeout;

$('.song1').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song5').css({'width': '100px', 'height': '100px'});
        $('.song1').css({'width': '350px', 'height': '350px',});
        $('.song1_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song1_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song5').css({'width': '200px', 'height': '200px'});
        $('.song1').css({'width': '200px', 'height': '200px',});
        $('.song1_name').css({'opacity': '0', 'display': 'none'});
    });
$('.song2').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song1, .song3, .song4, .song5').css({'width': '100px', 'height': '100px',});
        $('.song2').css({'width': '350px', 'height': '350px',});
        $('.song2_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song2_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song1, .song3, .song4, .song5').css({'width': '200px', 'height': '200px'});
        $('.song2').css({'width': '200px', 'height': '200px',});
        $('.song2_name').css({'opacity': '0', 'display': 'none'});
    });
$('.song3').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song1, .song4, .song5').css({'width': '100px', 'height': '100px',});
        $('.song3').css({'width': '350px', 'height': '350px',});
        $('.song3_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song3_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song1, .song4, .song5').css({'width': '200px', 'height': '200px'});
        $('.song3').css({'width': '200px', 'height': '200px',});
        $('.song3_name').css({'opacity': '0', 'display': 'none'});
    });

$('.song4').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song1, .song5').css({'width': '100px', 'height': '100px',});
        $('.song4').css({'width': '350px', 'height': '350px',});
        $('.song4_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song4_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song1, .song5').css({'width': '200px', 'height': '200px'});
        $('.song4').css({'width': '200px', 'height': '200px',});
        $('.song4_name').css({'opacity': '0', 'display': 'none'});
    });
$('.song5').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song1').css({'width': '100px', 'height': '100px',});
        $('.song5').css({'width': '350px', 'height': '350px',});
        $('.song5_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song5_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song1').css({'width': '200px', 'height': '200px'});
        $('.song5').css({'width': '200px', 'height': '200px',});
        $('.song5_name').css({'opacity': '0', 'display': 'none'});
    });


var slideIndex = 0;
showSlides();

function showSlides() {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
    setTimeout(showSlides, 2000); // Change image every 2 seconds
}

function plusSlides(n) {
    selectSlides(slideIndex += n);
}

function currentSlide(n) {
    selectSlides(slideIndex = n);
}

function selectSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}