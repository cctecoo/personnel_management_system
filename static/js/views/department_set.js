/**
 * Created by cc on 15-4-23.
 */
define([
    'require',
    'jquery',
    'backbone',
    'editable'
], function (require, $, Backbone) {
    "use strict";

    var AppView;
    AppView = Backbone.View.extend({
        el:"body",
        in_syncing:false, //防止两重提交标志位

        // 事件定义
        events:{
            'click .btn-process-confirm': 'onProcessConfirm',
            'click #btnReturn':'return_to_prev_page'
        },

        // 初始化
        initialize:function () {
            // 确定按钮提示信息
            $('#btnNext').popover({
                placement: "top",
                trigger: "hover",
                title: "提示",
                delay: {show:1000, hide:100},
                content: "请再次确认您的操作信息，以免出现误操作。"
            });

            $(document).ready(function() {

                $('.tip').tooltip();
                if($('#excluded_error').val() == 1){
                    $('[name="data-type"]').editable({
                        disabled: true
                    });
                }else{
                    $('.tip').tooltip();
                    // 状态初期化
                    $('.status').editable({
                        emptytext: '空',
                        source: [
                            {value: 0, text: '实习'},
                            {value: 1, text: '在职'},
                            {value: 9, text: '离职'}
                        ],
                        success: function(data){
                            if (data.error_code > 0) {
                                return data.error_msg;
                            }
                        },
                        error: function(){
                            return '与服务器通讯发生错误，请稍后重试。';
                        }
                    });
                };
            });
        },

        // 下一步
        onProcessConfirm: function(event) {
            event.preventDefault(); // prevent navigation
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var url = '/order/' + $('#order_id').val() + '/detail/confirm/'; // get the contact form url
            $.ajax({
                type: "GET",
                url: url,
                success: function(data){
                    if (data.error_code > 0) {
                        $('#process-confirm').modal('hide');
                        $('#confirm-error-message').text(data.error_msg);
                        $(".alert").show();
                    }else {
                        window.location.href = '/comprehensive/department/list/';
                    }
                },
                error: function(){
                    window.alert('与服务器通讯发生错误，请稍后重试。');
                },
                complete: function(){
                    //防止两重提交
                    //恢复现场
                    current_view.options.parentView.trigger('finish_ajax_sync');
                    current_view.in_syncing = false;
                }
            });
            return false; // prevent the click propagation
        },

        // 返回用户一览
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
    return AppView;
});