/**
 * Created by cc on 15-5-3.
 */
define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";

    var AppView = Backbone.View.extend({
        el:"body",
        in_syncing:false,  //防止两重提交标志位

        // 一览分页使用 开始--------------------------
        queryString:{
            'from':parseInt($('#qs_from').val()),
            'limit':parseInt($('#qs_limit').val()),
            'to':parseInt($('#qs_to').val()),
            'order_direction':$('#qs_order_direction').val(),
            'order_field':$('#qs_order_field').val()
        },
        total_count:parseInt($('#total_count').val()),
        url:'/comprehensive/check_in/all/list/?',
        btnNextPage:$('#btnNextPage'),
        btnPrevPage:$('#btnPrevPage'),
        lblPageCounter:$('#lblPageCounter'),
        //一览分页使用 结束--------------------------

        // 事件定义
        events:{
            'click .data_column':'sortColumn', // 排序
            'click #btnSearch':'search' //根据关键字搜索
        },

        // 初始化
        initialize:function () {
            this.initPaginationStatus();
            this.initColumnOrderStatus();
        },

        // 排序列状态初始化
        initColumnOrderStatus:function() {
            // 初始化排序列的表头
            var logo_css;
            if (this.queryString.order_direction === '-') {
                logo_css = 'icon-arrow-down';
            }else {
                logo_css = 'icon-arrow-up';
            }
            $('.data_column[sort_key=' + this.queryString.order_field + ']').append('<li class="' + logo_css + '"></li>');

        },

        // 搜索
        search:function() {
            var queryKey = $('#queryKey').val();
            queryKey = $.trim(queryKey);
            var url = this.url;
            url = url + 'lm=' + encodeURIComponent(this.queryString.limit);
            url = url + '&fr=' + encodeURIComponent(this.queryString.from);
            if (this.queryString.order_field) {
                url = url + '&of=' + encodeURIComponent(this.queryString.order_field);
                if (this.queryString.order_direction === '-') {
                    url = url + '&od=-';
                }
            }
            url = url + '&q=' + encodeURIComponent(queryKey);
            window.location.href = url;
        },

        // 列排序
        sortColumn:function(event) {
            var url = this.url;
            url = url + 'lm=' + encodeURIComponent(this.queryString.limit);
            url = url + '&fr=' + encodeURIComponent(this.queryString.from);
            var od = '-';
            if (this.queryString.order_direction === '-') {
                od = '';
            }
            var of = $(event.target).attr('sort_key');

            if (of) {
                url = url + '&of=' + encodeURIComponent(of);
                if (od === '-') {
                    url = url + '&od=-';
                }
            }
            window.location.href = url;
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
                if (this.queryString.order_field) {
                    url = url + '&of=' + encodeURIComponent(this.queryString.order_field);
                    if (this.queryString.order_direction === '-') {
                        url = url + '&od=-';
                    }
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
                if (this.queryString.order_field) {
                    url = url + '&of=' + encodeURIComponent(this.queryString.order_field);
                    if (this.queryString.order_direction === '-') {
                        url = url + '&od=-';
                    }
                }
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