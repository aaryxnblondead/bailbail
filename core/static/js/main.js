// Main JavaScript for BailReckoner

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    initializeBootstrapComponents();
    
    // Setup event listeners
    setupEventListeners();
});

function initializeBootstrapComponents() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

function setupEventListeners() {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && alert.parentNode) {
                alert.classList.add('fade');
                setTimeout(function() {
                    if (alert && alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 300);
            }
        }, 5000);
    });
    
    // Make tables with .table-clickable have clickable rows
    const clickableTables = document.querySelectorAll('.table-clickable');
    clickableTables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            if (row.dataset.href) {
                row.style.cursor = 'pointer';
                row.addEventListener('click', function(e) {
                    if (!e.target.closest('a, button, input, .no-click')) {
                        window.location = row.dataset.href;
                    }
                });
            }
        });
    });
}

// Handle form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
            
            // Create error message if not exists
            let errorMessage = field.nextElementSibling;
            if (!errorMessage || !errorMessage.classList.contains('invalid-feedback')) {
                errorMessage = document.createElement('div');
                errorMessage.className = 'invalid-feedback';
                errorMessage.textContent = 'This field is required';
                field.parentNode.insertBefore(errorMessage, field.nextSibling);
            }
        } else {
            field.classList.remove('is-invalid');
            
            // Remove error message if exists
            const errorMessage = field.nextElementSibling;
            if (errorMessage && errorMessage.classList.contains('invalid-feedback')) {
                errorMessage.remove();
            }
        }
    });
    
    return isValid;
}

// Handle file uploads with preview
function handleFileUpload(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    if (!input || !preview) return;
    
    input.addEventListener('change', function() {
        preview.innerHTML = '';
        
        if (input.files && input.files[0]) {
            const file = input.files[0];
            const fileReader = new FileReader();
            
            fileReader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'img-thumbnail';
                preview.appendChild(img);
            };
            
            fileReader.readAsDataURL(file);
        }
    });
}