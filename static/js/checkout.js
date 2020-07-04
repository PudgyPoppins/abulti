//checkout.js
var stripe = Stripe('{{ stripe_pub_key }}');
var elements = stripe.elements({locale: window.__exampleLocale});

var cardNumber = elements.create('cardNumber', {
	style: style,
});
cardNumber.mount('#card-number');

var cardExpiry = elements.create('cardExpiry', {
	style: style,
});
cardExpiry.mount('#card-expiry');

var cardCvc = elements.create('cardCvc', {
	style: style,
});
cardCvc.mount('#card-cvc');

registerElements([cardNumber, cardExpiry, cardCvc]);


var address1;
var address2;
var city;
var state;
var zip;
var country;

var form = document.querySelector('form');
console.log(form)

document.querySelector('#id_shipping_country').value = 'US'
document.querySelector('#id_billing_country').value = 'US'

var same_check = document.getElementById('id_same_billing_address');
same_check.addEventListener("click", toggleBilling);

var billingBox = document.getElementById('billing');

function toggleBilling(){
	if(same_check.checked){
		billingBox.style.display = 'none';

		//the values ARE the same, get the submission info from the shipping boxes
		address1 = form.querySelector('#id_shipping_address');
		address2 = form.querySelector('#id_shipping_address2');
		city = form.querySelector('#id_shipping_city');
		state = form.querySelector('#id_shipping_state');
		zip = form.querySelector('#id_shipping_zip');
		country = form.querySelector('#id_shipping_country');

	} else{
		billingBox.style.display = 'initial';

		//the values are not the same, get the submission info from the billing boxes
		address1 = form.querySelector('#id_billing_address');
		address2 = form.querySelector('#id_billing_address2');
		city = form.querySelector('#id_billing_city');
		state = form.querySelector('#id_billing_state');
		zip = form.querySelector('#id_billing_zip');
		country = form.querySelector('#id_billing_country');
	}
}
toggleBilling();

var style = {
	base: {
		color: "#32325d",
	}
};


function registerElements(elements) {
	var wrapper = document.querySelector('#payment-form');
	var error = form.querySelector('#card-errors');
	var errorMessage = error.querySelector('.card-error');

	function enableInputs() {
		Array.prototype.forEach.call(
			form.querySelectorAll(
				"input[type='text'], input[type='email'], input[type='tel']"
			),
			function(input) {
				input.removeAttribute('disabled');
			}
		);
	}

	function disableInputs() {
		Array.prototype.forEach.call(
			form.querySelectorAll(
				"input[type='text'], input[type='email'], input[type='tel']"
			),
			function(input) {
				input.setAttribute('disabled', 'true');
			}
		);
	}

	function triggerBrowserValidation() {
		// The only way to trigger HTML5 form validation UI is to fake a user submit
		// event.
		var submit = document.createElement('input');
		submit.type = 'submit';
		submit.style.display = 'none';
		form.appendChild(submit);
		submit.click();
		submit.remove();
	}

	// Listen for errors from each Element, and show error messages in the UI.
	var savedErrors = {};
	elements.forEach(function(element, idx) {
		element.on('change', function(event) {
			if (event.error) {
				error.classList.add('visible');
				savedErrors[idx] = event.error.message;
				errorMessage.innerText = event.error.message;
			} else {
				savedErrors[idx] = null;

				// Loop over the saved errors and find the first one, if any.
				var nextError = Object.keys(savedErrors)
					.sort()
					.reduce(function(maybeFoundError, key) {
						return maybeFoundError || savedErrors[key];
					}, null);

				if (nextError) {
					// Now that they've fixed the current error, show another one.
					errorMessage.innerText = nextError;
				} else {
					// The user fixed the last error; no more errors.
					error.classList.remove('visible');
				}
			}
		});
	});

	// Listen on the form's 'submit' handler...
	form.addEventListener('submit', function(e) {
		e.preventDefault();
		payWithCard(stripe, card, data.clientSecret);

		/*// Trigger HTML5 validation UI on the form if any of the inputs fail
		// validation.
		var plainInputsValid = true;
		Array.prototype.forEach.call(form.querySelectorAll('input'), function(
			input
		) {
			if (input.checkValidity && !input.checkValidity()) {
				plainInputsValid = false;
				return;
			}
		});
		if (!plainInputsValid) {
			triggerBrowserValidation();
			return;
		}

		// Gather additional customer data we may have collected in our form.
		var name = form.querySelector('#id_name');
		
		var additionalData = {
			name: name ? name.value : undefined,
			address_line1: address1 ? address1.value : undefined,
			address_line2: address2 ? address2.value : undefined,
			address_city: city ? city.value : undefined,
			address_state: state ? state.value : undefined,
			address_zip: zip ? zip.value : undefined,
			address_country: country ? country.value : undefined,
		};

		// Use Stripe.js to create a token. We only need to pass in one Element
		// from the Element group in order to create a token. We can also pass
		// in the additional customer data we collected in our form.
		stripe.createToken(elements[0], additionalData).then(function(result) {
			// Stop loading!
			//wrapper.classList.remove('submitting');

			if (result.token) {
				// If we received a token, show the token ID.
				//wrapper.querySelector('.token').innerText = result.token.id;

				form.submit();
			} else {
				// Otherwise, un-disable inputs.
				enableInputs();
			}
		});*/
	});
}
