
//Popovers initialization

$("[data-toggle=popover]").each(function(i, obj) {

$(this).popover({
	// container: 'body',
	delay: { "show": 500, "hide": 100},
	animation:true,
	html: true,
	content: function() {
	var id = $(this).attr('id')
	return $('#popover-content-' + id).html();
  }
});

});

// SIPPING FORM

$("#id_shipping_0").on("click", function(){		
		$("label[for='id_address']").parent().show();
});

$("#id_shipping_1").on("click", function(){		
		$("label[for='id_address']").parent().hide();		
});

// Переключение grid/list of Products
var productViews = $(".products-view");
var icons = $(".icon");

function hideAllViews(){
	for (var i=0; i<productViews.length; i++){
		$(productViews[i]).hide();
	}
}

function bindIconToView(idNumber){
	$(".icon-"+idNumber).click(function(){
		hideAllViews();
		$(".products-view-"+idNumber).show();

		for (var i=1; i<=icons.length; i++){
			if (i==idNumber) {
				$(".icon-"+i).addClass("dark");
			}
			else {
				$(".icon-"+i).removeClass("dark");
			}
		}
	})
}

for (var i=1; i<=icons.length; i++){
	bindIconToView(i);
}

hideAllViews();
var doc_w = $(document).width();
console.log(doc_w);
if (doc_w<=500){
	$(".products-view-1").show();
	$(".icon-1").addClass("dark");
}
else{
	$(".products-view-2").show();
	$(".icon-2").addClass("dark");
}

// ---/ Переключение grid/list of Products