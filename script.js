// Theme toggle with persistence
const themeToggle = document.getElementById('themeToggle');
const root = document.documentElement;

function applyTheme(theme) {
  root.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

const savedTheme = localStorage.getItem('theme')
  || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
applyTheme(savedTheme);

themeToggle.addEventListener('click', () => {
  const current = root.getAttribute('data-theme');
  applyTheme(current === 'dark' ? 'light' : 'dark');
});

// Waitlist form
const form = document.getElementById('waitlistForm');
const emailInput = document.getElementById('emailInput');
const formNote = document.getElementById('formNote');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const email = emailInput.value.trim();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailRegex.test(email)) {
    formNote.textContent = 'Please enter a valid email address.';
    formNote.className = 'form-note error';
    return;
  }

  // TODO: wire this up to your actual waitlist backend / email service
  // (e.g. Mailchimp, Google Sheets via Apps Script, Supabase, etc.)
  const waitlist = JSON.parse(localStorage.getItem('waitlist') || '[]');
  if (!waitlist.includes(email)) waitlist.push(email);
  localStorage.setItem('waitlist', JSON.stringify(waitlist));

  formNote.textContent = "You're on the list! We'll email you at launch.";
  formNote.className = 'form-note success';
  form.reset();
});
