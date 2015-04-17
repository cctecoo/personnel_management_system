/**
 * Created by cc on 15-4-16.
 */
define([
    'require',
    'jquery',
    'backbone',
    'datepicker',
    'datetimepicker'
], function (require, $, Backbone, ZeroClipboard) {
    "use strict";

    return Backbone.View.extend({
        el: "body",
        in_syncing: false,  //防止两重提交标志位

        events:{
            'click .dropdownItem': 'dropdownItem_click',
            //'click #btnReturn': 'return_to_prev_page',
            'click #btnSave': 'save_click',
            'click .goods_edit': 'onGoodsEditClicked',
            'click .btn-goods-edit': 'onGoodsEditEnterClicked',
            'click #checkSelectAll':'selectAll',
            'change .list_selector':'selectorChanged',
            'click #btnDelete':'remove_click' //删除
        },

        initialize:function() {
            $('#id_start_date').datepicker().on('changeDate', function(event) {
                $(event.target).datepicker('hide');
            });
            $('#id_end_date').datepicker().on('changeDate', function(event) {
                $(event.target).datepicker('hide');
            });
            $('.goods_match').datetimepicker({
                format: 'yyyy-MM-dd hh:mm',
                pickSeconds: false,
                language: 'zh-CN'
            });

            $('#btnSave').popover({
                placement: "top",
                trigger: "hover",
                title: "提示",
                delay: {show:1000, hide:100},
                content: "保存活动信息的修改。"
            });

            $(document).ready(function() {
                $('.tip').tooltip();
            });
        },

        onGoodsEditClicked: function(event) {
            event.preventDefault(); // prevent navigation
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var url = $(event.target).data("form"); // get the contact form url
            $.ajax({
                type: "GET",
                url: url,
                success: function(data){
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        var goodsForm = $("#frmEditGoods", data);
                        $('#goodsFormModal').html(goodsForm);
                        $('.goods_match').datetimepicker({
                            format: 'yyyy-MM-dd hh:mm',
                            pickSeconds: false,
                            language: 'zh-CN'
                        });
                        $("#goodsFormModal").modal('show');
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

        onGoodsEditEnterClicked: function(){
            event.preventDefault(); // prevent navigation
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var form = $('#frmEditGoods');
            $.ajax({
                type: "POST",
                url: form.attr('action'),
                data: form.serialize(), // serializes the form's elements.
                success: function(data) {
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        var goodsForm = $("#frmEditGoods", data);
                        $('#goodsFormModal').html(goodsForm);
                        var validation = $('#id_validation').val();
                        if (validation === "True") {
                            var url = "/activity/" + $('#pk').val() + "/goods/list/";
                            $.ajax({
                                type: "GET",
                                url: url,
                                success: function(data){
                                    if (data.error_code > 0) {
                                        window.alert(data.error_msg);
                                    }else {
                                        $('#goodsList').html(data);
                                        $('.tip').tooltip();
                                    }
                                },
                                error: function(){
                                    window.alert('与服务器通讯发生错误，请稍后重试。');
                                }
                            });
                            $("#goodsFormModal").modal('hide');
                        }else {
                            $('.goods_match').datetimepicker({
                                format: 'yyyy-MM-dd hh:mm',
                                pickSeconds: false,
                                language: 'zh-CN'
                            });
                        }
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
            return false; // avoid to execute the actual submit of the form.
        },

        // 保存
        save_click:function() {
            //防止两重提交
            //if (this.in_syncing) {
            //    return;
            //}
            //this.in_syncing = true;
            //$('#btnSave').prop('disabled', true);
            //
            //$('#frmEditInfo').submit();
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var form = $('#frmEditInfo');
            $.ajax({
                type: "GET",
                url: form.attr('action'),
                success: function(data){
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        var validation = $('#id_validation').val();
                        if (validation === "True") {
                            $('.tip').tooltip();
                            alert("hah");

                        }
                        else {
                            alert("error");
                        }
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
        },

        // 选择
        dropdownItem_click:function(event) {
            var element = $(event.target);
            var id = element.attr('for');
            $("#" + id).val(element.attr('value'));
            $("#" + id + '_trigger').text(element.text());
        },


        // 删除数据
        remove_click:function () {
            // 删除确认对话框
            if (!window.confirm("警告，请确认是否要删除选中的商品？")) {
                return;
            }

            $('#btnDelete').addClass('disabled');

            var pks = '';
            $('.list_selector:checked').each(function (index, value) {
                pks = pks + $(value).attr('pk') + ',';
            });
            $('#id_goods_pks').val(pks);

            event.preventDefault(); // prevent navigation
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var form = $('#frmGoodsList');
            $.ajax({
                type: "POST",
                url: form.attr('action'),
                data: form.serialize(), // serializes the form's elements.
                success: function(data) {
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        $('#goodsList').html(data);
                        $('#id_goods_pks').val('');
                        $('.tip').tooltip();
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
            $('#btnDelete').removeClass('disabled');
            return false; // avoid to execute the actual submit of the form.
        },

        // 选中全部
        selectAll:function () {
            $('.list_selector').prop('checked', $('#checkSelectAll').prop('checked'));
            this.toggleCommandButtonStatus();
        },

        // 选择框变更状态
        selectorChanged:function () {
            this.toggleCommandButtonStatus();
            $('#checkSelectAll').prop('checked', $('.list_selector').length === $('.list_selector:checked').length);
        },

        // 一览前置选择框状态变化使用
        toggleCommandButtonStatus:function () {
            if ($('#btnDelete')) {
                var selectedNumToBeDeleted = $('.list_selector:checked').length;
                $('#btnDelete').prop('disabled', selectedNumToBeDeleted === 0);
                if (selectedNumToBeDeleted !== 0) {
                    $('#btnDelete').removeClass('disabled');
                } else {
                    $('#btnDelete').addClass('disabled');
                }
            }
        }

    });
});