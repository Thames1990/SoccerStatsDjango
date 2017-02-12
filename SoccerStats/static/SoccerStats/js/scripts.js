(function ($) {
    "use strict";

    $('body').scrollspy({
        target: '.fixed-top',
        offset: 60
    });

    new WOW().init();

    // TODO Update
    $('a.page-scroll').bind('click', function (event) {
        var $ele = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($ele.attr('href')).offset().top - 60)
        }, 1450, 'easeInOutExpo');
        event.preventDefault();
    });

    // TODO Update
    $('#collapsingNavbar').find('li a').click(function () {
        // Always close responsive nav after click
        $('.navbar-toggler:visible').click();
    });
})(jQuery);