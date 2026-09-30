document.addEventListener("DOMContentLoaded", function() {
    // Smooth scrolling untuk link navigasi
    const links = document.querySelectorAll('nav a[href^="#"], .hero-content a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            
            if(targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70, // Offset untuk tinggi header
                    behavior: "smooth"
                });
            }
        });
    });

    // Validasi sederhana form sebelum submit
    const form = document.getElementById('orderForm');
    form.addEventListener('submit', function(e) {
        const whatsapp = document.getElementById('whatsapp').value;
        const phoneRegex = /^[0-9]{10,14}$/;
        
        if (!phoneRegex.test(whatsapp)) {
            e.preventDefault();
            alert("Mohon masukkan nomor WhatsApp yang valid (hanya angka, 10-14 digit).");
        }
    });
});