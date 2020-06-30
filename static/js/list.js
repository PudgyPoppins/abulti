var min = document.getElementById("min");
var max = document.getElementById("max");

min.addEventListener("input", minUpdate);
minUpdate();

max.addEventListener("input", maxUpdate);
maxUpdate(); 

function minUpdate() {
	var x = min.value;
	document.getElementById("minprice").innerHTML = x;
	max.min = x;
	maxUpdate(); //for some stupid reason javascript is weird and doesn't update the display first time, so I do it here and idk why
	if(min.value > max.value){
		max.value = x;
		maxUpdate();
	}
}
function maxUpdate() {
	var x = max.value;
	document.getElementById("maxprice").innerHTML = x;
}


// Filtering Stuff
$( ".cardWrapper" ).addClass( "isotope" );

var checkboxFilter;
var sRegex;
var minPrice = 0;
var maxPrice = Number.MAX_VALUE; //idk, maybe we'll sell shirts that cost over $2^53.00

var $container = $('.cardWrapper').isotope({
	itemSelector: '.shopCard',
	layoutMode: 'fitRows',

	getSortData: {
    	name: '.name',
	    popularity: '.pop parseInt',
	    date: '.date parseInt',
	    price: function( itemElem ) {
			var price = $( itemElem ).find('.price').text();
			return parseFloat( price.replace( /[$]/g, '') );
    	},
    },
	filter: function() {
		var $this = $(this);

		var itemName = $this.children('.cardCaption').children('.captionInfo').children('.name').text();
		var searchResult = sRegex ? itemName.match( sRegex ) : true;
		
		var checkboxResult = checkboxFilter ? $this.is( checkboxFilter ) : true;
		
		var itemPrice = parseFloat($this.children('.cardCaption').children('.captionInfo').children('.price').text().replace( /[$]/g, ''));
		//^ this fuckin monstrosity of a line gets the item price as a float
		var priceResult = itemPrice > minPrice && itemPrice < maxPrice;
		return searchResult && checkboxResult && priceResult;
	},
});

//Checkboxes filtering stuff
var $checkboxes = $('#checkboxes input');
$checkboxes.change(updateCheckboxes);
function updateCheckboxes(){
	var inclusives = [];
	$checkboxes.each( function( i, elem ) {
		if ( elem.checked ) {
			inclusives.push( elem.value );
		}
	})
	checkboxFilter = inclusives.length ? inclusives.join(', ') : '*';
	$container.isotope();
}
updateCheckboxes();
//end checkbox filter stuff


//Search bar filtering stuff
var $search = $('.search').keyup( debounce( function() {
	sRegex = new RegExp( $search.val(), 'gi' );
	$container.isotope();
}) );

function debounce( fn, threshold ) {
	var timeout;
	threshold = threshold || 100;
	return function debounced() {
		clearTimeout( timeout );
		var args = arguments;
		var _this = this;
		function delayed() {
			fn.apply( _this, args );
	}
	timeout = setTimeout( delayed, threshold );
	};
}
//end search bar filter stuff

//slider filtering stuff
var $min = $('#min'); 
$min.change(filterMinPrice);
function filterMinPrice(){
	minPrice = $min.val();
	$container.isotope();
}
filterMinPrice();

var $max = $('#max'); 
$max.change(filterMaxPrice);
function filterMaxPrice(){
	maxPrice = $max.val();
	$container.isotope();
}
filterMaxPrice();
//end slider filter stuff

//select sorting stuff
$('#sort').change(selectSort);
function selectSort(){
	var sortByValue = this.value;
	var isAscending = !($(this).find('option:selected').attr('id') == 'dec');
	$container.isotope({ sortBy: sortByValue, sortAscending: isAscending });
}
selectSort();
//end select sort stuff