/**
 * Created by cc on 15-4-13.
 */
define([
    'backbone'
], function(Backbone) {
    "use strict";

    return Backbone.Router.extend({
        initialize: function(options) {
            if (options['sender']) {
                this.sender = options['sender'];
            }
        },

        routes:{
            'manage_terminals':'manage_terminals'
        },

        manage_terminals:function() {
            if (this.sender && this.sender.manage_terminals) {
                this.sender.manage_terminals();
            }
        }
    });
});