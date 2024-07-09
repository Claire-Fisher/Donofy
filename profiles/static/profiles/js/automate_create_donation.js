// automates triggering create_donation_if_24th subscription view
document.addEventListener("DOMContentLoaded", function() {
    var today = new Date();
    if (today.getDate() === 24) {
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