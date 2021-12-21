$('#new_task').click(function () {
    if($('#user_role').val() == '管理员') {
        var content = ''
        var content_u = ''
        $.ajax({
            url: '/task_manage/get_data_list',
            type: 'POST',
            data: {'name': ''},
            success: function (data) {
                for (var i = 0; i < data.flist.length; i++) {
                    let x = '<div class="mdc-form-field">' +
                        '  <div class="mdc-checkbox">' +
                        '    <input type="checkbox"' +
                        '           class="mdc-checkbox__native-control us" value="' + data.flist[i] + '"/>' +
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
                        '  <label for="my-checkbox" class="na">' + data.flist[i] + '</label>' +
                        '</div>'
                    content += x
                }
                for (var i = 0; i < data.glist.length; i++) {
                    let x = '<div class="mdc-form-field">' +
                        '  <div class="mdc-checkbox">' +
                        '    <input type="checkbox"' +
                        '           class="mdc-checkbox__native-control se" value="' + data.glist[i] + '"/>' +
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
                        '  <label for="my-checkbox">' + data.glist[i] + '</label>' +
                        '</div>'
                    content_u += x
                }

                $.confirm({
                    title: '新建任务',
                    content: '<div class="mdc-layout-grid">\n' +
                    '  <div class="mdc-layout-grid__inner">\n' +
                    '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">名称</label></div>\n' +
                    '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-text-field" style="width: 100%"><input type="text" id="data_name" class="mdc-text-field__input" placeholder="请输入任务名称"></div></div>\n' +
                    '  </div><div class="mdc-layout-grid__inner">\n' +
                    '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">类型</label></div>\n' +
                    '    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-form-field"><div class="mdc-radio">' +
                    '  <input class="mdc-radio__native-control" type="radio" name="radios" checked value="按文件切分">' +
                    '  <div class="mdc-radio__background">' +
                    '    <div class="mdc-radio__outer-circle"></div>' +
                    '    <div class="mdc-radio__inner-circle"></div>' +
                    '  </div>' +
                    '</div>' +
                    '<label id="radio-1-label" for="radio-1">按文件切分</label><div class="mdc-radio">' +
                    '     <input class="mdc-radio__native-control" type="radio" name="radios" value="按句切分">' +
                    '       <div class="mdc-radio__background">' +
                    '         <div class="mdc-radio__outer-circle"></div>' +
                    '         <div class="mdc-radio__inner-circle"></div>' +
                    '        </div>' +
                    '      </div>' +
                    '        <label id="radio-1-label" for="radio-1">按句切分</label>' +
                    '</div></div></div><div class="mdc-layout-grid__inner"><div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">选择数据</div>' +
                    '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><input type="search" id="sear" class="mdc-text-field__input" oninput="sear()" placeholder="搜索"><div id="crol" style="border: 1px solid black;width: 100%;height: 100px;overflow: auto;position: relative">' +
                    content +
                    '</div></div>' +
                    '</div>' +
                    '<div class="mdc-layout-grid__inner" style="margin-top: 5px"><div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">任务分组</div>' +
                    '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div style="border: 1px solid black;width: 100%;height: 100px;overflow: auto">' + content_u + '</div></div>' +
                    '</div></div>',
                    type: 'blue',
                    // theme: 'material',
                    // backgroundDismiss: true,
                    columnClass: 'wi1',
                    buttons: {
                        ok: {
                            text: "确定（Y）",
                            btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                            keys: ['Y'],
                            action: function () {
                                var g = []
                                $('.se:checked').each(function () {
                                    g.push($(this).val())
                                });
                                var d = []
                                $('.us:checked').each(function () {
                                    d.push($(this).val())
                                });
                                var name = $('#data_name').val()
                                var ty = $('input:radio[name="radios"]:checked').val()
                                var user = $('#user_name').val()
                                if (name == '') {
                                    toastr.error('任务名称不能为空！')
                                    return false
                                } else if (d.length == 0) {
                                    toastr.error('请选择数据！')
                                    return false
                                } else if (g.length == 0) {
                                    toastr.error('请选择分组！')
                                    return false
                                } else {
                                    $.ajax({
                                        url: '/task_manage/new_task',
                                        type: 'POST',
                                        data: {
                                            'name': name,
                                            'type': ty,
                                            'user': user,
                                            'groups': g,
                                            'datas': d
                                        },
                                        success: function (data) {
                                            if (data != 'success') {
                                                toastr.error(data)
                                            }
                                            else {
                                                get_table('1', '')
                                                toastr.success('修改成功！')
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
function sear() {
    $(".na").each(function(){
        if($('#sear').val() != '') {
            if ($(this).text().indexOf($('#sear').val()) != -1) {
                $(this).parent('.mdc-form-field').css('display', '')
            }else {
                $(this).parent('.mdc-form-field').css('display', 'none')
            }
        }else {
            $(".na").each(function(){
                $(this).parent('.mdc-form-field').css('display', '')
            })
        }
    });
}
var current_page = 1
var page_count
var cond = ''

function get_table(page, cond) {
    var data = {'page': page, 'cond': cond, 'user':$('#user_name').val(), 'role':$('#user_role').val()}
    $.ajax({
        url: '/task_manage/get_tasks',
        type: 'POST',
        data: data,
        success: function (data) {
            if (data != 'no data') {
                page_count = parseInt(data.page_total)
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
                        '                        <td>' + data.files[i].first + '</td>\n' +
                        '                        <td>' + data.files[i].second + '</td>\n' +
                        '                        <td>' + data.files[i].third + '</td>\n' +
                        '                        <td style="padding-right: 1px"><button title="修改" class="mdc-button mdc-button--dense mdc-ripple-upgraded btn-table upd" data-mdc-auto-init="MDCRipple"><i class="fa fa-edit fa-lg" style="vertical-align: center;text-align: center"></i></button>' +
                        '<button title="标注" class="mdc-button mdc-button--dense mdc-ripple-upgraded btn-table bz" data-mdc-auto-init="MDCRipple"><i class="fa fa-eyedropper" style="vertical-align: center;text-align: center"></i></button>' +
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
$('#main_body').on('click', '.del', (function () {
    var name = $(this).parent().parent().children(":eq(0)").html()
    if ($('#user_role').val() == '管理员') {
        $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '选择',
            content: '是否确认删除该任务?',
            type: 'blue',
            columnClass: 'wi2',
            buttons: {
                ok: {
                    text: '是（Y）',
                    keys: ['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        $.ajax({
                            url: '/task_manage/del_task',
                            type: 'POST',
                            data: {'name': name},
                            success: function (data) {
                                get_table('1', '')
                                toastr.success('删除成功！')
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
        var content = ''
        var content_u = ''
        $.ajax({
            url: '/task_manage/get_data_list',
            type: 'POST',
            data: {'name': name},
            success: function (data) {
                if (data.disable == '0'){
                    var yy = '<div class="mdc-checkbox mdc-checkbox--disabled">'
                }else {
                    var yy = '<div class="mdc-checkbox">'
                }
                for (var i = 0; i < data.flist.length; i++) {
                    if (data.datas.includes(data.flist[i])){
                        var x = '<div class="mdc-form-field">' +
                        yy +
                        '    <input type="checkbox"' +
                        '           class="mdc-checkbox__native-control us" value="' + data.flist[i] + '" checked/>' +
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
                        '  <label for="my-checkbox">' + data.flist[i] + '</label>' +
                        '</div>'
                    }else {
                        var x = '<div class="mdc-form-field">' +
                            yy +
                            '    <input type="checkbox"' +
                            '           class="mdc-checkbox__native-control us" value="' + data.flist[i] + '"/>' +
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
                            '  <label for="my-checkbox">' + data.flist[i] + '</label>' +
                            '</div>'
                    }
                    content += x
                }
                for (var i = 0; i < data.glist.length; i++) {
                    if (data.groups.includes(data.glist[i])){
                        var x = '<div class="mdc-form-field">' +
                            '  <div class="mdc-checkbox">' +
                            '    <input type="checkbox"' +
                            '           class="mdc-checkbox__native-control se" value="' + data.glist[i] + '" checked/>' +
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
                            '  <label for="my-checkbox">' + data.glist[i] + '</label>' +
                            '</div>'
                    }else {
                        var x = '<div class="mdc-form-field">' +
                            '  <div class="mdc-checkbox">' +
                            '    <input type="checkbox"' +
                            '           class="mdc-checkbox__native-control se" value="' + data.glist[i] + '"/>' +
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
                            '  <label for="my-checkbox">' + data.glist[i] + '</label>' +
                            '</div>'
                    }
                    content_u += x
                }
                if(data.type == '按文件切分'){
                    var rdo1 = '<input class="mdc-radio__native-control" id="rdo1" type="radio" name="radios" checked value="按文件切分">'
                    var rdo2 = '<input class="mdc-radio__native-control" id="rdo2" type="radio" name="radios" value="按句切分">'
                }else {
                    var rdo1 = '<input class="mdc-radio__native-control" id="rdo1" type="radio" name="radios" value="按文件切分">'
                    var rdo2 = '<input class="mdc-radio__native-control" id="rdo2" type="radio" name="radios" checked value="按句切分">'
                }
                $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '修改任务',
            content: '<div class="mdc-layout-grid">' +
            '                      <div class="mdc-layout-grid__inner">' +
            '                        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">名称</label></div>' +
            '                        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-text-field" style="width: 100%"><input type="text" id="data_name" class="mdc-text-field__input" placeholder="请输入任务名称" value="'+name+'"></div></div>' +
            '                      </div><div class="mdc-layout-grid__inner">' +
            '                        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">类型</label></div>' +
            '                        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-form-field"><div class="mdc-radio mdc-radio--disabled ">' +
            rdo1 +
            '                      <div class="mdc-radio__background">' +
            '                        <div class="mdc-radio__outer-circle"></div>' +
            '                        <div class="mdc-radio__inner-circle"></div>' +
            '                      </div>' +
            '                    </div>' +
            '                    <label id="radio-1-label" for="radio-1">按文件切分</label><div class="mdc-radio mdc-radio--disabled">' +
            rdo2 +
            '                           <div class="mdc-radio__background">' +
            '                             <div class="mdc-radio__outer-circle"></div>' +
            '                             <div class="mdc-radio__inner-circle"></div>' +
            '                            </div>' +
            '                          </div>' +
            '                            <label id="radio-1-label" for="radio-1">按句切分</label>' +
            '                    </div></div></div><div class="mdc-layout-grid__inner"><div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">选择数据</div>' +
            '                    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div style="border: 1px solid black;width: 100%;height: 100px;overflow: auto">' +
            content +
            '                    </div></div>' +
            '                    </div>' +
            '                    <div class="mdc-layout-grid__inner" style="margin-top: 5px"><div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">任务分组</div>' +
            '                    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div style="border: 1px solid black;width: 100%;height: 100px;overflow: auto">'+content_u+'</div></div>' +
            '                    </div></div>',
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
                                var d = []
                                $('.us:checked').each(function () {
                                    d.push($(this).val())
                                });
                                var ty = $('input:radio[name="radios"]:checked').val()
                                var user = $('#user_name').val()
                                var groups = data.groups
                                var datas = data.datas
                                if ($('#data_name').val() == '') {
                                    toastr.error('任务名称不能为空！')
                                    return false
                                } else if (d.length == 0) {
                                    toastr.error('请选择数据！')
                                    return false
                                } else if (g.length == 0) {
                                    toastr.error('请选择分组！')
                                    return false
                                } else {
                                    var new_name = $('#data_name').val()
                                     $.ajax({
                                        url: '/task_manage/upd_task',
                                        type: 'POST',
                                        data: {'name': name,'new_name':new_name,'groups': groups, 'datas':datas,'gs':g,'ds':d},
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
                    keys: ['ESC'],
                    text: '取消（ESC）',
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
$('#main_body').on('click', '.bz', (function () {
    var name = $(this).parent().parent().children(":eq(0)").html()
    var count = $(this).parent().parent().children(":eq(2)").html()
     window.location.href='/annotation/'+name+'/'+count
}))