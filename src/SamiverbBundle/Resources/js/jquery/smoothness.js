var navbarPadding = parseInt($('body').css('padding-top').replace("px", ""));

function scrollToTarget(target) {
  var $target = $(target);

  $('html, body').stop().animate({
    'scrollTop': $target.offset().top - navbarPadding
  }, 2000, 'easeInOutCubic');
}

$(document).ready( function() {

  $(window).scroll( function() {
    if ($(window).scrollTop() >= ($('#conjugations').offset().top - navbarPadding - 250)) {
      $('#goToTop').fadeIn();
    } else {
      $('#goToTop').fadeOut();
    }
  });

});