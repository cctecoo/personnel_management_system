/**
 * Created by cc on 15-4-23.
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
        btnEdit:$('#btnEdit'),
        btnDelete:$('#btnDelete'),

        // 事件定义
        events:{
            'click #checkSelectAll':'selectAll',
            'change .list_selector':'selectorChanged',
            'click #btnSearch':'search', //根据关键字搜索
            'click #btnDelete':'deleteUser', //删除部门
            'click #btnEdit':'editUser' //编辑部门
        },

        // 初始化
        initialize:function () {
            this.toggleCommandButtonStatus();
            this.addRefToEditLink();
        },


        // 编辑连接上附加回调地址
        addRefToEditLink:function() {
            var currentView = this;
            // 修正编辑连接
            $('.edit_link').each(function(index, obj) {
                var href = $(obj).prop('href');
                if (href.indexOf('?') > 0) {
                    href = href + '&';
                }else {
                    href = href + '?';
                }
                href += currentView.options.parentView.get_next_link();
                $(obj).attr('href', href);
            });
        },

        // 搜索
        search:function() {
            var queryKey = $('#queryKey').val();
            queryKey = $.trim(queryKey);
            var url = '/comprehensive/department/list/?';
            url = url + 'q=' + encodeURIComponent(queryKey);
            window.location.href = url;
        },

        // 删除数据
        deleteUser:function() {
            //防止两重提交
            if (this.in_syncing) return;
            this.in_syncing = true;
            this.btnDelete.prop('disabled', true);
            this.btnDelete.addClass('disabled');
            this.undelegateEvents();

            var pk = '';
            $('.list_selector:checked').each(function(index, value) {
                pk = pk + $(value).attr('pk') + ',';
            });
            $('#pk').val(pk);

            var url = '/comprehensive/department/list/?';
            $('#redirect_url').val(url);
            $('#frmDeleteDepartment').submit();
        },

        // 编辑部门
        editUser:function() {
            var pk = $('.list_selector:checked').attr('pk');
            var url = '/comprehensive/department/edit/' + pk + '/';
            window.location.href = url + '?' + this.options.parentView.get_next_link();
        },

        // 选中全部
        selectAll:function() {
            $('.list_selector').prop('checked', $('#checkSelectAll').prop('checked'));
            this.toggleCommandButtonStatus();
        },

        // 选择框变更状态
        selectorChanged:function() {
            this.toggleCommandButtonStatus();
            $('#checkSelectAll').prop('checked', $('.list_selector').length === $('.list_selector:checked').length);
        },


        // 一览前置选择框状态变化使用
        toggleCommandButtonStatus:function() {
            var selectedNum = $('.list_selector:checked').length;
            if (this.btnEdit) {
                this.btnEdit.prop('disabled', selectedNum !== 1);
                if (selectedNum === 1) {
                    this.btnEdit.removeClass('disabled');
                }else {
                    this.btnEdit.addClass('disabled');
                }
            }
            if (this.btnDelete) {
                this.btnDelete.prop('disabled', selectedNum === 0);
                if (selectedNum !== 0) {
                    this.btnDelete.removeClass('disabled');
                }else {
                    this.btnDelete.addClass('disabled');
                }
            }
        }
    });
    return AppView;
});