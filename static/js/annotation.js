$('#config').click(function () {
    var username = $('#user_name').val()
     $.ajax({
         url: '/annotation/get_labels',
         type: 'POST',
         success: function (data) {
             console.log(data)
             var ens = ''
             for(var i=0;i<data.ens.length;i++){
                 ens += data.ens[i] + '\n'
             }
             var res = ''
             if(data.res.length != 0){
                 for(var i=0;i<data.res.length;i++){
                     res += data.res[i].rel_type + ' ' + data.res[i].e1_label + ' ' + data.res[i].e2_label + '\n'
                 }
             }
            $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '标签配置',
            content: '<div class="mdc-layout-grid">' +
            '              <div class="mdc-layout-grid__inner">' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">实体配置</label></div>' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-text-field" style="width: 100%"><select class="en_config">\n' +
            '                                                    <option>'+ username + '_en.txt</option>\n' +
            '                                                 </select></div></div>' +
            '              </div><div class="mdc-layout-grid__inner">' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><button title="选择文件" class="mdc-button mdc-button--stroked mdc-ripple-upgraded" onclick="uplod_file()" data-mdc-auto-init="MDCRipple" style="--mdc-ripple-fg-size:10px;"><i class="material-icons mdc-button__icon">folder_open</i></button></div>' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><textarea id="enconfig" class="mdc-textfield__input" style="width: 100%;height: 80px">'+ens+'</textarea></div>' +
            '              </div>'+
             '              <div class="mdc-layout-grid__inner">' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><label class="mdc-textfield__label" for="my-textfield" style="">关系配置</label></div>' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><div class="mdc-text-field" style="width: 100%"><select class="en_config">\n' +
            '                                                    <option>'+ username + '_re.json</option>\n' +
            '                                                 </select></div></div>' +
            '              </div><div class="mdc-layout-grid__inner">' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3"><button title="选择文件" class="mdc-button mdc-button--stroked mdc-ripple-upgraded" onclick="uplod_file()" data-mdc-auto-init="MDCRipple" style="--mdc-ripple-fg-size:10px;"><i class="material-icons mdc-button__icon">folder_open</i></button></div>' +
            '                <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7"><textarea id="reconfig" class="mdc-textfield__input" style="width: 100%;height: 80px">'+res+'</textarea></div>' +
            '              </div>'+
            '            </div>',
            type: 'blue',
            columnClass: 'wi',
            buttons: {
                ok: {
                    text: '是(ENTER)',
                    keys: ['ENTER'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        var ens_new = $('#enconfig').val()
                        var res_new = $('#reconfig').val()
                        if(ens_new == ''){
                            toastr.error('实体项不能为空！')
                            return false
                        }else if(res_new == ''){
                            toastr.error('关系项不能为空！')
                            return false
                        }else{
                             $.ajax({
                                 url: '/annotation/labels_config',
                                 type: 'POST',
                                 data: {'ens': ens_new, 'res': res_new},
                                 success: function (data) {
                                    if(data == 'success'){
                                        location.reload()
                                        toastr.success('配置成功！')
                                    }else{
                                        toastr.error('配置失败！')
                                    }
                                 }
                             })
                        }
                    }
                },
                cancel: {
                    text: '否(ESC)',
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    keys: ['ESC'],
                    action: function () {

                    }
                }
                }
            })
         }
     })

})
flag = false
$('#zk').click(function () {
    if (flag) {
        $('#tool').css('display', 'none')
        $('#main').removeClass('mdc-layout-grid__cell--span-8')
        $('#main').addClass('mdc-layout-grid__cell--span-10')
        flag = false
    }else {
        $('#tool').css('display', '')
        $('#main').removeClass('mdc-layout-grid__cell--span-10')
        $('#main').addClass('mdc-layout-grid__cell--span-8')
        flag = true
    }
})
flag1 = true
$('#basic-switch').click(function () {
    if(flag1){
        $('.entitys').css('display','none')
        $('.relations').css('display','')
        $('.entity').removeClass('mdc-button--raised')
        entity = ''
        flag1 = false
    }else {
        $('.entitys').css('display','')
        $('.relations').css('display','none')
        $('.relation').each(function () {
        $(this).val('')
        label = ''
    })
        flag1 = true
    }
})
var prop_flag = false
$('#basic-switch2').click(function () {
    if(!prop_flag){
        prop_flag = true
    }else{
        prop_flag = false
    }
})
 function Collapse(className,close_prev,default_open){
        this._elements = [];
        this._className = String(className);
        this._previous = Boolean(close_prev)
        this._default = typeof(default_open)==="number" ? default_open: -1
        this.getCurrent
        this.init();
    }

    //收集所有折叠菜单的div
    Collapse.prototype.collectElementbyClass = function(){
        this._elements = [];
        var allelements = document.getElementsByTagName("div");

        for(var i=0;i<allelements.length;i++){
            var collapse_div = allelements[i];
            if (typeof collapse_div.className === "string" && collapse_div.className === this._className){

                var h3s = collapse_div.getElementsByTagName("h3");
                var collapse_body = collapse_div.getElementsByClassName("collapse_body");
                if(h3s.length === 1 && collapse_body.length === 1){
                    h3s[0].style.cursor = "pointer";

                    if(this._default === this._elements.length){
                        collapse_body[0].style.visibility = "visible";
                      collapse_body[0].style.height = ($('#coll')[0].scrollHeight)*0.682+"px"
                    }else{
                        collapse_body[0].style.height = "0px";
                      collapse_body[0].style.visibility = "hidden";
                    }
                    this._elements[this._elements.length] = collapse_div;
                }
            }
        }
    }
    Collapse.prototype.open = function(elm){
        elm.style.visibility = "visible";
        elm.style.height = ($('#coll')[0].scrollHeight)*0.682 + "px"

    }
    Collapse.prototype.close = function(elm){
      elm.style.height = "0px";
      elm.style.visibility = "hidden";
    }
    Collapse.prototype.isOpen = function(elm){

      return elm.style.visibility === "visible"
    }

    Collapse.prototype.getCurrent = function(header){
        var cur ;
        if(window.addEventListener){
            cur = header.parentNode
        }else{
            cur = header.parentElement
        }
        return cur.getElementsByClassName("collapse_body")[0]
        }

    Collapse.prototype.toggleDisplay = function(header){

        var cur = this.getCurrent(header)
        //console.log(cur)
        if(this.isOpen(cur)){
            this.close(cur);
        }else{
            this.open(cur);
        }
        if(this._previous){
            for(var i=0;i<this._elements.length;i++){
                if(this._elements[i] !== (cur.parentNode||cur.parentElement)){
                    var collapse_body = this._elements[i].getElementsByClassName("collapse_body");
                    collapse_body[0].style.height = "0px";
                    collapse_body[0].style.visibility = "hidden";

                }
            }
        }
    }

    Collapse.prototype.init = function(){
        var instance = this;
        this.collectElementbyClass();
        if(this._elements.length === 0){
            return;
        }

        for(var i=0;i<this._elements.length;i++){
            var h3s = this._elements[i].getElementsByTagName("h3");
            if(window.addEventListener){
                h3s[0].addEventListener("click",function(){ instance.toggleDisplay(this);},false);
            }else{
                h3s[0].onclick = function(){instance.toggleDisplay(this);}
            }
        }
    }

