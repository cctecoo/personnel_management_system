/**
 * Created by cc on 15-4-27.
 */
define([
    'require',
    'jquery',
    'backbone',
    'datetimepicker'
], function (require, $, Backbone) {
    "use strict";

    return Backbone.View.extend({
        el:"body",
        in_syncing:false,  //防止两重提交标志位

        events:{
            'click #btnReturn':'return_to_prev_page',
            'click #btnSave':'save'
        },

        initialize:function () {
            var ru = $('#redirect_url');
            if (ru && ru.val() === '') {
                $('#btnReturn').hide();
            }
            $(".start_date").datetimepicker({
                format: 'yyyy-MM-dd hh:mm',
                // 忽略秒数
                pickSeconds: false
            });
            $(".end_date").datetimepicker({
                format: 'yyyy-MM-dd hh:mm',
                // 忽略秒数
                pickSeconds: false
            });
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

            $('#frmEditNotice').submit();
        },

        // 返回公告一览
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
});