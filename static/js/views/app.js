define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";

    return Backbone.View.extend({
        el:"body",
        in_ajax_working:false,

        // ajax访问开始事件
        start_ajax_sync:function() {
            if (this.in_ajax_working) {
                return;
            }
            this.in_ajax_working = true;
            // 显示ajax logo
            this.ajax_logo.fadeIn();
        },

        // ajax访问结束事件
        finish_ajax_sync:function() {
            this.ajax_logo.fadeOut();
            this.in_ajax_working = false;
        },

        // 当前网址加入返回队列
        get_next_link:function() {
            var current_url = window.location.pathname + window.location.search;
            return "next=" + encodeURIComponent(current_url);
        },

        initialize:function() {
            this.url_path = $('#url_path').val();
            var url_path = this.url_path;
            $('[active-by-url]').each(function(){
                var regx = new RegExp($(this).attr('active-by-url'));
                if (url_path.match(regx)) {
                    $(this).addClass('active');
                }
            });

            // 所有的按钮采用bootstrap tooltip，要生效必须设定title
            $('.btn').tooltip({
                delay:{show:200, hide:100}
            });

            // 页面上如果存在default_button，则绑定enter键事件
            $(this.el).live('keydown', function(event){
                if (event.keyCode === 13) {
                    var default_button;
                    var priority = 0;
                    var default_buttons = $('.default_button');
                    for (var i =0; i < default_buttons.length; i++) {
                        var obj = default_buttons[i];
                        if (!default_button) {
                            default_button = obj;
                        }
                        if ($(obj).attr('default_priority')) {
                            var p = parseInt($(obj).attr('default_priority'), 10);
                            if (p > priority) {
                                priority = p;
                                default_button = obj;
                            }
                        }
                    }
                    if (default_button) {
                        $(default_button).trigger('click');
                        return false;
                    }
                }
                return true;
            });

            // 聚焦到第一个控件
            $('.first_focus').focus();
            // 聚焦到出错控件的第一个
            $('.error_flg').first().focus();

            // 初始化ajax logo
            this.ajax_logo = $('<div id="ajax_logo"><img src="/static/img/ajax-loader.gif"/></div>');
            this.ajax_logo.appendTo(this.el);
            this.on('start_ajax_sync', this.start_ajax_sync);
            this.on('finish_ajax_sync', this.finish_ajax_sync);

            // 限制输入
            $('.numberic_only').on('keydown', function(event) {
                // 只能输入0~9, Enter Delete Tab
                if ((event.keyCode < 48 || event.keyCode > 57) && $.inArray(event.keyCode, [8, 9, 13]) === -1) {
                    event.stopPropagation();
                    return false;
                }
            });

            // 加载其他的脚本
            var appModule = $('#amd_module');
            if (appModule.length > 0) {
                var currentView = this;
                require([appModule.val()], function(OtherApp) {
                    return new OtherApp({parentView:currentView});
                });
            }
        }
    });
});