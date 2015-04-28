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
            'click .dropdownItem': 'dropdownItem_click'
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

                // 状态初期化
                $('.status').editable({
                    emptytext: '空',
                    source: [
                        {value: 0, text: '实习'},
                        {value: 1, text: '在职'},
                        {value: 2, text: '离职'}
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

            });
        },

        // 选择
        dropdownItem_click:function(event) {
            var element = $(event.target);
            var td = "#" + element.parents('.cell_center').attr('id');
            var id = element.attr('for');
            $(td+" #" + id + '_trigger').text(element.text());

            var department_id = element.attr('value');

            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var url = $(event.target).data("url"); // get the contact form url
            $.ajax({
                type: "POST",
                url: url,
                data: {personal_id : element.parents('.cell_center').attr('id'),  department_id : department_id },
                success: function(data){
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                        alert('error');
                    }else {
                        $('.tip').tooltip();
                        //alert('编辑成功');
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
            return true;
            //return false; // prevent the click propagation
        }

    });
    return AppView;
});