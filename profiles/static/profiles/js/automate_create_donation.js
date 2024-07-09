// automates triggering create_donation_if_24th subscription view
document.addEventListener("DOMContentLoaded", function() {
    var today = new Date();
    // Date requirement would be set to === 24 if donation creation is automated
    if (today.getDate() >= 1) {
        fetch('/create-donation/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});