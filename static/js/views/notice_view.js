/**
 * Created by cc on 15-4-15.
 */
define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";

    var AppView = Backbone.View.extend({
        el:"body",

        events:{
            'click #btnReturn':'return_to_prev_page',
        },

        initialize:function () {

        },

        // 返回
        return_to_prev_page:function() {
            var ru = $('#redirect_url');
            var url;
            if (!ru || ru.length === 0 || !ru.val()) {
                url = '/notice/list/';
            }else {
                url = ru.val();
            }
            window.location.href = url;
        }
    });
    return AppView;
});