/**
 * Smart IT Ticket Prioritizer - Main JavaScript file
 * Handles UI interactions and dynamic functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get the current page
    const currentPath = window.location.pathname;
    
    // Initialize based on the page
    if (currentPath.includes('/submit')) {
        initSubmitPage();
    } else if (currentPath.includes('/tickets')) {
        initTicketsPage();
    }

    // Initialize any global elements that appear on all pages
});

/**
 * Initialize the Submit Ticket page functionality
 */
function initSubmitPage() {
    const titleInput = document.getElementById('title');
    const descInput = document.getElementById('description');
    const form = document.getElementById('ticketForm');
    const previewSection = document.getElementById('classification-preview');
    
    // Set up form validation
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
            }
        });
    }
    
    // Set up live classification preview (if both inputs exist)
    if (titleInput && descInput) {
        // Throttled preview update
        let typingTimer;
        const doneTypingInterval = 1000; // ms
        
        const updatePreview = function() {
            // Only show preview if both fields have content
            if (titleInput.value.trim() && descInput.value.trim()) {
                // Make API call to get classification
                fetch('/api/classify', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        title: titleInput.value,
                        description: descInput.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.error) {
                        // Update preview
                        document.getElementById('priority-preview').textContent = data.priority;
                        document.getElementById('team-preview').textContent = data.team;
                        
                        // Show preview section
                        previewSection.classList.remove('hidden');
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                // Hide preview if fields are empty
                previewSection.classList.add('hidden');
            }
        };
        
        // Input event listeners with debounce
        titleInput.addEventListener('input', function() {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(updatePreview, doneTypingInterval);
        });
        
        descInput.addEventListener('input', function() {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(updatePreview, doneTypingInterval);
        });
    }
    
    // Form validation function
    function validateForm() {
        let isValid = true;
        
        // Check title (required, min length 5)
        if (!titleInput.value || titleInput.value.trim().length < 5) {
            showError(titleInput, 'Title is required and must be at least 5 characters');
            isValid = false;
        } else {
            removeError(titleInput);
        }
        
        // Check description (required, min length 20)
        if (!descInput.value || descInput.value.trim().length < 20) {
            showError(descInput, 'Description is required and must be at least 20 characters');
            isValid = false;
        } else {
            removeError(descInput);
        }
        
        return isValid;
    }
    
    // Helper functions for form validation
    function showError(element, message) {
        // Remove any existing error
        removeError(element);
        
        // Add error class to element
        element.classList.add('error');
        
        // Create and add error message
        const errorMessage = document.createElement('div');
        errorMessage.className = 'field-error-message';
        errorMessage.textContent = message;
        element.parentNode.appendChild(errorMessage);
    }
    
    function removeError(element) {
        // Remove error class
        element.classList.remove('error');
        
        // Remove error message if exists
        const errorMessage = element.parentNode.querySelector('.field-error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }
}

/**
 * Initialize the View Tickets page functionality
 */
function initTicketsPage() {
    // Get filter elements
    const searchInput = document.getElementById('ticketSearch');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const teamFilter = document.getElementById('teamFilter');
    const tableRows = document.querySelectorAll('.tickets-table tbody tr');
    
    // Set up search functionality
    if (searchInput) {
        searchInput.addEventListener('input', filterTickets);
    }
    
    // Set up priority filter buttons
    if (filterButtons) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Filter the tickets
                filterTickets();
            });
        });
    }
    
    // Set up team filter dropdown
    if (teamFilter) {
        teamFilter.addEventListener('change', filterTickets);
    }
    
    // Combined filter function
    function filterTickets() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const priorityFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
        const teamFilterValue = teamFilter ? teamFilter.value : 'all';
        
        // Loop through all ticket rows
        tableRows.forEach(row => {
            const title = row.querySelector('.ticket-title').textContent.toLowerCase();
            const description = row.querySelector('.ticket-description').textContent.toLowerCase();
            const rowPriority = row.className.match(/priority-(\w+)/)[1];
            const rowTeam = row.className.match(/team-(\w+)/)[1];
            
            // Check if row matches all filters
            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesPriority = priorityFilter === 'all' || rowPriority === priorityFilter;
            const matchesTeam = teamFilterValue === 'all' || rowTeam === teamFilterValue;
            
            // Show/hide row based on filters
            if (matchesSearch && matchesPriority && matchesTeam) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
}