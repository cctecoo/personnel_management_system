/**
 * Created by cc on 15-4-16.
 */
define([
    'require',
    'jquery',
    'backbone',
    'datepicker',
    'datetimepicker'
], function (require, $, Backbone) {
    "use strict";

    return Backbone.View.extend({
        el: "body",
        in_syncing: false,  //防止两重提交标志位

        events:{
            'click .dropdownItem': 'dropdownItem_click',
            //'click #btnReturn': 'return_to_prev_page',
            'click #btnSave': 'save_click',
            'click .job_edit': 'onJobEditClicked',
            'click .btn-job-edit': 'onJobEditEnterClicked',  //job
            'click .education_edit': 'onEducationEditClicked',
            'click .btn-education-edit': 'onEducationEditEnterClicked',  //education
            'click #checkSelectAll':'selectAll',
            'change .list_selector':'selectorChanged',
            'click #btnDelete':'remove_click' //删除
        },

        initialize:function() {
            $('#btnSave').popover({
                placement: "top",
                trigger: "hover",
                title: "提示",
                delay: {show:1000, hide:100},
                content: "保存个人信息的修改。"
            });

            $(document).ready(function() {
                $('.tip').tooltip();
            });
        },

        onJobEditClicked: function(event) {
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
                        var jobForm = $("#frmEditJob", data);
                        $('#jobFormModal').html(jobForm);
                        $('.job_start_date').datepicker({
                            format: 'yyyy-mm-dd',
                            language: 'zh-CN'
                        });
                        $('.job_end_date').datepicker({
                            format: 'yyyy-mm-dd',
                            language: 'zh-CN'
                        });
                        $("#jobFormModal").modal('show');
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

        onJobEditEnterClicked: function(){
            event.preventDefault(); // prevent navigation
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var form = $('#frmEditJob');
            $.ajax({
                type: "POST",
                url: form.attr('action'),
                data: form.serialize(), // serializes the form's elements.
                success: function(data) {
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        var jobForm = $("#frmEditJob", data);
                        $('#jobFormModal').html(jobForm);
                        var validation = $('#id_job_validation').val();
                        if (validation === "True") {
                            var url = "/information/personal/" + $('#pk').val() + "/job/list/";
                            $.ajax({
                                type: "GET",
                                url: url,
                                success: function(data){
                                    if (data.error_code > 0) {
                                        window.alert(data.error_msg);
                                    }else {
                                        $('#jobList').html(data);
                                        $('.tip').tooltip();
                                    }
                                },
                                error: function(){
                                    window.alert('与服务器通讯发生错误，请稍后重试。');
                                }
                            });
                            $("#jobFormModal").modal('hide');
                        }else {
                            $('.job_start_date').datepicker({
                                format: 'yyyy-mm-dd',
                                language: 'zh-CN'
                            });
                            $('.job_end_date').datepicker({
                                format: 'yyyy-mm-dd',
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

        onEducationEditClicked: function(event) {
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
                        var educationForm = $("#frmEditEducation", data);
                        $('#educationFormModal').html(educationForm);
                        $('.education_start_date').datepicker({
                            format: 'yyyy-mm-dd',
                            language: 'zh-CN'
                        });
                        $('.education_end_date').datepicker({
                            format: 'yyyy-mm-dd',
                            language: 'zh-CN'
                        });
                        $("#educationFormModal").modal('show');
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

        onEducationEditEnterClicked: function(){
            event.preventDefault(); // prevent navigation
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var form = $('#frmEditEducation');
            $.ajax({
                type: "POST",
                url: form.attr('action'),
                data: form.serialize(), // serializes the form's elements.
                success: function(data) {
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        var educationForm = $("#frmEditEducation", data);
                        $('#educationFormModal').html(educationForm);
                        var validation = $('#id_education_validation').val();
                        if (validation === "True") {
                            var url = "/information/personal/" + $('#pk').val() + "/education/list/";
                            $.ajax({
                                type: "GET",
                                url: url,
                                success: function(data){
                                    if (data.error_code > 0) {
                                        window.alert(data.error_msg);
                                    }else {
                                        $('#educationList').html(data);
                                        $('.tip').tooltip();
                                    }
                                },
                                error: function(){
                                    window.alert('与服务器通讯发生错误，请稍后重试。');
                                }
                            });
                            $("#educationFormModal").modal('hide');
                        }else {
                            $('.education_start_date').datepicker({
                                format: 'yyyy-mm-dd',
                                language: 'zh-CN'
                            });
                            $('.education_end_date').datepicker({
                                format: 'yyyy-mm-dd',
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
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var form = $('#frmEditInfo');
            $.ajax({
                type: "POST",
                url: form.attr('action'),
                data: form.serialize(),
                success: function(data){
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        var validation = data.validation;
                        if (validation === true) {
                            alert("编辑成功");
                            var myDate = new Date();
                            $('#id_update_datetime').val(myDate.toLocaleString());
                            //日期格式待完善
                            $('.tip').tooltip();
                        }else {
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
        remove_click:function (event) {
            // 删除确认对话框
            if (!window.confirm("警告，请确认是否要删除选中的信息？")) {
                return;
            }
            var element = $(event.target);
            var tab = "#" + element.parents('.tab-pane').attr('id');
            var name = tab.split('_');
            //console.log(name[1]);

            $(tab+' #btnDelete').addClass('disabled');

            var pks = '';
            $(tab+' .list_selector:checked').each(function (index, value) {
                pks = pks + $(value).attr('pk') + ',';
            });
            $('#id_'+name[1]+'_pks').val(pks);

            event.preventDefault(); // prevent navigation
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            var current_view = this;
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            var form = $('#frm_'+name[1]+'List');
            $.ajax({
                type: "POST",
                url: form.attr('action'),
                data: form.serialize(), // serializes the form's elements.
                success: function(data) {
                    if (data.error_code > 0) {
                        window.alert(data.error_msg);
                    }else {
                        $('#'+name[1]+'List').html(data);
                        $('#id_'+name[1]+'_pks').val('');
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
            $(tab+' #btnDelete').removeClass('disabled');
            return false; // avoid to execute the actual submit of the form.
        },

        // 选中全部
        selectAll:function (event) {
            var element = $(event.target);
            var tab = "#" + element.parents('.tab-pane').attr('id');

            $(tab+' .list_selector').prop('checked', $(tab+' #checkSelectAll').prop('checked'));
            this.toggleCommandButtonStatus(tab);
        },

        // 选择框变更状态
        selectorChanged:function (event) {
            var element = $(event.target);
            var tab = "#" + element.parents('.tab-pane').attr('id');

            this.toggleCommandButtonStatus(tab);
            $(tab+' #checkSelectAll').prop('checked', $(tab+' .list_selector').length === $(tab+' .list_selector:checked').length);
        },

        // 一览前置选择框状态变化使用
        toggleCommandButtonStatus:function (tab) {
            if ($(tab+' #btnDelete')) {
                var selectedNumToBeDeleted = $(tab+' .list_selector:checked').length;
                $(tab+' #btnDelete').prop('disabled', selectedNumToBeDeleted === 0);
                if (selectedNumToBeDeleted !== 0) {
                    $(tab+' #btnDelete').removeClass('disabled');
                } else {
                    $(tab+' #btnDelete').addClass('disabled');
                }
            }
        }

    });
});