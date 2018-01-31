
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

// SIPPING FORM

// FORM

// После клика по input окну если есть подсказка, она исчезает, 

$( 'input.form-control' ).on( 'select click', function( evt ) {
  if ($(evt.target).val()!==0){
    $(evt.target).val('');
	}
  })
// FORM