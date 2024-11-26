
// Function to add staggered card visibility
document.addEventListener('DOMContentLoaded', () => {
  const feedbackCards = document.querySelectorAll('.feedback-card');
  feedbackCards.forEach((card, index) => {
      // Set a delay to make them appear one after another
      setTimeout(() => {
          card.classList.add('visible');
      }, index * 500); // Delay by 500ms per card
  });
});

// Function to reset interactivity (optional)
// Remove moveCard and resetCardPosition functionality if unnecessary
