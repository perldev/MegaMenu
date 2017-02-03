var Chanels = {};
$( document ).ready(function() {
    $("#chanel_errors").hide();

    var cat;

    Chanels.action="add";
    Chanels.add_item = function(id, obj){
            cat = id;
            console.log("add changel");
            $("#id_chanel").val(cat);
            Chanels.action = "add";
            $("#wrapper_title_chanel_item").show();
            $("#wrapper_ordering_chanel_item").show();
            $("#wrapper_content_chanel_item").show();
            $("#wrapper_image_chanel_item").show();
            
            if($(obj).data("disable_title")){
                $("#wrapper_title_chanel_item").hide();
            }
            if($(obj).data("disable_content")){
                $("#wrapper_content_chanel_item").hide();
            }
            if($(obj).data("disable_ordering")){
                $("#wrapper_ordering_chanel_item").hide();
            }
            if($(obj).data("disable_image")){
                $("#wrapper_image_chanel_item").hide();
            }            
	    
            $("#myChanelModal").modal("show");
            $("#title_chanel_item").val("");
            $("#myModalLabelChanel").html("Add");
    };
    Chanels.edit_item = function(obj, cat, id){
            $("#id_chanel").val(id);
            Chanels.action = "edit";
            $("#myChanelModal").modal("show");

            $("#wrapper_title_chanel_item").show();
            $("#wrapper_ordering_chanel_item").show();
            $("#wrapper_content_chanel_item").show();
            $("#wrapper_image_chanel_item").show();
            
            if($(obj).data("disable_title")){
                $("#wrapper_title_chanel_item").hide();
            }
            if($(obj).data("disable_content")){
                $("#wrapper_content_chanel_item").hide();
            }
            if($(obj).data("disable_ordering")){
                $("#wrapper_ordering_chanel_item").hide();
            }
            if($(obj).data("disable_image")){
                $("#wrapper_image_chanel_item").hide();
            }            
            console.log($(obj).data("title"));
            console.log($(obj).data("ordering"));
            console.log($(obj).data("content"));
            console.log($(obj).data("img"));
            console.log($(obj).data("disable_title"));
            console.log($(obj).data("disable_ordering"));
            console.log($(obj).data("disable_content"));
            console.log($(obj).data("disable_image"));

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
        var email_decoded = encodeURI(email);
        $.ajax({
            url: "subscribe/add?email=" + email_decoded,
            type: 'GET',
            async: true,
            success: function (data) {
                  MyCommon.modal("Спасибо за ваш интерес,<p>\
                                  регулярное обновление нашего ассортимента </p><p>\
                                  будет присылаться на почту <strong>"+email+"</strong></p>",
                                 "Спасибо, вы подписаны на наши новости");
            },
            cache: false,
            contentType: false,
            processData: false
        });      
        $("#SubInputEmail").val("");
        return false;
    });
    $("#contactForm").on("submit", function(ev){
        var formData = new FormData($("#contactForm")[0]);
        $.ajax({
            url: "send_marina",
            type: 'POST',
            data: formData,
            async: true,
            success: function (data) {
                  MyCommon.modal("Мы ответим на ваш вопрос в кратчайшие сроки","Спасибо за ваш интерес");
            },
            cache: false,
            contentType: false,
            processData: false
        });      
        
        $("#question").val("");
        $("#name").val("");
        $("#contact").val("");
        return false;
    });
    
    
    
    
    
    
    
    
    
    
    
    
    var MyCart = {};
    MyCart.add_package = function(pk){
       $.ajax({
            url: "cart/add_package/"+pk,
            type: 'GET',
            async: true,
            success: function (data) {
		MyCommon.modal("Акционный пакет добавлен вам в корзину","Корзина");
		var count = $("#cart_count").html();
		count = count*1+2;
		$("#cart_count").html(count);
	    },
            cache: false,
            contentType: false,
            processData: false
        });      
      
    };
    
    
    MyCart.add2cart_simple = function(pk, count, title){
      
         $.ajax({
            url: "cart/add/"+pk+"/"+count,
            type: 'GET',
            async: true,
            success: function (data) {
		MyCommon.modal("Позиция '"+title+"' добавлена вам в корзину в количестве 1 шт.","Корзина");
		var count = $("#cart_count").html();
		count = count*1+1;
		$("#cart_count").html(count);
	    },
            cache: false,
            contentType: false,
            processData: false
        });      
    };
    MyCart.change_item_count = function(pk, price, obj){

      var count = obj.value;
      $.ajax({
            url: "cart/change/item/"+pk+"/"+count,
            type: 'GET',
                  success: function (data) {
                        var total_price = price*count;
                        $("#total_item_price_"+pk).html(total_price.toFixed(2)+" грн");
                        $("#cart_total").html(data["price"]+" грн");
                  },
                  cache: false,
                  contentType: false,
                  processData: false
              });
	
      
    };
    MyCart.delete_item = function(pk){
           
         $.ajax({
            url: "cart/del/item/"+pk,
            type: 'GET',
            async: true,
            success: function (data) {
               var group = $("#cart_position_"+pk).data("group")
               if(group){
                  $(".group_"+group).hide();
               }else{
                  $("#cart_position_"+pk).hide();
               }
               $("#cart_total").html(data["price"]);
               
              },
              cache: false,
              contentType: false,
              processData: false
        });
      
    };
    
    MyCart.add2cart_count_from = function(pk, count_of_items, title){
         var count = $(count_of_items).val()*1;
         $.ajax({
            url: "cart/add/"+pk+"/"+count,
            type: 'GET',
            async: true,
            success: function (data) {
		MyCommon.modal("Позиция '"+title+"' добавлена вам в корзину в количестве "+count+" шт.","Корзина");
		var count_cart = $("#cart_count").html();
		count_cart = count_cart*1+count;
		$("#cart_count").html(count_cart);
	    },
            cache: false,
            contentType: false,
            processData: false
        });
      
      
    };  
    
    
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
        console.log(Chanels.action);
        $("#content_chanel").html(content);
        var formData = new FormData($("#form_chanel")[0]);
	
        $.ajax({
            url: "chanel/"+Chanels.action,
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
    window.MyCart = MyCart;
    $(".formSubmit").on("click", function(ev){
	var id = $(this).data("submit");
        console.log(id);
	$(id).submit();
    });
    

});