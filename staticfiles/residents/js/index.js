       // Get references to the search input and the list container
        const searchInput = document.getElementById('search-input');
        const residentsListContainer = document.getElementById('residents-list-container');
        const searchForm = document.getElementById('search-form');

        // Prevent the default form submission for the search
        if (searchForm) { // Check if searchForm exists to avoid errors on other pages
            searchForm.addEventListener('submit', function(event) {
                event.preventDefault();
            });
        }


        // Add an event listener to the search input for 'input' event
        if (searchInput) { // Check if searchInput exists
            searchInput.addEventListener('input', function() {
                const query = searchInput.value; // Get the current value of the input

                // Construct the URL for the search request
                // Ensure 'index' is the correct URL name for your AJAX endpoint for search
                const searchUrl = `{% url 'index' %}?q=${encodeURIComponent(query)}`;

                // Use the Fetch API to send an asynchronous request to the server
                fetch(searchUrl, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest' // Important for Django to recognize AJAX
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json(); // Parse the JSON response
                })
                .then(data => {
                    // Update the residents list container with the new data
                    // Use window.location.pathname + window.location.search for currentPath
                    // as the AJAX response might not always contain the path you need for 'next'
                    const currentPath = window.location.pathname + window.location.search;
                    updateResidentsList(data.residents, currentPath);
                })
                .catch(error => {
                    console.error('Error fetching search results:', error);
                    residentsListContainer.innerHTML = '<p>Error loading search results. Please try again.</p>';
                });
            });
        }


        // Function to update the HTML table based on the received data
        // Accepts residents data and the current path (including potential query)
        function updateResidentsList(residents, currentPath) {
            let html = ''; // Start with an empty string to build the new HTML
            const currentPathEncoded = encodeURIComponent(currentPath); // Encode the path for the URL parameter

            if (residents && residents.length > 0) { // Add check for residents being defined
                html += '<table>';
                html += '<thead><tr><th>Full Name</th><th>Address</th><th>Tier</th><th>Action</th></tr></thead>'; // Updated headers
                html += '<tbody>';
                residents.forEach(resident => {
                    // Construct the URL for the resident detail page
                    // Ensure your JSON response for residents includes 'id', 'full_name', 'address', and 'tier'
                    const detailUrl = `/residents/${resident.id}/`;
                    // Construct the URL for edit/delete pages, passing the current path as 'next'
                    const editUrl = `/residents/${resident.id}/edit/?next=${currentPathEncoded}`;
                    const deleteUrl = `/residents/${resident.id}/delete/?next=${currentPathEncoded}`;

                    html += `
                        <tr>
                            <td>
                                <a href="${detailUrl}">
                                    ${resident.full_name || 'N/A'} {# Add fallback for potentially missing data #}
                                </a>
                            </td>
                            <td>${resident.address || 'N/A'}</td>
                            <td>${resident.tier || 'N/A'}</td> {# Display Tier #}
                            <td>
                                <div class="resident-actions">
                                    <a href="${editUrl}" title="Edit">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <a href="${deleteUrl}" title="Delete">
                                        <i class="fas fa-trash-alt"></i>
                                    </a>
                                </div>
                            </td>
                        </tr>
                    `;
                });
                html += '</tbody>';
                html += '</table>';
            } else {
                html += '<p>No residents found.</p>';
            }

            // Replace the content of the residents list container
            if(residentsListContainer) { // Check if container exists
                 residentsListContainer.innerHTML = html;
            }
        }

        // Note: The initial render is handled by Django.
        // The AJAX part only updates the list when the search input changes.



 document.addEventListener('DOMContentLoaded', function() {
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