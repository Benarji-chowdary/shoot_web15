// Modal Elements
const bookingModal = document.getElementById('bookingModal');
const weddingModal = document.getElementById('weddingModal');

// Form Elements
const selectedPackageText = document.getElementById('selectedPackageText');
const formPackageName = document.getElementById('formPackageName');

// Open main Booking Form Modal
function openBookingModal(packageName) {
    if (packageName) {
        selectedPackageText.textContent = packageName;
        formPackageName.value = packageName;
    } else {
        selectedPackageText.textContent = "General Query";
        formPackageName.value = "General Query";
    }
    bookingModal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

// Close main Booking Form Modal
function closeBookingModal() {
    bookingModal.classList.remove('active');
    document.body.style.overflow = 'auto'; // Restore scrolling
}

// Open Full-Screen Wedding Modal
function openWeddingModal() {
    weddingModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close Full-Screen Wedding Modal
function closeWeddingModal() {
    weddingModal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Open booking from inside the Wedding Modal
function openBookingFromWedding(packageName) {
    // Keep wedding modal open in background or close it depending on preference
    // Here we'll close the wedding modal and open the booking modal to keep focus on form
    closeWeddingModal();

    // Add small delay for smooth transition
    setTimeout(() => {
        openBookingModal(packageName);
    }, 300);
}

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === bookingModal) {
        closeBookingModal();
    }
    if (e.target.classList.contains('wedding-modal-content')) {
        // don't close, user clicked inside content
    } else if (e.target === document.querySelector('.full-screen-modal')) {
        closeWeddingModal();
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        // Remove active class from all
        document.querySelectorAll('.nav-icon').forEach(icon => {
            icon.classList.remove('active');
        });

        // Add active class to clicked
        this.classList.add('active');

        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Form Submission Logic
const enquiryForm = document.getElementById('enquiryForm');
if (enquiryForm) {
    enquiryForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(enquiryForm);

        // Extracting form fields based on the name attributes defined in HTML
        const payload = {
            package: formData.get('Package') || 'None Selected',
            name: formData.get('Full Name'),
            phone: formData.get('Country Code') + ' ' + formData.get('Phone Number'),
            email: formData.get('Email'),
            occasion: formData.get('Occasion'),
            city: formData.get('City'),
            date: formData.get('Date')
        };

        const submitBtn = enquiryForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/book', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (response.ok) {
                alert('Enquiry submitted successfully! We will contact you soon.');
                enquiryForm.reset();
                closeBookingModal();
            } else {
                alert('Error submitting enquiry: ' + (result.message || result.error));
            }
        } catch (error) {
            console.error('Submission error:', error);
            alert('A network error occurred while submitting the enquiry. Please ensure the backend is running.');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}
