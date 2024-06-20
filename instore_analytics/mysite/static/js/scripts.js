// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.button');

    buttons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#0056b3';
        });

        button.addEventListener('mouseout', function() {
            this.style.backgroundColor = '#007BFF';
        });
    });
});
