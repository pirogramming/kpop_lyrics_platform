$('.main-searchtxt').focus(
    function () {
        $('#main_wrap_2').css({'background-color': 'black', 'opacity': '0.7'});
        $('.main-searchbox').css({'box-shadow': '0px 0px 7px 2px white'})
    });

$('.main-searchtxt').blur(
    function () {
        $('#main_wrap_2').css({'background-color': 'transparent', 'opacity': '1'});
        $('.main-searchbox').css({'box-shadow': '0px 0px 0px 0px'});
        $(this).css("background-color", "white");
        $(this).css({'box-shadow': 'none'});
        setTimeout(function() {
            $('#livesearch_item_wrapper').css("display", "none");
        },300);

    });


var myTimeout;

$('.song1').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song5').css({'width': '100px', 'height': '100px'});
        $('.buffer2, .buffer3, .buffer4, .buffer5').css({'width': '125px', 'height': '125px'});
        $('.song1').css({'width': '350px', 'height': '350px',});
        $('.song1_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song1_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song5').css({'width': '200px', 'height': '200px'});
        $('.buffer2, .buffer3, .buffer4, .buffer5').css({'width': '0px', 'height': '0px'});
        $('.song1').css({'width': '200px', 'height': '200px',});
        $('.song1_name').css({'opacity': '0', 'display': 'none'});
    });
$('.song2').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song1, .song3, .song4, .song5').css({'width': '100px', 'height': '100px',});
        $('.buffer1, .buffer3, .buffer4, .buffer5').css({'width': '125px', 'height': '125px'});
        $('.song2').css({'width': '350px', 'height': '350px',});
        $('.song2_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song2_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song1, .song3, .song4, .song5').css({'width': '200px', 'height': '200px'});
        $('.buffer1, .buffer3, .buffer4, .buffer5').css({'width': '0px', 'height': '0px'});
        $('.song2').css({'width': '200px', 'height': '200px',});
        $('.song2_name').css({'opacity': '0', 'display': 'none'});
    });
$('.song3').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song1, .song4, .song5').css({'width': '100px', 'height': '100px',});
        $('.buffer1, .buffer2, .buffer4, .buffer5').css({'width': '125px', 'height': '125px'});
        $('.song3').css({'width': '350px', 'height': '350px',});
        $('.song3_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song3_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song1, .song4, .song5').css({'width': '200px', 'height': '200px'});
        $('.buffer1, .buffer2, .buffer4, .buffer5').css({'width': '0px', 'height': '0px'});
        $('.song3').css({'width': '200px', 'height': '200px',});
        $('.song3_name').css({'opacity': '0', 'display': 'none'});
    });

$('.song4').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song1, .song5').css({'width': '100px', 'height': '100px',});
        $('.buffer1, .buffer2, .buffer3, .buffer5').css({'width': '125px', 'height': '125px'});
        $('.song4').css({'width': '350px', 'height': '350px',});
        $('.song4_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song4_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song1, .song5').css({'width': '200px', 'height': '200px'});
        $('.buffer1, .buffer2, .buffer3, .buffer5').css({'width': '0px', 'height': '0px'});
        $('.song4').css({'width': '200px', 'height': '200px',});
        $('.song4_name').css({'opacity': '0', 'display': 'none'});
    });
$('.song5').hover(
    function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song1').css({'width': '100px', 'height': '100px',});
        $('.buffer1, .buffer2, .buffer3, .buffer4').css({'width': '125px', 'height': '125px'});
        $('.song5').css({'width': '350px', 'height': '350px',});
        $('.song5_name').css({'display': 'block', 'opacity': '0'});
        myTimeout = setTimeout(function () {
            $('.song5_name').animate({'opacity': '0.7'}, 500);
        }, 1000);
    }, function () {
        clearTimeout(myTimeout);
        $('.song2, .song3, .song4, .song1').css({'width': '200px', 'height': '200px'});
        $('.buffer1, .buffer2, .buffer3, .buffer4').css({'width': '0px', 'height': '0px'});
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