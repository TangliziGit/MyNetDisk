$('#uploadBtn').click(function(){
    $('#uploadForm').submit();
})

$('#loginBtn').click(function(){
    $('#loginForm').submit();
})

$('#downloadBtn').click(function(){
    var ids=new Array();
    
    $('.checkBox').each(function(index, item){
        if ($(this).prop('checked'))
            ids.push(index);
    })

    $('#downloadForm input').val(JSON.stringify(ids));
    $('#downloadForm').submit();
});

$('#removeBtn').click(function(){
    var ids=new Array();
    
    $('.checkBox').each(function(index, item){
        if ($(this).prop('checked'))
            ids.push(index);
    })

    $('#removeForm input').val(JSON.stringify(ids));
    $('#removeForm').submit();
});

$('#totalCheckBox').click(function(){
    if ($(this).prop('checked'))
        $('.checkBox').prop('checked', true);
    else
        $('.checkBox').prop('checked', false);
})

$(document).ready(function(){
    $('<form />',{
        id: "downloadForm",
        method: "POST",
        action: serverUrl+"/download"
    }).appendTo('#column');

    $('<form />',{
        id: "removeForm",
        method: "POST",
        action: serverUrl+"/remove"
    }).appendTo('#column');

    $('#uploadForm').attr('action', serverUrl+"/upload");
    $('#loginForm').attr('action', serverUrl+"/login");

    $('<input />', {
        type: 'hidden',
        name: 'ids',
        value: ''
    }).appendTo('#downloadForm');

    $('<input />', {
        type: 'hidden',
        name: 'ids',
        value: ''
    }).appendTo('#removeForm');
})
