document.addEventListener('DOMContentLoaded', function() {
    // Confirm before deleting announcement
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('آیا مطمئن هستید که می‌خواهید این اطلاعیه را حذف کنید؟')) {
                e.preventDefault();
            }
        });
    });
    
    // Add any additional JavaScript functionality here
});