//传参
 var myCollapse = new Collapse("collapseDiv",true);
var entity = ''
var color = ''
var label = ''
var re_start = ''
var re_end = ''
var source = ''
var target = ''
var conn = null
var property = ''         //属性端点
var en1_property = ''
var en2_property = ''
var property_count = 0    //属性计数
var connects = []
var stub = 30
var has_property = false
var en1_has_prop = false
var en2_has_prop = false
$('.entity').click(function () {
    $('.entity').removeClass('mdc-button--raised')
    $(this).addClass('mdc-button--raised')
    entity = $(this).text()
    color = $(this).attr('data-color')
})
$('#relations').on('change','.relation',(function () {
    label = $(this).val().trim()
    re_start = $(this).attr('data-start')
    re_end = $(this).attr('data-end')
    rel_type = $(this).val().trim()
    val = $(this).val()

    $('.relation').each(function () {
        $(this).val('')
    })
    $(this).val(val)
}))
var relations = []
$("#content-area").mouseup(function (e) {
    if (e.button == 0){
        if(e.target.id == 'content-area') {
            text = window.getSelection().toString()
            if (text != '' && text != '\n' && text != ' ') {
                // var start = window.getSelection().anchorOffset+getoffset()
                // var end = window.getSelection().focusOffset+getoffset()
                start = window.getSelection().anchorOffset + getoffset()
                end = window.getSelection().focusOffset + getoffset()
                if (start > end) {
                    t = start
                    start = end
                    end = start + text.length
                }
                var txt = $('#content').html().toString().substring(start, end)
                console.log(txt)
                if(txt == text){
                    add_entity()
                }else{
                    console.log('111')
                    console.log(txt)
                    end = start + text.length
                    add_entity()
                }
            }
        }else if(e.target.id.split('_')[0] != 'jsPlumb') {
            $('.tag-txt').removeClass('bor')
            if ($(e.target)[0].tagName == 'B') {
                $(e.target).addClass('bor')
            }
            if(!flag1){
                if(label != ''){
                    if ($(e.target)[0].tagName == 'B') {
                        if (source == '') {
                           if (re_check_start(e.target.id)) {
                              source = e.target.id
                           }
                        }else{
                            if (re_check_end(e.target.id)) {
                                        if (e.target.id != source) {
                                            target = e.target.id
                                            if(is_re(source)){
                                                stub -= 13 * get_re_count(source)
                                                connect(source, target, label, 'property' + property_count, stub)
                                                // re_connect(source, target, 'property' + property_count, label, stub)
                                                stub = 70
                                            }else {
                                                stub = 70
                                                connect(source, target, label, 'property' + property_count, stub)
                                                // re_connect(source, target, 'property' + property_count, label, stub)
                                            }
                                            if (prop_flag) {
                                                add_en1_prop()
                                            }else{
                                                property = ''
                                                en1_property = ''
                                                en2_property = ''
                                                has_property = false
                                                en1_has_prop = false
                                                en2_has_prop = false
                                                get_relations(source, target, property, en1_property, en2_property)
                                                get_conns(conn,source,target)
                                                if (en1_property == ''){
                                                    var eee1 = '实体1没有属性!'
                                                }
                                                if (en2_property == ''){
                                                    var eee2 = '实体2没有属性!'
                                                }
                                                var new_prop = '<span id="property'+property_count+'" data-source="'+source+'" data-target="'+target+'" data-en1-prop="'+eee1+'" data-en2-prop="'+eee2+'">该关系没有属性！</span>'
                                                $('#re_props').append(new_prop)
                                                property_count += 1
                                                toastr.success('继续下个标注！')
                                                source = ''
                                                target = ''
                                            }
                                            // add_property(source, target)
                                        } else {
                                            toastr.error('实体不能和自身建立关系！')
                                        }
                                    }
                        }
                    }
                }else{
                    toastr.error('请选择关系项！')
                }
            }
        }

    }else if(e.button == 2){
        if (e.target.id == 'content-area') {
        }else if(e.target.id.split('_')[0] != 'jsPlumb'){
                        if(flag1) {
                            if(is_re(e.target.id)) {
                                //$(e.target).replaceWith($(e.target).text())
                                //jsPlumb.remove(e.target.id)
                                jsPlumb.deleteConnectionsForElement(e.target)
                                $(e.target).replaceWith($(e.target).text())
                                del_relation(e.target.id)
                               // alert(e.target.id)
                                del_conns_by_one_id(e.target.id)
                            }else {
                                $(e.target).replaceWith($(e.target).text())
                            }
                        }else {
                            if(is_re(e.target.id)) {
                                jsPlumb.deleteConnectionsForElement(e.target)
                                del_relation(e.target.id)
                                del_conns_by_one_id(e.target.id)
                            }
                        }
                    }
    }
})
    function re_check_start(sel_id){
        if($('#'+sel_id).attr('data-entity') == re_start){
            return true
        }else if(re_start == 'x') {
            return true
        }else {
            toastr.error('该关系开始标签应为'+re_start+'！')
            return false
        }
    }
