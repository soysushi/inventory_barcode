$.noConflict();

jQuery(document).ready(function($) {

	"use strict";


	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	});

	jQuery('.selectpicker').selectpicker;

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

	$('.equal-height').matchHeight({
		property: 'max-height'
	});

	// var chartsheight = $('.flotRealtime2').height();
	// $('.traffic-chart').css('height', chartsheight-122);


	// Counter Number
	$('.count').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 3000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});

	var count = 1
	// Variant Trigger
	$('#variant-button').on('click', function() {
	    let $this = $("#id_variant_0")
	    let $clone = $this.clone()
			let name = $clone.attr('name')
		  let n = count
		  name = 'variant_' + n
			count++
			$clone.val('')
			$clone.attr('name', name)
			let new_id = "id_" + name
			$clone.attr('id', new_id)
			$clone.appendTo($this.parent())
			$this.addClass('form-control')
			// add variant value(s)
			})
	// Search Field
	const searchField = document.querySelector("#searchField");
	const tableOutput = document.querySelector(".table-output");
	const appTable = document.querySelector(".app-table");
	tableOutput.style.display = "block";
	searchField.addEventListener("keyup", (e) => {
		const searchValue = e.target.value;
		tableOutput.innerHTML="";
		if(searchValue.trim().length>0){



			console.log('searchValue', searchValue)

			fetch("search-products", {
				body: JSON.stringify({ searchText: searchValue }),
				method: "POST",
			})
				.then((res) => res.json())
				.then((data) => {
					console.log("data", data);
					if (data.length===0){
						tableOutput.innerHTML+=`
						<tr>
						<td>TEST</td>
						</tr>`;
					}
					else {

							tableOutput.innerHTML+=`
							<tr>
							<a href="../../${data.label}"<td><img src="../../${data.label}" width="300px"></img></td></a>
							</tr>`;

					};
				});
		}
		else{
			tableOutput.style.display = "none";
			appTable.style.display = "block";
		}
	});
	// Menu Trigger
	$('#menuToggle').on('click', function(event) {
		var windowWidth = $(window).width();
		if (windowWidth<1010) {
			$('body').removeClass('open');
			if (windowWidth<760){
				$('#left-panel').slideToggle();
			} else {
				$('#left-panel').toggleClass('open-menu');
			}
		} else {
			$('body').toggleClass('open');
			$('#left-panel').removeClass('open-menu');
		}

	});


	$(".menu-item-has-children.dropdown").each(function() {
		$(this).on('click', function() {
			var $temp_text = $(this).children('.dropdown-toggle').html();
			$(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>');
		});
	});


	// Load Resize
	$(window).on("load resize", function(event) {
		var windowWidth = $(window).width();
		if (windowWidth<1010) {
			$('body').addClass('small-device');
		} else {
			$('body').removeClass('small-device');
		}
	});


});
