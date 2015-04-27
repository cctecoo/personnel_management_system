/**
 * Created by cc on 15-4-23.
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

        events:{
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
            $('#btnSave').prop('disabled', true);

            $('#frmEditDepartment').submit();
        },

        // 返回部门一览
        return_to_prev_page:function() {
            var ru = $('#redirect_url');
            var url;
            if (!ru || ru.length === 0 || !ru.val()) {
                url = '/comprehensive/department/list/';
            }else {
                url = ru.val();
            }
            window.location.href = url;
        }

    });
});