function re_check_end(sel_id){
    if($('#'+sel_id).attr('data-entity') == re_end){
        return true
    }else if(re_end == 'x') {
        return true
    }else{
        toastr.error('该关系结束标签应为'+re_end+'！')
        return false
    }}
function getoffset() {
    var container = window.getSelection().getRangeAt(0).startContainer

    var offset = 0

    while(container.previousSibling){
        offset += container.previousSibling.textContent.length
        container = container.previousSibling
    }
    return offset
}

function add_entity() {
     if (entity != '') {
                selectedText = "<b class='tag-txt "+color+"' data-entity='" + entity + "' id='" + start + "' data-start='" + start + "' data-end='" + end + "' style=''>" + text + "</b>";
                let top = $('#content-area').scrollTop()
                let model = selectedText
                document.execCommand("insertHTML", true, model)
                $('#content-area').scrollTop(top)
                $('.tag-txt').css('font-family', '')
            }else if(en1_has_prop){
                en1_property = window.getSelection().toString()
                en1_has_prop = false
                add_en2_prop()
            }
            else if(en2_has_prop){
                en2_property = window.getSelection().toString()
                en2_has_prop = false
                add_property(source, target)
            }
            else if(has_property){
                        property = window.getSelection().toString()

                        get_relations(source,target,property, en1_property, en2_property)
                        get_conns(conn,source,target)
                        has_property = false
                        var new_prop = '<span id="property'+property_count+'" data-source="'+source+'" data-target="'+target+'" data-en1-prop="'+en1_property+'" data-en2-prop="'+en2_property+'">'+property+'</span>'
                        $('#re_props').append(new_prop)
                        property_count += 1
                        toastr.success('属性标注完成！')
                        source = ''
                        target = ''
                        property = ''
                        // alert(JSON.stringify(relations))
                    }
            else{
                if(flag1) {
                    toastr.warning('请先选择实体项!')
                }
            }
}
function get_relations(sourceID, targetID, rel_property, en1_p, en2_p) {
            var relation = {}
            relation.rel_type =  label

            var span_front = {}
            span_front.span_name = $('#'+sourceID).text()
            span_front.label = $('#'+sourceID).attr('data-entity')
            span_front.start_offset = $('#'+sourceID).attr('data-start')
            span_front.end_offset = $('#'+sourceID).attr('data-end')
            span_front.en_property = en1_p

            relation.span_front = span_front

            var span_after = {}
            span_after.span_name = $('#'+targetID).text()
            span_after.label = $('#'+targetID).attr('data-entity')
            span_after.start_offset = $('#'+targetID).attr('data-start')
            span_after.end_offset = $('#'+targetID).attr('data-end')
            span_after.en_property = en2_p

            relation.span_after =span_after
            relation.rel_property = rel_property

            relations.push(relation)

            // alert(JSON.stringify(relations))

     }
     //判断该实体是否存在关系
    function is_re(el_id) {
        for(var i=0;i<relations.length;i++){
            if(el_id == relations[i].span_front.start_offset || el_id == relations[i].span_front.end_offset || el_id == relations[i].span_after.start_offset || el_id == relations[i].span_after.end_offset){
                return true
            }
        }
        return false

    }
    function get_re_count(el_id) {
        var re_count = 0
        for(var i=0;i<relations.length;i++){
            if(el_id == relations[i].span_front.start_offset || el_id == relations[i].span_front.end_offset || el_id == relations[i].span_after.start_offset || el_id == relations[i].span_after.end_offset){
                re_count += 1
            }
        }
        return re_count
    }
    //关系删除函数(根据一个id)
    function del_relation(del_ID) {
        var del_span = {}
        del_span.span_name = $('#'+del_ID).text()
        del_span.label = $('#'+del_ID).attr('data-entity')
        del_span.start_offset = $('#'+del_ID).attr('data-start')
        del_span.end_offset = $('#'+del_ID).attr('data-end')
        for(var i=0;i<relations.length;i++){
            if(com_re(del_span,relations[i].span_front)){
                relations.splice(i,1);
            }else if(com_re(del_span,relations[i].span_after)){
                relations.splice(i,1);
            }
        }
        //alert(JSON.stringify(relations))
    }
    //对象比较函数
    function com_re(del_span,span) {
        if(del_span.span_name == span.span_name && del_span.label == span.label && del_span.start_offset == span.start_offset && del_span.end_offset == span.end_offset){
            return true
        }else {
            return false
        }
    }
    //缓存连接函数
    function get_conns(con,sou,ta) {

        var cons = {}
        cons.connect = con
        cons.start = sou
        cons.end = ta


        connects.push(cons)

        conn = null
    }
    //删除连接根据一个id
    function del_conns_by_one_id(del_id) {
        for(var i=0;i<connects.length;i++){
            if(del_id == connects[i].start || del_id == connects[i].end){
                connects.splice(i,1);
            }
        }
    }
    //删除关系根据两个id
     function del_relation_by_two_id(source_id,target_id) {
        // alert(JSON.stringify(relations))
        //  alert(source_id+'  '+target_id)
        for(var i=0;i<relations.length;i++){
            if(relations[i].span_front.start_offset == source_id && relations[i].span_after.start_offset == target_id){
                relations.splice(i,1);
            }
        }
     }
    //删除连接根据两个id
    function del_conns_by_two_id(source_id,target_id) {
        for(var i=0;i<connects.length;i++){
            if(source_id == connects[i].start && target_id == connects[i].end){
                //alert(connects[i].start)
                jsPlumb.deleteConnection(connects[i].connect);
                connects.splice(i,1);
            }
        }
    }
    //根据关系获取开始结束id
    function get_source_target(re_type) {
       // alert(JSON.stringify(relations))
        var sou_tas = []
        for(var i=0;i<relations.length;i++){
            if(re_type == relations[i].rel_type){
                var s_t = {}
                s_t.source = relations[i].span_front.start_offset
                s_t.target = relations[i].span_after.start_offset
                sou_tas.push(s_t)
            }
        }
       // alert(JSON.stringify(sou_tas))
        return sou_tas
    }
