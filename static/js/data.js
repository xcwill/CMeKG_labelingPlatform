$(function() {
    toastr.options = {
        closeButton: false,
        debug: false,
        progressBar: true,
        positionClass: "toast-top-right",
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        timeOut: "1000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    };
})
$('#upload').click(function () {
    if($('#user_role').val() == '管理员') {
        $.confirm({
            title: '上传文件',
            content:
            '<div class="mdc-layout-grid">\n' +
            '  <div class="mdc-layout-grid__inner">\n' +
            '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">名称</label></div>\n' +
            '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-text-field" style="width: 100%"><input type="text" id="data_name" class="mdc-text-field__input" placeholder="请输入数据集名称"></div></div>\n' +
            '  </div><div class="mdc-layout-grid__inner">\n' +
            '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><button title="选择文件" class="mdc-button mdc-button--stroked mdc-ripple-upgraded" onclick="uplod_file()" data-mdc-auto-init="MDCRipple" style="--mdc-ripple-fg-size:10px;"><i class="material-icons mdc-button__icon">folder_open</i></button></div>\n' +
            '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><textarea id="multi-line" class="mdc-textfield__input" style="width: 100%;height: 130px" readonly="readonly"></textarea></div>\n' +
            '  </div>\n' +
            '</div>',
            type: 'blue',
            // theme: 'material',
            // backgroundDismiss: true,
            columnClass: 'wi',
            buttons: {
                ok: {
                    text: "确定（Y）",
                    keys: ['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        $('#dataname').val($('#data_name').val())
                        var formData = new FormData($('#file')[0])
                        if ($('#dataname').val() == '') {
                            toastr.warning('数据集名称不能为空！');
                            return false
                        } else {
                            $.ajax({
                                url: "/data_manage/upload",
                                type: "POST",
                                data: formData,
                                contentType: false,
                                processData: false,
                                success: function (data) {
                                    if (data == 'success') {
                                        toastr.success('上传成功！')
                                        current_page = 1
                                        cond = $('#search_file').val()
                                        get_table(current_page, cond)
                                    } else if (data == 'fail') {
                                        toastr.error('上传失败！')
                                    } else if (data == 'repeat') {
                                        toastr.warning('文件名已存在！')
                                    }
                                }
                            })
                        }


                    }
                },
                cancel: {
                    text: "取消（ESC）",
                    keys: ['ESC'],
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    action: function () {
                        $('#multi-line').val('')
                        $('#data_name').val('')
                    }
                }
            }

        });
    }else{
        toastr.error('没有权限！')
    }
})
function uplod_file() {
    $('#fi').trigger('click')
}
function file_change() {

    //toastr.success($(this).val()+' 上传成功！')
    var files = $('#fi')[0].files
    for (var i = 0; i < files.length; i++) {
        $('#multi-line').append(i + 1 + '. ' + files[i].name + '\n')
    }
}
var current_page = 1
var page_count
var cond = ''



function get_table(page, cond) {
    // alert(page)
    var data = {'page': page, 'cond': cond}
    $.ajax({
        url: '/data_manage/get_files',
        type: 'POST',
        data: data,
        success: function (data) {
            if (data != 'no data') {
                page_count = parseInt(data.page_total)
                console.log(data)
                $('#result').html('显示第' + data.page_start + '条' + '到' + data.page_end + '条记录，共' + data.data_length + '条记录；当前第' + page + '页，共' + page_count + '页')
                $('#main_body').html('')
                for (var i = 0; i < data.files.length; i++) {
                    $('#main_body').append('<tr>\n' +
                        '                        <td class="text-left">' + data.files[i].name + '</td>\n' +
                        '                        <td>' + data.files[i].type + '</td>\n' +
                        '                        <td>' + data.files[i].count + '</td>\n' +
                        '                        <td>' + data.files[i].time + '</td>\n' +
                        '                        <td>' + data.files[i].user + '</td>\n' +
                        '                        <td>' + data.files[i].words + '</td>\n' +
                        '                        <td style="padding-right: 1px"><button title="重命名" class="mdc-button mdc-button--dense mdc-ripple-upgraded btn-table upd" data-mdc-auto-init="MDCRipple" style="padding-top: 1px"><i class="fa fa-edit fa-lg" style="vertical-align: center;text-align: center"></i></button>' +
                        '<button title="删除" class="mdc-button mdc-button--dense mdc-ripple-upgraded btn-table del" data-mdc-auto-init="MDCRipple"><i class="fa fa-trash-o fa-lg" style="vertical-align: center;text-align: center"></i></button></td>\n' +
                        '                      </tr>')
                }
                $('.pagination').html('')
                if (parseInt(page) == 1) {
                    $('.pagination').append('<li title="首页" class="first page-disabled le"><a class="first page-disabled">&laquo;</a></li>\n' +
                        '<li title="上一页" class="page-disabled"><a class="previous page-disabled">&lsaquo;</a></li>')
                } else {
                    $('.pagination').append('<li title="首页" class="first le"><a class="first" href="#">&laquo;</a></li>\n' +
                        '<li title="上一页"><a class="previous" href="#">&lsaquo;</a></li>')
                }
                if (parseInt(data.page_total) <= 5) {
                    for (var i = 1; i < parseInt(data.page_total) + 1; i++) {
                        if (i == parseInt(page)) {
                            $('.pagination').append('<li title="第' + i + '页" class="page-active"><a class="page-active page" href="#">' + i + '</a></li>')
                        } else {
                            $('.pagination').append('<li title="第' + i + '页"><a class="page" href="#">' + i + '</a></li>')
                        }

                    }
                } else {
                    if (parseInt(page) <= 3) {
                        for (var i = 1; i < 6; i++) {
                            if (i == parseInt(page)) {
                                $('.pagination').append('<li title="第' + i + '页" class="page-active"><a class="page-active page" href="#">' + i + '</a></li>')
                            } else {
                                $('.pagination').append('<li title="第' + i + '页"><a class="page" href="#">' + i + '</a></li>')
                            }

                        }
                    } else if (parseInt(page) > 3 && (parseInt(page) + 2) <= parseInt(data.page_total)) {
                        $('.pagination').append('<li title="第' + (parseInt(page) - 2) + '页"><a class="page" href="#">' + (parseInt(page) - 2) + '</a></li>')
                        $('.pagination').append('<li title="第' + (parseInt(page) - 1) + '页"><a class="page" href="#">' + (parseInt(page) - 1) + '</a></li>')
                        $('.pagination').append('<li class="page-active" title="第' + parseInt(page) + '页"><a class="page page-active" href="#">' + parseInt(page) + '</a></li>')
                        $('.pagination').append('<li title="第' + (parseInt(page) + 1) + '页"><a class="page" href="#">' + (parseInt(page) + 1) + '</a></li>')
                        $('.pagination').append('<li title="第' + (parseInt(page) + 2) + '页"><a class="page" href="#">' + (parseInt(page) + 2) + '</a></li>')

                    } else {
                        for (var i = parseInt(data.page_total) - 4; i < parseInt(data.page_total) + 1; i++) {
                            if (i == parseInt(page)) {
                                $('.pagination').append('<li title="第' + i + '页" class="page-active"><a class="page-active page" href="#">' + i + '</a></li>')
                            } else {
                                $('.pagination').append('<li title="第' + i + '页"><a class="page" href="#">' + i + '</a></li>')
                            }

                        }
                    }

                }
                if (parseInt(page) == parseInt(data.page_total)) {
                    $('.pagination').append('<li title="下一页" class="page-disabled"><a class="page-disabled">&rsaquo;</a></li>\n' +
                        '<li title="末页" class="last page-disabled"><a class="page-disabled">&raquo;</a></li>')
                } else {
                    $('.pagination').append('<li title="下一页"><a class="next" href="#">&rsaquo;</a></li>\n' +
                        '<li title="末页" class="last"><a class="last" href="#">&raquo;</a></li>')
                }
            }else{
                $('#main_body').html('')
                $('.pagination').html('')
                $('#result').html('空空如也!')

            }
        }
    })
}
$('.pagination').on('click','.page',(function (){
    current_page = $(this).text()
    cond = $('#search_file').val()
    get_table(current_page, cond)
}))
$('.pagination').on('click','.previous',(function (){
    if(current_page > 1){
        current_page = parseInt(current_page) - 1
        cond = $('#search_file').val()
        get_table(current_page, cond)
    }
}))
$('.pagination').on('click','.next',(function () {
    if (current_page < page_count) {
        current_page = parseInt(current_page) + 1
        cond = $('#search_file').val()
        get_table(current_page, cond)
    }
}))
$('.pagination').on('click','.first',(function () {
    current_page = 1
    cond = $('#search_file').val()
    get_table(current_page, cond)
}))
$('.pagination').on('click','.last',(function () {
    current_page = page_count
    cond = $('#search_file').val()
    get_table(current_page, cond)
}))
function search_input() {
    cond = $('#search_file').val()
    get_table('1', cond)
}
$('#main_body').on('click', '.del', (function () {
    var name = $(this).parent().parent().children(":eq(0)").html()
    if ($('#user_role').val() == '管理员') {
        $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '选择',
            content: '是否确认删除该数据?',
            type: 'blue',
            columnClass: 'wi2',
            buttons: {
                ok: {
                    text: '是（Y）',
                    keys: ['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        $.ajax({
                            url: '/data_manage/del_data',
                            type: 'POST',
                            data: {'name': name},
                            success: function (data) {
                                if (data=='success'){
                                   get_table('1', '')
                                toastr.success('删除成功！')
                                }else{
                                    toastr.error('删除失败！（该数据有任务正在使用中！）')
                                }

                            }
                        })
                    }
                },
                cancel: {
                    text: '否（N）',
                    keys: ['N'],
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    action: function () {

                    }
                }
            }
        });
    }else{
        toastr.error('没有权限！')
    }
}))
$('#main_body').on('click', '.upd', (function () {
    var name = $(this).parent().parent().children(":eq(0)").html()
    if ($('#user_role').val() == '管理员') {
        $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '重命名',
            content: '<br/><div align="center" style="width: 90%;padding-left: 5%"><div class="mdc-text-field" style="width: 100%"><input type="text" id="new_name" class="mdc-text-field__input" value="'+name+'"></div></div>\n' +
                    '  </div></div>',
            type: 'blue',
            columnClass: 'wi2',
            buttons: {
                ok: {
                    text: '是（Y）',
                    keys: ['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        var new_name = $('#new_name').val()
                        if (name != new_name){
                            $.ajax({
                            url: '/data_manage/new_name',
                            type: 'POST',
                            data: {'name': name, 'new_name': new_name},
                            success: function (data) {
                                if (data=='success'){
                                   get_table('1', '')
                                toastr.success('修改成功！')
                                }else{
                                    toastr.error('修改失败！')
                                }

                            }
                        })
                        }else {
                            toastr.warning('无修改！')
                        }
                    }
                },
                cancel: {
                    text: '否（ESC）',
                    keys: ['ESC'],
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    action: function () {

                    }
                }
            }
        });
    }else{
        toastr.error('没有权限！')
    }
}))