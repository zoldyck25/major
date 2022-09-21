/**
*
* -----------------------------------------------------------------------------
*
* Template : Tekhub - Multipurpose Startups HTML5 Template
* Author : rs-theme
* Author URI : http://rstheme.com/ 

* -----------------------------------------------------------------------------
*
**/

(function($) {
    "use strict";

    // sticky menu
    var header = $('.menu-sticky');
    var win = $(window);

    win.on('scroll', function() {
       var scroll = win.scrollTop();
       if (scroll < 1) {
           header.removeClass("sticky");
       } else {
           header.addClass("sticky");
       }

        $("section").each(function() {
        var elementTop = $(this).offset().top - $('#rs-header').outerHeight();
            if(scroll >= elementTop) {
                $(this).addClass('loaded');
            }
        });

    });

    // Revolution Slider Js Start
    jQuery(document).ready(function() {
        jQuery('#rev_slider_1').show().revolution({
            autoHeight: 'on',
            minHeight: [950, 950, 500, 500],
            gridheight: 500,
            delay: 8000,
            stopLoop: 'on',
            stopAfterLoops: 0,
            stopAtSlide: 1,
            sliderLayout: 'fullwidth',
            fullScreenAlignForce: 'off',
            boxshadow: 0,
            responsiveLevels: [1440, 1199, 991, 767],
            gridwidth: [1380, 1110, 930, 690],

            parallax: {
                type: 'mouse+scroll',
                origo: 'slidercenter',
                speed: 1000,
                levels: [10,7,4,3,2,5,4,3,2,1],
                disable_onmobile: 'on'
            },
            navigation: {
                arrows: {
                    enable: false,
                    style: 'zeus',
                    tmp: '<div class="tp-title-wrap"><div class="tp-arr-imgholder"></div></div>',
                },
                bullets: {
                    enable: false,
                    style: "hesperiden",
                    hide_onleave: false,
                    h_align: "center",
                    v_align: "bottom",
                    h_offset: 0,
                    v_offset: 20,
                    space: 5
                }
            }
        });
    });
    // Revolution Slider Js End

    
    var rs_skillbar = $('.skillbar');
    if(rs_skillbar.length){
    // Skill bar            
        $('.skillbar').skillBars({  
            from: 0,    
            speed: 4000,    
            interval: 100,  
            decimals: 0,    
        });
    }



    //banner-slider home6
    var $owl = $('#rs-apps-slider');
    $owl.children().each( function( index ) {
      $(this).attr( 'data-position', index ); // NB: .attr() instead of .data()
    });
    $owl.owlCarousel({
        center: true,
        loop: true,
        items: 3,
    });
    $(document).on('click', '#rs-apps-slider .owl-item>div', function() {
        var $speed = 300;  // in ms
        $owl.trigger('to.owl.carousel', [$(this).data( 'position' ), $speed] );
    });
    
    

    $('.rs-faq-section .card').click(function(event){
        $('.rs-faq-section .card').removeClass('current');
        $(this).addClass('current');
        event.preventDefault();
    });



	// Testimonial Slider
    var rs_sliderfor = $('.slider-for');
    if(rs_sliderfor.length){
        $('.slider-for').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: false,
            asNavFor: '.slider-nav',
        });
    }

    var rs_slidernav = $('.slider-nav');
    if(rs_slidernav.length){
        $('.slider-nav').slick({
            slidesToShow: 3,
            slidesToScroll: 1,
            asNavFor: '.slider-for',
            dots: false,
            arrows: false,
            vertical: true,
            centerMode: true,
            centerPadding: '0',
            focusOnSelect: true,
            directionNav: true,
            responsive: [
                {
                    breakpoint: 768,
                    settings: {
                        vertical: false,
                    }
                }
              ]
        });
    }

    /*-------------------------------------
        OwlCarousel
    -------------------------------------*/

    $('.rs-carousel').each(function() {
        var owlCarousel = $(this),

        // lg device
        loop = owlCarousel.data('loop'),
        items = owlCarousel.data('items'),
        margin = owlCarousel.data('margin'),
        dots = owlCarousel.data('dots'),
        nav = owlCarousel.data('nav'),
        autoplay = owlCarousel.data('autoplay'),
        smartSpeed = owlCarousel.data('smart-speed'),
        stagePadding = owlCarousel.data('stage-padding'),
        autoplayTimeout = owlCarousel.data('autoplay-timeout'),
        center= owlCarousel.data('center'),
        hoverPause = owlCarousel.data('hoverpause'),

        // md device
        itemsMd = owlCarousel.data('items-md'),
        navMd = owlCarousel.data('nav-md'),
        dotsMd = owlCarousel.data('dots-md'),
        marginMd = owlCarousel.data('margin-md'),
        centerMd = owlCarousel.data('center-md'),

        // sm device
        itemsSm = owlCarousel.data('items-sm'),
        navSm = owlCarousel.data('nav-sm'),
        dotsSm = owlCarousel.data('dots-sm'),
        marginSm = owlCarousel.data('margin-sm'),

        // xs device
        itemsXs = owlCarousel.data('items-xs'),
        navXs = owlCarousel.data('nav-xs'),
        marginXs = owlCarousel.data('margin-xs'),
        dotsXs = owlCarousel.data('dots-xs');

        owlCarousel.owlCarousel({
            
            // Default Function
            loop: (loop ? true : false),
            lazyLoad: true,
            autoplayHoverPause: (hoverPause ? true : false),
            autoplay: (autoplay ? true : false),
            autoplayTimeout: (autoplayTimeout ? autoplayTimeout : 1000),
            smartSpeed: (smartSpeed ? smartSpeed : 250),
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsiveClass: true,
            responsive: {

                // xs device
                0: {
                    items: (itemsXs ? itemsXs : 1),
                    nav: (navXs ? true : false),
                    dots: (dotsXs ? true : false),
                    center: false,
                    margin: (marginXs ? marginXs : 0),
                },

                // sm device
                576: {
                    items: (itemsSm ? itemsSm : 3),
                    nav: (navSm ? true : false),
                    dots: (dotsSm ? true : false),
                    center: false,
                    margin: (marginSm ? marginSm : 0),
                },

                // md device
                768: {
                    items: (itemsMd ? itemsMd : 4),
                    nav: (navMd ? true : false),
                    dots: (dotsMd ? true : false),
                    center: (centerMd ? true : false),
                    margin: (marginMd ? marginMd : 0),
                },

                // lg device
                992: {
                    items: (items ? items : 4),
                    margin: (margin ? margin : 0),
                    dots: (dots ? true : false),
                    nav: (nav ? true : false),
                    center: (center ? true : false),
                }
            }
        });
    });


    // Counter Up
    if ($('.rs-counter').length) {  
        $('.rs-counter').counterUp({
            delay: 20,
            time: 1500
        });
    }

    //window load
   $(window).on( 'load', function() {
        $("#loading").delay(1500).fadeOut(500);
        $("#loading-center").on( 'click', function() {
        $("#loading").fadeOut(500);
        })
    })

   // Elements Animation
    if ($('.wow').length) {
        var wow = new WOW(
            {
                boxClass: 'wow', // animated element css class (default is wow)
                animateClass: 'animated', // animation css class (default is animated)
                offset: 0, // distance to the element when triggering the animation (default is 0)
                mobile: false, // trigger animations on mobile devices (default is true)
                live: true       // act on asynchronously loaded content (default is true)
            }
        );
        wow.init();
    }

    // magnificPopup init
    var imagepopup = $('.image-popup');
    if(imagepopup.length) {
        $('.image-popup').magnificPopup({
            type: 'image',
            callbacks: {
                beforeOpen: function() {
                   this.st.image.markup = this.st.image.markup.replace('mfp-figure', 'mfp-figure animated zoomInDown');
                }
            },
            gallery: {
                enabled: true
            }
        });
    }

    // scrollTop init
    var totop = $('#scrollUp'); 
    if(totop.length){   
        win.on('scroll', function() {
            if (win.scrollTop() > 150) {
                totop.fadeIn();
            } else {
                totop.fadeOut();
            }
        });
        totop.on('click', function() {
            $("html,body").animate({
                scrollTop: 0
            }, 500)
        });
    }

    /*----------------------------
    Single Product js active
    ------------------------------ */

    var single_product_image = $('.single-product-image');
    if(single_product_image.length) {
        $('.single-product-image').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: true,
            asNavFor: '.single-product-nav'
        });
    }

    var single_product_nav = $('.single-product-nav');
    if(single_product_nav.length) {
        $('.single-product-nav').slick({
            slidesToShow: 4,
            asNavFor: '.single-product-image',
            dots: false,
            focusOnSelect: true,
            centerMode:false,
            responsive: [
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 2
                  }
                },
                {
                  breakpoint: 591,
                  settings: {
                    slidesToShow: 2
                  }
                }
              ] 
        });
    }

    // image loaded portfolio init
    var gridfilter = $('.grid');
        if(gridfilter.length){
        $('.grid').imagesLoaded(function() {
            $('.gridFilter').on('click', 'button', function() {
                var filterValue = $(this).attr('data-filter');
                $grid.isotope({
                    filter: filterValue
                });
            });
            var $grid = $('.grid').isotope({
                itemSelector: '.grid-item',
                percentPosition: true,
                masonry: {
                    columnWidth: '.grid-item',
                }
            });
        });
    }   
        
    // project Filter
    if ($('.gridFilter button').length) {
        var projectfiler = $('.gridFilter button');
            if(projectfiler.length){
            $('.gridFilter button').on('click', function(event) {
                $(this).siblings('.active').removeClass('active');
                $(this).addClass('active');
                event.preventDefault();
            });
        }
    }

    // onepage nav
    var navclose = $('#onepage-menu');
    if(navclose.length){
        $(".nav-menu li").on("click", function () {
            if ($(".showhide").is(":visible")) {
                $(".showhide").trigger("click");
            }
        });
        
        if ($.fn.onePageNav) {
            $(".nav-menu").onePageNav({
                currentClass: "active-menu"
            });
        }
    }

    //Videos popup jQuery 
    var popup = $('.popup-videos');
    if(popup.length) {
        $('.popup-videos').magnificPopup({
            disableOn: 10,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        }); 
    }

    /*-------------------------------------
       #Countedown
    -------------------------------------*/
    var countdown_first = $('#countdown');
    if(countdown_first.length){
        var countDownDate = new Date("Nov 12 2020, 19:00:00").getTime();

            // Update the count down every 1 second
            var x = setInterval(function() {

            // Get today's date and time
            var now = new Date().getTime();
                
            // Find the distance between now and the count down date
            var distance = countDownDate - now;
                
            // Time calculations for days, hours, minutes and seconds
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
            // Output the result in an element with id="countdown"
            document.getElementById("countdown").innerHTML = "<div>" + days + "<span>days</span>" + "</div>" + "<div>" + hours + "<span>hour</span> " + "</div>"
              + "<div>" + minutes + "<span>min</span> " + "</div>" + "<div>" + seconds + "<span>sec</span>" + "</div>";
                
            // If the count down is over, write some text 
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("countdown").innerHTML = "Website Is Ready";
            }
        });
    }


    // Chat Box Active
    $(".chatbox-part .chat-icon i").on('click', function(){
        $(this).parents('.chatbox-part').children('.chatbox').toggleClass("active");
    });

	$(".chatbox-part .chatbox-top .close-icon i").on('click', function(){
        $(this).parents('.chatbox-part').children('.chatbox').removeClass("active");
    });

    //Vartical Testmonials Slider
    var $carousel = $('#carousel');
    var currdeg = 0;
    var radius = 100;
    var childCount = $('#carousel').children('.testimonial-item').length;
    var $childList = $('#carousel').children('.testimonial-item');
    var rotations = 0;

    $childList.each(function() {
        var opacity = 0; 
        var i = $(this).index();
        var z = radius * Math.cos(2 * Math.PI/childCount * i);
        var y = radius * Math.sin(2 * Math.PI/childCount * i);
        
        // var nextZ = radius * Math.cos(2 * Math.PI/childCount);
        // var nextY = radius * Math.sin(2 * Math.PI/childCount);
        // if(z == radius) {
        //   opacity = 1;
        // } else if (z == nextZ && y == nextY) {
        //   opacity = 0.5;
        // }
        
        $(this).css({
            "-webkit-transform": "translateZ("+z+"px) translateY("+y+"px) rotateX(0deg)",
            "-moz-transform": "translateZ("+z+"px) translateY("+y+"px) rotateX(0deg)",
            "-o-transform": "translateZ("+z+"px) translateY("+y+"px) rotateX(0deg)",
            "transform": "translateZ("+z+"px) translateY("+y+"px) rotateX(0deg)"
        });
    });



    $(".testimonial-item").on("click", function() {rotateHandler(-1, null)} );
    $(".go").on("click", function(e) {
    e.preventDefault();
        var data = $(this).data('index');
        goTo(data);
    });

    function rotateHandler(e, target = null){
    var count = e;
    var diff = 0;
    if(target != null) {
        diff = target;
    } else {
        var current = $('#carousel .testimonial-item.active').index();
        // console.log(current - count);
        if(current - count < 0 || current - count > (childCount-1) ) {
        diff = childCount - current - 1;
        } else {
        diff = current - count;
        }
    }
    // TARGET for ACTIVE
    var $target = $('#carousel .testimonial-item').eq(diff);
    
    var containerRotation = 360/childCount * count;
    currdeg = currdeg - containerRotation;
    var elemdeg = -currdeg;
    
    rotateElements(elemdeg);
    rotateContainer(currdeg);
    //UPDATE ACTIVE;
    $('#carousel .testimonial-item.active').removeClass('active');
    
    $target.addClass('active');

    }

    function rotateElements(elemdeg) {
    if(elemdeg < 0) { 
        var front = (Math.abs(elemdeg) / (360/childCount) % childCount);
    } else if(elemdeg > 0) {
        var front = childCount - ( (Math.abs(elemdeg) / (360/childCount) ) % childCount);
    } else {
        var front = 0;
    }
    var below = getNeighbors(front)[0];
    // console.log('front: ' + front);
    // console.log('below: ' + below);
    $childList.each(function() {
        var z = parseFloat( $(this).css('transform').split(',')[14] ).toFixed(4);
        var y = parseFloat( $(this).css('transform').split(',')[13] ).toFixed(4);
        var x = elemdeg;
        $(this).css({
        "-webkit-transform": "translateZ("+z+"px) translateY("+y+"px) rotateX("+x+"deg)",
        "-moz-transform": "translateZ("+z+"px) translateY("+y+"px) rotateX("+x+"deg)",
        "-o-transform": "translateZ("+z+"px) translateY("+y+"px) rotateX("+x+"deg)",
        "transform": "translateZ("+z+"px) translateY("+y+"px) rotateX("+x+"deg)"
        });
    });
    
    $('#carousel .testimonial-item.front').removeClass('front');
    $('#carousel .testimonial-item.below').removeClass('below');
    $('#carousel .testimonial-item').eq(front).addClass('front');
    $('#carousel .testimonial-item').eq(below).addClass('below');
    }
    
    function rotateContainer() {  
        var x = currdeg;
        $carousel.css({
            "-webkit-transform": "rotateX("+x+"deg)",
            "-moz-transform": "rotateX("+x+"deg)",
            "-o-transform": "rotateX("+x+"deg)",
            "transform": "rotateX("+x+"deg)"
        });
    }


    // Takes an index
    function goTo(target) {
    var current = $('#carousel .testimonial-item.active').index();
    var num = $('#carousel').children('.testimonial-item').length;
    // console.log('target: ' + target);
    // console.log('current: ' + current);
    // console.log('length: ' + num);
        var count = 0;
        if( target > current ){
        var dif = target - current;
        if( dif <= num/2 ){
            count = -dif;
        }else{
            count = (num - dif);
        }
        }else{
        var dif = current - target;
        if( dif <= num/2 ){
            count = dif;
        }else{
            count = -(num - dif);
        }
    }

    //console.log(count);
    rotateHandler(count, target);
    }

    function getNeighbors(index) {
    var above, below;
    if(index + 1 > (childCount - 1)) {
        below = 0;
    } else if (index + 1 ) {
        below = index + 1;
    }
    
    if(index - 1 < 0 ){
        above = childCount -1;
    } else {
        above = index - 1;
    }
    
    return [below, above];
    }

    function handleScroll(event) {
    event.preventDefault();
    console.log('scroll: ' + event.originalEvent.wheelDelta);
    if (event.originalEvent.wheelDelta > 1) {
        console.log('Scroll up');
        rotateHandler(1, null);
    }
    else if(event.originalEvent.wheelDelta < -1) {
        console.log('Scroll down');
        rotateHandler(-1, null);
    }
    }


    //preloader
    $(window).on( 'load', function() {
        $("#tekhub-load").delay(1000).fadeOut(500);
    })

    
})(jQuery);