var save_path = ''
 $('.shuju').on('click','.file',(function () {
        var name = $(this).parent().attr('title')
        save_path = $(this).parent().parent().attr('id')
        $('#dname').html(name)
        var filena = $('.filena').text()
        data = {'name': name,'filena':filena,'save_path':save_path}
        $.ajax({
            url: '/annotation/get_file_content',
            type: 'POST',
            data: data,
            success: function (data) {
                $('#content-area').html('')
                $('#content-area').html(data.content_new)
                $('#content').html(data.content)
                $('.jtk-endpoint').remove()
                $('svg').remove()
                relations = []
                connects = []

                   for (var i = 0; i < data.relations.length; i++) {
                       var new_prop = ''
                        if(is_re(data.relations[i].source.toString())){
                           stub -= 13 * get_re_count(data.relations[i].source.toString())
                            connect(data.relations[i].source.toString(), data.relations[i].target.toString(),data.relations[i].label, 'property' + property_count,stub)
                            stub = 70
                        }else {
                           stub = 70
                            connect(data.relations[i].source.toString(), data.relations[i].target.toString(), data.relations[i].label, 'property' + property_count,stub)
                        }
                        if (data.relations[i].en1_prop.toString() == ''){
                           var eee1 = '实体1没有属性!'
                        }else{
                           var eee1 = data.relations[i].en1_prop.toString()
                        }
                        if (data.relations[i].en2_prop.toString() == ''){
                           var eee2 = '实体2没有属性!'
                        }else{
                           var eee2 = data.relations[i].en2_prop.toString()
                        }
                        let prop = data.relations[i].rel_property
                        if (prop == '') {
                             new_prop = '<span id="property' + property_count + '" data-source="' + data.relations[i].source.toString() + '" data-target="' + data.relations[i].target.toString() + '" data-en1-prop="'+eee1+'" data-en2-prop="'+eee2+'">该关系没有属性！</span>'
                       } else {
                             new_prop = '<span id="property' + property_count + '" data-source="' + data.relations[i].source.toString() + '" data-target="' + data.relations[i].target.toString() + '" data-en1-prop="'+eee1+'" data-en2-prop="'+eee2+'">' + prop + '</span>'
                        }

                        $('#re_props').append(new_prop)
                        property_count += 1
                       label = data.relations[i].label
                        get_relations(data.relations[i].source.toString(), data.relations[i].target.toString(), prop, data.relations[i].en1_prop.toString(), data.relations[i].en2_prop.toString())
                        get_conns(conn,data.relations[i].target.toString(),data.relations[i].target.toString())
                    }
                        // alert(JSON.stringify(data.relations[i]))
            }
        })
 }))
