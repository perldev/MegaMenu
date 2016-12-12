$(function() {

	$(".sf-menu").superfish({
		delay: 200,
		speed: "fast",
		cssArrows: false
	})
	.after("<div id='mobile-menu'>").clone().appendTo("#mobile-menu");
	$("#mobile-menu").find("*").attr("style", "");
	$("#mobile-menu").children("ul").removeClass("sf-menu")
	.parent().mmenu({
		extensions : [ 'widescreen', 'theme-white', 'effect-menu-slide', 'pagedim-black' ],
		navbar: {
			title: "Меню"
		}
	});

	$(".toggle-mnu").click(function() {
		$(this).addClass("on");
	});

	var api = $("#mobile-menu").data("mmenu");
	api.bind("closed", function () {
		$(".toggle-mnu").removeClass("on");
	});




	$(".sf-menu2").superfish({
		delay: 200,
		speed: "fast",
		cssArrows: false
	})
	.after("<div id='mobile-menu2'>").clone().appendTo("#mobile-menu2");
	$("#mobile-menu2").find("*").attr("style", "");
	$("#mobile-menu2").children("ul").removeClass("sf-menu2")
	.parent().mmenu({
		extensions : [ 'widescreen', 'theme-white', 'effect-menu-slide', 'pagedim-black' ],
		navbar: {
			title: "Название меню"
		}
	});

	$(".toggle-mnu2").click(function() {
		$(this).addClass("on");
		$(".toggleRow").addClass("rowOff");
		
	});

	var api = $("#mobile-menu2").data("mmenu");
	api.bind("closed", function () {
		$(".toggle-mnu2").removeClass("on");
		$(".toggleRow").removeClass("rowOff");
	});


});