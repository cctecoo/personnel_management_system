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
            'click #btnEdit':'goto_edit'
        },

        initialize:function () {

        },

        goto_edit:function() {
            var id = $('#id_pk').val();
            var url = '/account/edit/' + id + '/';
            window.location.href = url + '?' + this.options.parentView.get_next_link();
        },

        // 返回用户一览
        return_to_prev_page:function() {
            var ru = $('#redirect_url');
            var url;
            if (!ru || ru.length === 0 || !ru.val()) {
                url = '/account/list/';
            }else {
                url = ru.val();
            }
            window.location.href = url;
        }
    });
    return AppView;
});