var save = ''
function to_json() {
        html = $('#content-area').html()
        content = $('#content').text()

        var filena = $('.filena').text()
        var name = $('#dname').text().split('.')[0]
        data = {'html': html,'content':content,'relations':JSON.stringify(relations),'filena':filena,'name':name,'save_path':save_path,'save':save}
        $.ajax({
            url: '/annotation/to_json',
            type: 'POST',
            data: data,
            success: function (data) {
                if(data == 'success') {
                     $.ajax({
                        url: '/annotation/save_file_update/'+filena,
                        type: 'POST',
                        success: function (data) {
                            if(save_path == 'yuanwenjian') {
                                $('#yibiao').html('')
                                for(var i=0;i<data.firsts.length;i++){
                                    $('#yibiao').append('<li style="margin-bottom: 11px;cursor: pointer;font-size: 13px" title="'+data.firsts[i]+'"><span class="file">'+data.firsts[i]+'</span></li>')
                                }
                            }else if(save_path == 'yibiao'){
                                 $('#erbiao').html('')
                                for(var i=0;i<data.seconds.length;i++){
                                    $('#erbiao').append('<li style="margin-bottom: 11px;cursor: pointer;font-size: 13px" title="'+data.seconds[i]+'"><span class="file">'+data.seconds[i]+'</span></li>')
                                }
                            }else if(save_path == 'erbiao') {
                                $('#sanbiao').html('')
                                for (var i = 0; i < data.three.length; i++) {
                                    $('#sanbiao').append('<li style="margin-bottom: 11px;cursor: pointer;font-size: 13px" title="' + data.three[i] + '"><span class="file">' + data.three[i] + '</span></li>')
                                }

                            }

                        }
                    })
                                toastr.success('保存成功！');
                            }
            }
        })
}
$('#save').click(function () {
    save = 'save'
    to_json()
})
$('.ignore').click(function () {
    if($('#dname').text() != '请选择文件开始标注！') {
            $.confirm({
                animation: 'RotateXR',
                closeAnimation: 'RotateYR',
                title: '选择',
                content: '是否确定忽略?（本次标注结果将不会保存！！！）',
                type: 'blue',
                columnClass: 'wi2',
                buttons: {
                    ok: {
                        text: '是',
                        btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                        action: function () {
                            $('#content-area').html('')
                            $('#content').html('')
                            $('.jtk-endpoint').remove()
                            $('svg').remove()
                            relations = []
                            connects = []
                            $('#dname').text('请选择文件开始标注！')
                        }
                    },
                    cancel: {
                        text: '否',
                        btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                        action: function () {

                        }
                    }
                }
            });
        }
})
$('.complete').click(function () {
    if($('#dname').text() != '请选择文件开始标注！') {
            $.confirm({
                animation: 'RotateXR',
                closeAnimation: 'RotateYR',
                title: '选择',
                content: '是否确定完成?（选择是将会生成下次标注文件，若要更新当前文档，请点击否然后点击右上方保存按钮！！！）',
                type: 'blue',
                columnClass: 'wi2',
                buttons: {
                    ok: {
                        text: '是',
                        btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                        action: function () {
                            save = 'no_save'
                            to_json()
                        }
                    },
                    cancel: {
                        text: '否',
                        btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                        action: function () {

                        }
                    }
                }
            });
        }
})
function connect(source_id, target_id, label, prop_c, stub){
    conn = jsPlumb.connect({
        anchor: ["TopCenter", "TopLeft", "TopRight"],
        source: source_id,
        target: target_id,
        endpoint: ['Dot', {radius: 3}],
        connector: ['Flowchart', {stub: stub}],
        paintStyle: { stroke: 'lightgray', strokeWidth: 1, cornerRadius: 5},
        overlays: [
            ["Label", {
            cssClass: "jspl_uml-label",
                labelStyle: {color: 'red'},
                label: label,
                //连接器的位置
                location: 0.5,
                id: "1",
                //点击事件
                events: {
                    "click": function () {
                                  $.alert({
                                      columnClass: 'wi2',
                                  title: '该关系属性：',
                                  type: 'blue',
                                  content: '关系属性：<input type="text" value="'+$('#'+prop_c).text()+'"/><br>实体1属性：<input type="text" value="'+$('#'+prop_c).attr('data-en1-prop')+'"/><br>实体2属性：<input type="text" value="'+$('#'+prop_c). attr('data-en2-prop')+'"/>'
                                   })
                    }
                    }
                }],
                ["Arrow",
                  {
                      cssClass: "l1arrow",
                      location: 1,
                      width: 10,
                      length: 10
                 }]
        ]
    })
}
function add_property(sour,targ) {
         $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '选择',
            content: '该关系是否包含属性?' +'\n'+
            '（Tip:选是则进行选择属性操作，选否则置属性为空）',
            type: 'blue',
            columnClass: 'wi2',
            buttons: {
                ok: {
                    text: '是(Y)',
                    keys:['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function() {
                        //get_relations(source, target)
                        toastr.warning('请选择此关系属性！')
                        has_property = true
                    }
                },
                cancel: {
                    text: '否(N)',
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    keys:['N'],
                    action: function() {
                        property = ''
                        has_property = false
                        get_relations(sour, targ, property, en1_property, en2_property)
                        get_conns(conn,sour,targ)
                        if (en1_property == ''){
                            var eee1 = '实体1没有属性!'
                        }
                        if (en2_property == ''){
                            var eee2 = '实体2没有属性!'
                        }
                        var new_prop = '<span id="property'+property_count+'" data-source="'+sour+'" data-target="'+targ+'" data-en1-prop="'+eee1+'" data-en2-prop="'+eee2+'">该关系没有属性！</span>'
                        $('#re_props').append(new_prop)
                        property_count += 1
                        toastr.success('继续下个标注！')
                        source = ''
                        target = ''
                    }
                }
            }
        });
    }
