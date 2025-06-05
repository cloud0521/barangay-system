// File: residents/static/residents/js/script.js
// (Or your chosen static file path)

// It's good practice to wrap your code in a DOMContentLoaded listener
// if the script might be loaded in the <head> or before the DOM is fully parsed.
// However, if you place the <script> tag at the end of the <body>,
// the DOM is usually ready by the time the script executes.
document.addEventListener('DOMContentLoaded', function() {

    // --- Script for contact_information field validation ---
    const contactInput = document.getElementById('id_contact_information');

    if (contactInput) {
        contactInput.addEventListener('keypress', function(event) {
            const char = event.key;
            // Allow digits, '+', and control keys like backspace, delete, arrow keys, Tab, Enter
            if (!/^[0-9+]$/.test(char) && 
                !event.ctrlKey && !event.metaKey && 
                !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', 'Enter'].includes(event.key)) {
                event.preventDefault(); // Prevent the character from being entered
            }
        });

        contactInput.addEventListener('paste', function(event) {
            const pasteData = (event.clipboardData || window.clipboardData).getData('text');
            // Validate the entire pasted string
            if (!/^[0-9+]*$/.test(pasteData)) {
                event.preventDefault(); // Prevent pasting invalid content
            }
        });
    }

    // --- Script to capitalize input for specified text fields ---

    // Function to capitalize input value
    function capitalizeInput(event) {
        const inputElement = event.target;
        // Preserve cursor position
        const start = inputElement.selectionStart;
        const end = inputElement.selectionEnd;
        
        inputElement.value = inputElement.value.toUpperCase();
        
        // Restore cursor position
        inputElement.setSelectionRange(start, end);
    }

    // Get the specific text input fields and textareas you want to apply capitalization to,
    // based on their IDs (Django's convention is id_<fieldname>).
    const fieldsToCapitalize = document.querySelectorAll(
        '#id_full_name, #id_occupation, #id_address, #id_notes, #id_purok, #id_nationality, #id_religion, #id_place_of_birth' // Targeting specific IDs
    );

    fieldsToCapitalize.forEach(field => {
        if (field) { // Check if the element actually exists
            // Using 'input' event for immediate capitalization as user types or pastes
            field.addEventListener('input', capitalizeInput);
        }
    });

    // --- Optional: Handle form submission for demonstration in standalone HTML ---
    // const residentForm = document.getElementById('residentForm');
    // if (residentForm && typeof django === 'undefined') { // Check if not in Django context for demo
    //     residentForm.addEventListener('submit', function(event) {
    //         event.preventDefault(); // Prevent actual submission for this demo
    //         alert('Form data (see console):');
    //         const formData = new FormData(residentForm);
    //         for (let [key, value] of formData.entries()) {
    //             console.log(key, value);
    //         }
    //     });
    // }
    

            const hamburger = document.getElementById('hamburger-icon');
            const navLinks = document.getElementById('navbar-links');

            if (hamburger && navLinks) {
                hamburger.addEventListener('click', function() {
                    const isActive = navLinks.classList.toggle('active');
                    hamburger.setAttribute('aria-expanded', isActive);

                    // Optional: Change icon from hamburger to 'X' (times) and back
                    const icon = hamburger.querySelector('i');
                    if (isActive) {
                        icon.classList.remove('fa-bars');
                        icon.classList.add('fa-times');
                    } else {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                });
            }
    
});

