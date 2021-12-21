var current_page = 1
var page_count
var cond = ''

function get_table(page, cond) {
    var data = {'page': page, 'cond': cond}
    $.ajax({
        url: '/group_manage/get_groups',
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
                        '                        <td class="text-left">' + data.files[i] + '</td>\n' +
                        '                        <td style="padding-right: 1px"><button title="修改" class="mdc-button mdc-button--dense mdc-ripple-upgraded btn-table upd" data-mdc-auto-init="MDCRipple" style="padding-top: 1px"><i class="fa fa-edit fa-lg" style="vertical-align: center;text-align: center"></i></button>' +
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
function search_input() {
    cond = $('#search_file').val()
    get_table('1', cond)
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
$('#new_group').click(function () {
    if($('#user_role').val() == '管理员') {
        var content = ''
        $.ajax({
            url: '/group_manage/get_data_list',
            type: 'POST',
            data: {'name': ''},
            success: function (data) {
                for (var i = 0; i < data.ulist.length; i++) {
                    let x = '<div class="mdc-form-field">' +
                        '  <div class="mdc-checkbox">' +
                        '    <input type="checkbox"' +
                        '           class="mdc-checkbox__native-control us" value="' + data.ulist[i] + '"/>' +
                        '    <div class="mdc-checkbox__background">' +
                        '      <svg class="mdc-checkbox__checkmark"' +
                        '           viewBox="0 0 24 24">' +
                        '        <path class="mdc-checkbox__checkmark__path"' +
                        '              fill="none"' +
                        '              stroke="white"' +
                        '              d="M1.73,12.91 8.1,19.28 22.79,4.59"/>' +
                        '      </svg>' +
                        '      <div class="mdc-checkbox__mixedmark"></div>' +
                        '    </div>' +
                        '  </div>' +
                        '' +
                        '  <label for="my-checkbox">' + data.ulist[i] + '</label>' +
                        '</div>'
                    content += x
                }
                $.confirm({
                    title: '新建分组',
                    content: '<div class="mdc-layout-grid">\n' +
                    '  <div class="mdc-layout-grid__inner">\n' +
                    '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">名称</label></div>\n' +
                    '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-text-field" style="width: 100%"><input type="text" id="data_name" class="mdc-text-field__input" placeholder="请输入分组名称"></div></div>\n' +
                    '  </div>'+
                    '<div class="mdc-layout-grid__inner"><div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">选择用户</div>' +
                    '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div style="border: 1px solid black;width: 100%;height: 100px;overflow: auto">' +
                    content +
                    '</div></div>' +
                    '</div>' +
                    '</div>',
                    type: 'blue',
                    // theme: 'material',
                    // backgroundDismiss: true,
                    columnClass: 'wi1',
                    buttons: {
                        ok: {
                            text: "确定（Y)",
                            btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                            keys: ['Y'],
                            action: function () {
                                var d = []
                                $('.us:checked').each(function () {
                                    d.push($(this).val())
                                });
                                var name = $('#data_name').val()
                                if (name == '') {
                                    toastr.error('任务名称不能为空！')
                                    return false
                                } else if (d.length == 0) {
                                    toastr.error('请选择用户！')
                                    return false
                                }  else {
                                    $.ajax({
                                        url: '/group_manage/new_group',
                                        type: 'POST',
                                        data: {
                                            'name': name,
                                            'users': d
                                        },
                                        success: function (data) {
                                            if (data != 'success') {
                                                toastr.error(data)
                                            }
                                            else {
                                                get_table('1', '')
                                                toastr.success('创建成功！')
                                            }
                                        }
                                    })
                                }

                            }
                        },
                        cancel: {
                            text: "取消（N）",
                            btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                            keys: ['N'],
                            action: function () {
                            }
                        }
                    }
                })
            }
        })
    }else {
        toastr.error('没有权限！')
    }
})
$('#main_body').on('click', '.upd', (function () {
    var name = $(this).parent().parent().children(":eq(0)").html()
    if ($('#user_role').val() == '管理员') {
        var content = ''
        var content_u = ''
        $.ajax({
            url: '/group_manage/get_data_list',
            type: 'POST',
            data: {'name': name},
            success: function (data) {
                for (var i = 0; i < data.ulist.length; i++) {
                    if (data.users.includes(data.ulist[i])){
                        var x = '<div class="mdc-form-field">' +
                            '  <div class="mdc-checkbox">' +
                            '    <input type="checkbox"' +
                            '           class="mdc-checkbox__native-control se" value="' + data.ulist[i] + '" checked/>' +
                            '    <div class="mdc-checkbox__background">' +
                            '      <svg class="mdc-checkbox__checkmark"' +
                            '           viewBox="0 0 24 24">' +
                            '        <path class="mdc-checkbox__checkmark__path"' +
                            '              fill="none"' +
                            '              stroke="white"' +
                            '              d="M1.73,12.91 8.1,19.28 22.79,4.59"/>' +
                            '      </svg>' +
                            '      <div class="mdc-checkbox__mixedmark"></div>' +
                            '    </div>' +
                            '  </div>' +
                            '' +
                            '  <label for="my-checkbox">' + data.ulist[i] + '</label>' +
                            '</div>'
                    }else {
                        var x = '<div class="mdc-form-field">' +
                            '  <div class="mdc-checkbox">' +
                            '    <input type="checkbox"' +
                            '           class="mdc-checkbox__native-control se" value="' + data.ulist[i] + '"/>' +
                            '    <div class="mdc-checkbox__background">' +
                            '      <svg class="mdc-checkbox__checkmark"' +
                            '           viewBox="0 0 24 24">' +
                            '        <path class="mdc-checkbox__checkmark__path"' +
                            '              fill="none"' +
                            '              stroke="white"' +
                            '              d="M1.73,12.91 8.1,19.28 22.79,4.59"/>' +
                            '      </svg>' +
                            '      <div class="mdc-checkbox__mixedmark"></div>' +
                            '    </div>' +
                            '  </div>' +
                            '' +
                            '  <label for="my-checkbox">' + data.ulist[i] + '</label>' +
                            '</div>'
                    }
                    content += x
                }
                $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '修改分组',
            content: '<div class="mdc-layout-grid">' +
            '                      <div class="mdc-layout-grid__inner">' +
            '                        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">名称</label></div>' +
            '                        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-text-field" style="width: 100%"><input type="text" id="data_name" class="mdc-text-field__input" value="'+name+'"></div></div>' +
            '                      </div>'+
            '                    <div class="mdc-layout-grid__inner"><div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">选择用户</div>' +
            '                    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div style="border: 1px solid black;width: 100%;height: 100px;overflow: auto">' +
            content +
            '                    </div></div>' +
            '                    </div>' +
            '                    </div>',
            type: 'blue',
            columnClass: 'wi1',
            buttons: {
                ok: {
                    keys: ['Y'],
                    text: '确认（Y）',
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                                var g = []
                                $('.se:checked').each(function () {
                                    g.push($(this).val())
                                });
                                var users = data.users
                                if ($('#data_name').val() == '') {
                                    toastr.error('分组名称不能为空！')
                                    return false
                                }else if (g.length == 0) {
                                    toastr.error('请选择用户！')
                                    return false
                                } else {
                                    var new_name = $('#data_name').val()
                                     $.ajax({
                                        url: '/group_manage/upd_group',
                                        type: 'POST',
                                        data: {'name': name,'new_name':new_name,'users': users, 'us':g},
                                        success: function (data) {
                                            if (data == '修改成功！'){
                                                get_table('1', '')
                                            }
                                            toastr.success(data)
                                        }})
                                }
                    }
                },
                cancel: {
                    keys: ['N'],
                    text: '取消（N）',
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    action: function () {

                    }
                }
            }
        });

            }
            })
    }else{
        toastr.error('没有权限！')
    }
}))
$('#main_body').on('click', '.del', (function () {
    var name = $(this).parent().parent().children(":eq(0)").html()
    if ($('#user_role').val() == '管理员') {
        $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '选择',
            content: '是否确认删除该分组?',
            type: 'blue',
            columnClass: 'wi2',
            buttons: {
                ok: {
                    text: '是（Y）',
                    keys: ['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        $.ajax({
                            url: '/group_manage/del_group',
                            type: 'POST',
                            data: {'name': name},
                            success: function (data) {
                                if (data=='success'){
                                   get_table('1', '')
                                toastr.success('删除成功！')
                                }else{
                                    toastr.error('删除失败！（该分组有任务正在进行中！）')
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