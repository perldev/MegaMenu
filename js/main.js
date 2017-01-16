var Chanels = {};
$( document ).ready(function() {
    $("#chanel_errors").hide();

    var cat;

    var action="add";
    Chanels.add_item = function(id){
            cat = id;
            $("#id_chanel").val(cat);
            action = "add"
            $("#myChanelModal").modal("show");
            $("#title_chanel_item").val("");
            $("#myModalLabelChanel").html("Add");
    };
    Chanels.edit_item = function(obj, cat, id){
            $("#id_chanel").val(id);
            action = "edit";
            $("#myChanelModal").modal("show");
            console.log($(obj).data("title"));
            console.log($(obj).data("ordering"));
            console.log($(obj).data("content"));
            $("#title_chanel_item").val( $(obj).data("title") );
            $("#ordering_chanel_item").val( $(obj).data("ordering") );
            $("#myModalLabelChanel").html("Edit");
            tinyMCE.activeEditor.setContent($(obj).data("content"));

    };
    Chanels.delete_item = function(obj, category, id){
        cat=id;
        console.log($(obj).data("title"));
        $("#myChanelDeleteModalContent").html("Delete?<br/>" + $(obj).data("title") );
        $("#myChanelDeleteModal").modal("show");


    };

    
    $("#chanel_item_delete").on("click", function(event){

         $.ajax({
            url: "chanel/delete/"+cat,
            type: 'GET',
            async: true,
            success: function (data) {
                window.location.reload();

            },
            cache: false,
            contentType: false,
            processData: false
        });
    });

    $("#subscription").on("submit", function(ev){
        var email = $("#SubInputEmail").val();
            
        MyCommon.modal("Подписка", "Спасибо за ваш интерес,<p>\
                        регулярное обновление нашего ассортимента </p><p>\
                        будет присылаться на почту <strong>"+email+"</strong></p>\
                        ");
        $("#SubInputEmail").val("");
        return false;
    });
    
    var MyCommon = {};


    MyCommon.modal = function(html, title) {
          $("#info_body").html(html);
          $("#info_modal_label").html(title);
          $("#modal_info").modal("show");
    };

    MyCommon.hide_modal = function() {
            $("#modal_info").modal("hide");
    };

    MyCommon.hide_confirm = function() {
            $("#confirm_modal").modal("hide");
    };

    window.MyCommon = MyCommon;

    


    $("#chanel_btn").on("click", function(event){
        event.preventDefault();
        content = tinyMCE.activeEditor.getContent();

        $("#content_chanel").html(content);
        console.log(content);
        var formData = new FormData($("#form_chanel")[0]);

        $.ajax({
            url: "chanel/"+action,
            type: 'POST',
            data: formData,
            async: true,
            success: function (data) {
                $("#myChanelModal").modal("hide");
                window.location.reload();

            },
            error: function(data){
                $("#chanel_errors").show("fast");
                $("#chanel_errors").hide(1500);
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
    });

});