/**
 * Created by cc on 15-4-14.
 */
define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";

    var AppView = Backbone.View.extend({
        el:"body",
        role:$('#id_role'),
        btnRoleDisplay:$('#btnRoleDisplay'),
        //city_id:$('#id_city_id'),
        //btnCityDisplay:$('#btnCityDisplay'),
        //cinema:$('#id_cinema'),
        //btnCinemaDisplay:$('#btnCinemaDisplay'),
        //panelCinema:$('#panelCinema'),
        in_syncing:false,  //防止两重提交标志位

        events:{
            'click #btnSave':'save',
            'click .dropdownItem':'dropdownItem_click',
            'click #btnReturn':'return_to_prev_page'

        },

        initialize:function () {

        },

        save:function() {
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            $('#btnSave').prop('disabled', true);
            $('#frmAddUser').submit();
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
        },

        // 选择人员角色
        dropdownItem_click:function(event) {
            var element = $(event.target);
            var source = element.attr('for');
            if (source === 'id_role') {
                this.role.val(element.attr('value'));
                this.btnRoleDisplay.text(element.text());
                // 如果选择了影院，就显示影院下拉框
                if (element.attr('value') === '3') {
                    this.panelCinema.show();
                } else {
                    this.panelCinema.hide();
                }
            } else if (source === 'id_city_id'){
                this.city_id.val(element.attr('value'));
                this.btnCityDisplay.text(element.text());
            } else {
                this.cinema.val(element.attr('value'));
                this.btnCinemaDisplay.text(element.text());
            }
        }
    });
    return AppView;
});