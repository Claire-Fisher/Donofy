var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
    base: {
        color: '#222',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {style: style});
card.mount('#card-element');

var form = document.getElementById('setup-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    var errorDiv = document.getElementById('card-errors');
    stripe.confirmCardSetup(
        clientSecret,
        {
            payment_method: {
                card: card,
                billing_details: {
                    name: '{{ user.first_name }} {{ user.last_name }}',
                    email: '{{ user.email }}',
                    address: {
                        line1: '{{ user_profile.street_address_1 }}',
                        line2: '{{ user_profile.street_address_2 }}',
                        city: '{{ user_profile.town_or_city }}',
                        state: '{{ user_profile.county }}',
                        postal_code: '{{ user_profile.post_code_zip }}',
                        country: '{{ user_profile.country.code }}'
                    },
                    phone: '{{ user_profile.phone_num }}',
                    consent: '{{ user_profile.payment_consent }}'
                }
            }
        }
    ).then(function(result) {
        if (result.error) {
            var html = `
            <span class="icon icon-pink role=alert">
                <i class="fa-solid fa-times-circle"></i>
            </span>
            <span>${result.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            stripeTokenHandler(result.setupIntent);
        }
    });
});

function stripeTokenHandler(setupIntent) {
    var form = document.getElementById('setup-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'setup_intent_id');
    hiddenInput.setAttribute('value', setupIntent.id);
    form.appendChild(hiddenInput);

    form.submit();
}
