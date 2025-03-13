document.addEventListener('DOMContentLoaded', function () {
    const toggleButtons = document.querySelectorAll('.toggle-subcategories');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.getAttribute('data-category-id');
            const subcategoryList = document.querySelector(`.subcategory-list[data-category-id="${categoryId}"]`);

            if (subcategoryList.style.display === 'none' || !subcategoryList.style.display) {
                subcategoryList.style.display = 'block';
                this.classList.add('active');
            } else {
                subcategoryList.style.display = 'none';
                this.classList.remove('active');
            }
        });
    });
});