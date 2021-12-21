(function($) {
  'use strict';
  $(function() {
    var body = $('body');
    var contentWrapper = $('.content-wrapper');
    var scroller = $('.container-scroller');
    var footer = $('.footer');
    var sidebar = $('.mdc-drawer-menu');

    // Menu Toggle Function
    var drawerEl = document.querySelector('.mdc-persistent-drawer');
    var MDCPersistentDrawer = mdc.drawer.MDCPersistentDrawer;
    var drawer = new MDCPersistentDrawer(drawerEl);
    document.querySelector('.menu-toggler').addEventListener('click', function() {
      drawer.open = !drawer.open;
    });

    //Add active class to nav-link based on url dynamically
    //Active class can be hard coded directly in html file also as required
    var current = location.pathname.split("/").slice(-1)[0].replace(/^\/|\/$/g, '');
    $('.mdc-drawer-item .mdc-drawer-link', sidebar).each(function() {
      var $this = $(this);
      if (current === "") {
        //for root url
        if ($this.attr('href').indexOf("index.html") !== -1) {
          $(this).addClass('active');
          if ($(this).parents('.mdc-expansion-panel').length) {
            $(this).closest('.mdc-expansion-panel').addClass('expanded');
          }
        }
      } else {
        //for other url
        if ($this.attr('href').indexOf(current) !== -1) {
          $(this).addClass('active');
          if ($(this).parents('.mdc-expansion-panel').length) {
            $(this).closest('.mdc-expansion-panel').addClass('expanded');
          }
        }
      }
    })

    $(".mdc-toolbar__menu-icon").on("click", function(){
      $(".body-wrapper .page-wrapper .content-wrapper").toggleClass("drawer-minimized");
    });
  });
})(jQuery);