function add_en1_prop() {
     $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '选择',
            content: '实体1是否包含属性?' +'\n'+
            '（Tip:选是则进行选择属性操作，选否则置属性为空）',
            type: 'blue',
            columnClass: 'wi2',
            buttons: {
                ok: {
                    text: '是(Y)',
                    keys: ['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        toastr.warning('请选择此实体属性！')
                        en1_has_prop = true
                    }
                },
                cancel: {
                    text: '否(N)',
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    keys: ['N'],
                    action: function () {
                        en1_property = ''
                        en1_has_prop = false
                        toastr.success('实体属性标注完成！')
                        add_en2_prop()
                    }
                }
                }
            })
}
function add_en2_prop() {
     $.confirm({
            animation: 'RotateXR',
            closeAnimation: 'RotateYR',
            title: '选择',
            content: '实体2是否包含属性?' +'\n'+
            '（Tip:选是则进行选择属性操作，选否则置属性为空）',
            type: 'blue',
            columnClass: 'wi2',
            buttons: {
                ok: {
                    text: '是(Y)',
                    keys: ['Y'],
                    btnClass: 'mdc-button mdc-button--stroked mdc-ripple-upgraded',
                    action: function () {
                        toastr.warning('请选择此实体属性！')
                        en2_has_prop = true
                    }
                },
                cancel: {
                    text: '否(N)',
                    btnClass: 'mdc-button mdc-button--stroked secondary-stroked-button mdc-ripple-upgraded',
                    keys: ['N'],
                    action: function () {
                        en2_property = ''
                        en2_has_prop = false
                        toastr.success('实体属性标注完成！')
                        add_property(source, target)
                    }
                }
                }
            })
}