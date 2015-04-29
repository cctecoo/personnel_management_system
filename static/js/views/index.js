/**
 * Created by cc on 15-4-14.
 */
define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";
    return Backbone.View.extend({
        el:"body",

        events:{
        },

        initialize:function(parent) {
            this.parentView = parent;
            //$('.carousel').carousel({
            //  interval: 1000
            //})
            $('#myCarousel').carousel()
        }

    });
});