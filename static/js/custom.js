
    function showHide(input, butt_show, butt_hide) {
        try {
            const inputEl = document.getElementById(input);
            const showB = document.getElementById(butt_show);
            const showH = document.getElementById(butt_hide);

            function hendelShowHide() {
                if (inputEl.type == 'password') {
                    inputEl.type = 'text';

                } else {
                    inputEl.type = 'password';
                }
        
                showB.classList.toggle('d-none');
                showH.classList.toggle('d-none');
                showB.style.color = 'gray';
            }

            showB.addEventListener('click', hendelShowHide);
            showH.addEventListener('click', hendelShowHide);
        } catch (error) {
            //nothing
        }


    }

    showHide('password', "password-show", "password-hide");
    showHide('password2', "password-show2", "password-hide2");



    tinymce.init({
        selector: 'textarea', // change this value according to your HTML
        plugins: 'a_tinymce_plugin',
        a_plugin_option: true,
        a_configuration_option: 400
    });

    const userProfile = document.getElementById('user-profile');
    const showUserProfile = document.getElementById('user-profile-menu');
    const allDiv = document.getElementById('all-div');


    userProfile.addEventListener('click', () => {
        showUserProfile.classList.toggle('d-none');
    });


    document.addEventListener('click', (event) => {
        if (!userProfile.contains(event.target)) {
            showUserProfile.classList.add('d-none');
        }else{
            showUserProfile.classList.remove('d-none');
        }
    });


   

    document.addEventListener("DOMContentLoaded", function () {
        // When the dropdown changes, show or hide the date input
        const dateFilter = document.getElementById("dateFilter");
        const dateInput = document.getElementById("datepicker");
    
        dateFilter.addEventListener('change', function () {
            const selectedValue = dateFilter.value;
    
            if (selectedValue === "before" || selectedValue === "after") {
                dateInput.style.display = "block";
            } else {
                dateInput.style.display = "none";
            }
        });
    });



 