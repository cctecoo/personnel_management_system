/**
 * Created by cc on 15-4-30.
 */
define([
    'require',
    'jquery',
    'backbone',
], function (require, $, Backbone) {
    "use strict";

    var AppView;
    AppView = Backbone.View.extend({
        el:"body",
        in_syncing:false, //防止两重提交标志位

        // 一览分页使用 开始--------------------------
        queryString:{
            'from':parseInt($('#qs_from').val()),
            'limit':parseInt($('#qs_limit').val()),
            'to':parseInt($('#qs_to').val())
        },
        total_count:parseInt($('#total_count').val()),
        url:'/comprehensive/check_in/'+$('#user_id').val()+'/?',
        btnNextPage:$('#btnNextPage'),
        btnPrevPage:$('#btnPrevPage'),
        lblPageCounter:$('#lblPageCounter'),
        //一览分页使用 结束--------------------------

        // 事件定义
        events:{
            'click .btn-success':'check_in'  //签到
        },

        // 初始化
        initialize:function () {
            // 签到按钮提示信息
            $('.btn-success').popover({
                placement: "right",
                trigger: "hover",
                title: "提示",
                delay: {show:1000, hide:100},
                content: "一天可以签到多次，统计首次和末次。"
            });

            this.initPaginationStatus();
        },

        // 签到
        check_in:function(event) {
            var element = $(event.target);

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
                data: {personal_id : $('#personal_id').val()},
                success: function(data){
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                        alert('error');
                    }else {
                        $('.tip').tooltip();
                        alert('签到成功');

                        var url = "/comprehensive/check_in/" + $('#user_id').val() + "/list/";
                        $.ajax({
                            type: "GET",
                            url: url,
                            success: function(data){
                                if (data.error_code > 0) {
                                    window.alert(data.error_msg);
                                }else {
                                    $('#CheckInList').html(data);
                                    $('.tip').tooltip();

                                    $('.btn-success').popover({
                                    placement: "right",
                                    trigger: "hover",
                                    title: "提示",
                                    delay: {show:1000, hide:100},
                                    content: "一天可以签到多次，统计首次和末次。"
                            });

                                }
                            },
                            error: function(){
                                window.alert('与服务器通讯发生错误，请稍后重试。');
                            }
                        });

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
        },

        // 一览分页元素初始化使用
        initPaginationStatus:function() {
            var url,fr;

            //前页
            if (this.queryString.from <= 0) {
                this.btnPrevPage.addClass('disabled');
            }else {
                fr = this.queryString.from - this.queryString.limit;
                if (fr < 0){
                    fr = 0;
                }
                url = this.url;
                url = url + 'lm=' + encodeURIComponent(this.queryString.limit);
                if (fr > 0) {
                    url = url + '&fr=' + encodeURIComponent(String(fr));
                }
                this.btnPrevPage.find('a').prop('href', url);
            }

            //次页
            if (this.queryString.from + this.queryString.limit >= this.total_count) {
                this.btnNextPage.addClass('disabled');
            }else {
                fr = this.queryString.from + this.queryString.limit;
                url = this.url;
                url = url + 'fr=' + encodeURIComponent(fr);
                url = url + '&lm=' + encodeURIComponent(this.queryString.limit);
                this.btnNextPage.find('a').prop('href', url);
            }

            // 页面
            var page_number = Math.ceil(this.total_count / this.queryString.limit);
//            if (this.total_count % this.queryString.limit !== 0) {
//                page_number = page_number + 1;
//            }
            var current_page = this.queryString.from / this.queryString.limit + 1;
            this.lblPageCounter.text(current_page + "/" + page_number + "页");
        }

    });
    return AppView;
});