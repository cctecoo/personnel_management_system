/**
 * Created by cc on 15-4-15.
 */
define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";

    return Backbone.View.extend({
        el:"body",
        in_syncing:false,  //防止两重提交标志位
        role:$('#id_role'),
        btnRoleDisplay:$('#btnRoleDisplay'),

        events:{
            'click .dropdownItem':'dropdownItem_click',
            'click #btnReturn':'return_to_prev_page',
            'click #btnSave':'save'
        },

        initialize:function () {
            var ru = $('#redirect_url');
            if (ru && ru.val() === '') {
                $('#btnReturn').hide();
            }
        },

        save:function() {
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            var txtPassword = $('#txtPassword');
            if (txtPassword.val() === '') {
                txtPassword.prop('disabled', true);
            }
            $('#btnSave').prop('disabled', true);

            $('#frmEditUser').submit();
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
            }
        }
    });
});