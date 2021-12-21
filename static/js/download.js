function gen_groups(){
    $.ajax({
        url: '/download_manage/get_groups',
        type: 'POST',
        success: function (data) {
            for(var i=0;i<data.groups.length;i++){
                $('.group').append('<option>' +data.groups[i]+ '</option>')
            }
        }
    })
}
$('.reset').click(function () {
    window.location.href = '/download'
})
$('.dc').click(function () {
    if($('#user_role').val()  == '管理员'){
    if($('#result').html() == '空空如也!'){
        toastr.error('未检索到数据！！请重新选择查询条件！！！')
    }else{
        window.open('/download_manage/download/zip/数据导出/数据导出.zip')
    }
    }else{
        toastr.error('没有权限！')
    }
})
var current_page = 1
var page_count
var cond = ''
var file_path = ''
var group = ''

function search_input() {
    cond = $('#search_file').val()
    get_table('1', cond, file_path, group)
}
$('.file_path').change(function () {
    file_path = $(this).val()
    get_table('1', cond, file_path, group)
})
$('.group').change(function () {
    group = $(this).val()
    get_table('1', cond, file_path, group)
})
function get_table(page, cond, file_path, group) {
    var data = {'page': page, 'cond': cond, 'file_path': file_path, 'group': group}
    $.ajax({
        url: '/download_manage/get_data',
        type: 'POST',
        data: data,
        success: function (data) {
            if (data != 'no data') {
                page_count = parseInt(data.page_total)
                console.log(data)
                $('#result').html('显示第' + data.page_start + '条' + '到' + data.page_end + '条记录，共' + data.data_length + '条记录；当前第' + page + '页，共' + page_count + '页')
                $('#ccad').html('查询完成!')
                $('#main_body').html('')
                for (var i = 0; i < data.files.length; i++) {
                    $('#main_body').append('<tr>\n' +
                        '                        <td class="text-left">' + data.files[i] + '</td>\n' +
                        '                        <td style="padding-right: 1px;padding-right: 2%"><button title="下载" class="mdc-button mdc-button--dense mdc-ripple-upgraded btn-table dow" data-mdc-auto-init="MDCRipple" style="padding-top: 1px"><i class="fa fa-download fa-lg" style="vertical-align: center;text-align: center"></i></button>' +
                        '</td>' +
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
    get_table(current_page, cond, file_path, group)
}))
$('.pagination').on('click','.previous',(function (){
    if(current_page > 1){
        current_page = parseInt(current_page) - 1
        cond = $('#search_file').val()
        get_table(current_page, cond, file_path, group)
    }
}))
$('.pagination').on('click','.next',(function () {
    if (current_page < page_count) {
        current_page = parseInt(current_page) + 1
        cond = $('#search_file').val()
        get_table(current_page, cond, file_path, group)
    }
}))
$('.pagination').on('click','.first',(function () {
    current_page = 1
    cond = $('#search_file').val()
    get_table(current_page, cond, file_path, group)
}))
$('.pagination').on('click','.last',(function () {
    current_page = page_count
    cond = $('#search_file').val()
    get_table(current_page, cond, file_path, group)
}))
$('#main_body').on('click', '.dow', (function () {
    var name = $(this).parent().parent().children(":eq(0)").html()
    if($('#user_role').val()  == '管理员') {
        window.open('/download_manage/download/' + 'zip/' + name + '/' + name + '_' + file_path + '.zip')
    }else {
        toastr.error('没有权限！')
    }
}))