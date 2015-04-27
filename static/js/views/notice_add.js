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

    var AppView = Backbone.View.extend({
        el:"body",
        in_syncing:false,  //防止两重提交标志位

        events:{
            'click #btnSave':'save',
            'click #btnReturn':'return_to_prev_page'

        },

        initialize:function () {
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
            // 前端check不通过直接return
            if (!this.validate()) {
                return;
            }

            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            $('#btnSave').prop('disabled', true);
            $('#frmAddNotice').submit();
        },

        // 前端check检查
        validate:function(){
            //待完善
            var content = $("textarea#addContent").val();
            if (content == ''){
                alert("通知内容不能为空");
                return false;
            }

            return true;
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
    return AppView;
});