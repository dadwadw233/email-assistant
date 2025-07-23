// Email Assistant Dashboard JavaScript

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Format date
function formatDate(dateString) {
    if (!dateString) return 'Unknown date';
    
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Format importance
function formatImportance(importance) {
    if (importance >= 0.7) return 'High';
    if (importance >= 0.4) return 'Medium';
    return 'Low';
}

// Get category icon
function getCategoryIcon(category) {
    const icons = {
        'work': 'fa-briefcase',
        'personal': 'fa-user-friends',
        'newsletter': 'fa-newspaper',
        'spam': 'fa-exclamation-triangle',
        'other': 'fa-question-circle'
    };
    return icons[category] || icons['other'];
}

// Get category class
function getCategoryClass(category) {
    const classes = {
        'work': 'bg-info',
        'personal': 'bg-success',
        'newsletter': 'bg-primary',
        'spam': 'bg-danger',
        'other': 'bg-secondary'
    };
    return classes[category] || classes['other'];
}

// Get importance class
function getImportanceClass(importance) {
    if (importance >= 0.7) return 'border-danger';
    if (importance >= 0.4) return 'border-warning';
    return 'border-success';
}