// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = 'var(--text-light)';
        navbar.style.borderBottom = '1px solid var(--border-color)';
    } else {
        navbar.style.backgroundColor = 'var(--text-light)';
        navbar.style.borderBottom = 'none';
    }
});

// Login and Register buttons functionality
const loginBtn = document.querySelector('.login-btn');
const registerBtn = document.querySelector('.register-btn');



// Catalog filters
const filterBtns = document.querySelectorAll('.filter-btn');
const catalogItems = document.querySelectorAll('.catalog-item');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        filterBtns.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');

        const filter = btn.textContent.toLowerCase();

        catalogItems.forEach(item => {
            if (filter === 'все' || item.querySelector('h3').textContent.toLowerCase().includes(filter)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

// Contact form submission
const contactForm = document.querySelector('.contact-form');
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Add loading state
    const submitBtn = contactForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = 'Отправка...';
    submitBtn.disabled = true;

    // Simulate form submission
    setTimeout(() => {
        alert('Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.');
        contactForm.reset();

        // Reset button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 1500);
});

document.addEventListener('DOMContentLoaded', function() {
    // Получаем все кнопки фильтров и карточки каталога
    const filterButtons = document.querySelectorAll('.filter-btn');
    const catalogCards = document.querySelectorAll('.catalog-card');

    // Добавляем обработчик клика для каждой кнопки фильтра
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Удаляем класс active у всех кнопок
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Добавляем класс active к нажатой кнопке
            this.classList.add('active');

            const filterValue = this.getAttribute('data-filter');

            // Показываем/скрываем карточки в зависимости от фильтра
            catalogCards.forEach(card => {
                if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Обработка кнопок аренды
    const rentButtons = document.querySelectorAll('.rent-btn');
    rentButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.catalog-card');
            const equipmentName = card.querySelector('h3').textContent;
            const price = card.querySelector('.price').textContent;

            // Здесь можно добавить логику для обработки заказа
            alert(`Заказ на аренду ${equipmentName} (${price}) принят! Мы свяжемся с вами в ближайшее время.`);
        });
    });
});