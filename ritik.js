document.addEventListener("DOMContentLoaded", () => {
  // Tab functionality
  const tabs = document.querySelectorAll(".tab-btn")

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      // Remove active class from all tabs
      tabs.forEach((t) => t.classList.remove("active"))
      // Add active class to clicked tab
      tab.classList.add("active")
    })
  })

  // Smooth scroll for navigation links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
      })
    })
  })

  // Service card hover effects
  const serviceCards = document.querySelectorAll(".service-card")
  serviceCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-5px)"
    })

    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0)"
    })
  })

  // Mobile menu toggle (if needed)
  const createMobileMenu = () => {
    if (window.innerWidth <= 768) {
      const nav = document.querySelector(".main-nav")
      const ul = nav.querySelector("ul")

      if (!document.querySelector(".mobile-menu-btn")) {
        const menuBtn = document.createElement("button")
        menuBtn.classList.add("mobile-menu-btn")
        menuBtn.innerHTML = "☰"
        nav.insertBefore(menuBtn, ul)

        menuBtn.addEventListener("click", () => {
          ul.classList.toggle("show")
        })
      }
    }
  }

  // Initialize mobile menu
  createMobileMenu()

  // Update on resize
  window.addEventListener("resize", createMobileMenu)

  // Language selector functionality
  const languageSelect = document.getElementById("language-select")
  if (languageSelect) {
    languageSelect.addEventListener("change", function () {
      // Here you would implement language change functionality
      console.log("Language changed to: " + this.value)
      // For demonstration purposes only
      alert("Language changed to: " + this.options[this.selectedIndex].text)
    })
  }
})

function findNearbyHospitals() {
  const query = "hospitals near me"
  window.open(`https://www.google.com/maps/search/${encodeURIComponent(query)}`)
}

// Open the modal
function openDiseaseModal() {
  const modal = document.getElementById("diseaseModal")
  if (modal) {
    modal.style.display = "block"
  }
}

// Close the modal
function closeDiseaseModal() {
  const modal = document.getElementById("diseaseModal")
  if (modal) {
    modal.style.display = "none"
  }
}

// Handle the disease input
function submitDisease() {
  const diseaseInput = document.getElementById("diseaseInput")
  if (diseaseInput) {
    const disease = diseaseInput.value.trim()
    if (disease) {
      const searchQuery = `doctors for ${encodeURIComponent(disease)} near me`
      window.open(`https://www.google.com/search?q=${searchQuery}`, "_blank")
      closeDiseaseModal()
    } else {
      alert("Please enter a disease.")
    }
  }
}

// Close modal when clicking outside of it
window.onclick = (event) => {
  const modal = document.getElementById("diseaseModal")
  if (event.target === modal) {
    closeDiseaseModal()
  }
}

function findNearbyHospitals() {
  const query = "hospitals near me"
  window.open(`https://www.google.com/maps/search/${encodeURIComponent(query)}`)
}

// buy medicine

function buymed() {
  const query = "buy medicines"
  window.open(`https://www.1mg.com/`)
}

