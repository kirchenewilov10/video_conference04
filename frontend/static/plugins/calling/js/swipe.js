function visitPage() {
	window.location = "sign-in.html"
}
$(document).ready(function () {
	$(".filterMembers").not(".all").hide("3000"),
	$(".filterMembers").not(".all").hide("3000"),
	$(".filterMembersBtn").click(function () {
		var t = $(this).attr("data-filter");
		$(".filterMembers").not("." + t).hide("3000"),
		$(".filterMembers").filter("." + t).show("3000"),
		$(".filterMembersBtn").removeClass("active"),
		$(this).addClass("active")
	})
}), $(document).ready(function () {
	$(".filterDiscussions").not(".all").hide("3000"),
	$(".filterDiscussions").not(".all").hide("3000"),
	$(".filterDiscussionsBtn").click(function () {
		var t = $(this).attr("data-filter");
		$(".filterDiscussions").not("." + t).hide("3000"),
		$(".filterDiscussions").filter("." + t).show("3000")
	})
}), $(document).ready(function () {
	$(".filterNotifications").not(".all").hide("3000"),
	$(".filterNotifications").not(".all").hide("3000"),
	$(".filterNotificationsBtn").click(function () {
		var t = $(this).attr("data-filter");
		$(".filterNotifications").not("." + t).hide("3000"),
		$(".filterNotifications").filter("." + t).show("3000")
	})
}), $(document).ready(function () {
	$("#people").on("keyup", function () {
		var t = $(this).val().toLowerCase();
		$("#users_list a").filter(function () {
			$(this).toggle($(this).text().toLowerCase().indexOf(t) > -1)
		})
	})
}), $(document).ready(function () {
	$("#conversations").on("keyup", function () {
		var t = $(this).val().toLowerCase();
		$("#chats a").filter(function () {
			$(this).toggle($(this).text().toLowerCase().indexOf(t) > -1)
		})
	})
}), $(document).ready(function () {
	$("#notice").on("keyup", function () {
		var t = $(this).val().toLowerCase();
		$("#alerts a").filter(function () {
			$(this).toggle($(this).text().toLowerCase().indexOf(t) > -1)
		})
	})
}), $(document).ready(function () {
	clicked = !0,
	$(".mode").click(function () {
		clicked ? ($("head").append('<link href="dist/css/dark.min.css" id="dark" type="text/css" rel="stylesheet">'), clicked = !1) : ($("#dark").remove(), clicked = !0)
	})
}), $(".back").click(function () {
	$("#call" + $(this).attr("name")).hide(),
	$("#chat" + $(this).attr("name")).removeAttr("style")
}), $(".connect").click(function () {
	$("#chat" + $(this).attr("name")).hide(),
	$("#call" + $(this).attr("name")).show()
});