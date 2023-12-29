
function subscribe() {
    var first_name = document.getElementById("first_name").value;
    var last_name = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;
    var company_name = companyData.company_name;
    var company_coupon = companyData.company_coupon;
    document.getElementById("first_name").value = "";
    document.getElementById("last_name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("phone").value = "";
    var formData = new FormData();
    formData.append("first_name", first_name);
    formData.append("last_name", last_name);
    formData.append("email", email);
    formData.append("phone", phone);
    formData.append("company", company_name);
    formData.append("coupon", company_coupon);
    fetch("https://tbm.xemiron.com/core/save-email/", {
            method: "POST",
            body: formData,
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            var susbscribed1 = document.getElementById("susbscribe1");
            var susbscribed2 = document.getElementById("susbscribe2");
            if (data.email != undefined) {
                susbscribed2.innerText = "";
                susbscribed1.innerText = "Success! Thanks for subscribe.";
            } else {
                susbscribed1.innerText = "";
                susbscribed2.innerText = "Fail!";
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors here, such as displaying an error message to the user
        });
}
