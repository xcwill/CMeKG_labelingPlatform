(function($) {
  'use strict';
  $(function() {

    $('[data-toggle="expansionPanel"]').on('click', function() {
      $('#' + $(this).attr("target-panel")).toggleClass('expanded');
    });

    /* Dropdown */
    $('[data-toggle="dropdown"]').on('click', function() {
      var menuEl = document.querySelector('#' + $(this).attr("toggle-dropdown"));
      var menu = new mdc.menu.MDCSimpleMenu(menuEl);
      menu.open = !menu.open;
    });

    mdc.autoInit();

    /* Select menu */
    var MDCSelect = mdc.select.MDCSelect;
    if ($('#hero-js-select').length) {
      var heroSelect = document.getElementById('hero-js-select');
      var heroSelectComponent = new mdc.select.MDCSelect(heroSelect);
    }

    /* text field */
    if ($('#tf-box-example').length) {
      var tfEl = document.getElementById('tf-box-example');
      var tf = new mdc.textField.MDCTextField(tfEl);
    }
    if ($('#demo-tf-box-wrapper').length) {
      var wrapper = document.getElementById('demo-tf-box-wrapper');
    }
    if ($('#tf-box-leading-example').length) {
      var tfBoxLeadingEl = document.getElementById('tf-box-leading-example');
      var tfBoxLeading = new mdc.textField.MDCTextField(tfBoxLeadingEl);
    }
    if ($('#demo-tf-box-leading-wrapper').length) {
      var wrapperBoxLeading = document.getElementById('demo-tf-box-leading-wrapper');
    }
    if ($('#tf-outlined-example').length) {
      var tfEl = document.getElementById('tf-outlined-example');
      var tf = new mdc.textField.MDCTextField(tfEl);
    }
    if ($('#demo-tf-outlined-wrapper').length) {
      var wrapper = document.getElementById('demo-tf-outlined-wrapper');
    }
  });
})(jQuery);