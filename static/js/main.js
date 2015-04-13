require.config({
    shim: {
        'underscore': {
            exports: '_'
        },
        'backbone': {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        'jquery': {
            exports: '$'
        },
        'datepicker': {
            deps: ['bootstrap', 'jquery'],
            exports: 'datepicker'
        }
    },
    paths: {
        underscore: 'lib/underscore-min',
        backbone: 'lib/backbone-min',
        bootstrap: 'lib/bootstrap-min',
        datepicker: 'lib/bootstrap-datepicker',
        datetimepicker: 'lib/bootstrap-datetimepicker'
    }
});

require([
    'views/app',
    'csrf_ajax_fix',
    'bootstrap'
], function(AppView) {
    "use strict";
    // Constructors are functions that are designed to be used with the new prefix.
    // The new prefix creates a new object based on the function's prototype,
    // and binds that object to the function's implied this parameter.
    // If you neglect to use the new prefix, no new object will be made and this will be bound to the global object.
    // This is a serious mistake.
    // According to http://stackoverflow.com/questions/2381253/what-side-effects-does-the-keyword-new-have-in-javascript
    var app = new AppView();
});

