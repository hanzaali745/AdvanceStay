/* ===========================
   BLOG POSTS DATA
   =========================== */

const blogPosts = [
  {
    id: 'beach-resorts',
    title: 'The Ultimate Guide to Hidden Beach Resorts',
    category: 'destinations',
    excerpt: 'Explore the most exclusive and undiscovered beach destinations around the world. Learn insider tips for finding luxury accommodations.',
    content: 'Explore the most exclusive and undiscovered beach destinations around the world. Learn insider tips for finding luxury accommodations that offer both privacy and breathtaking views. From secret coves in Croatia to pristine islands in Southeast Asia, discover where to find the world\'s most exclusive beachfront escapes. This comprehensive guide covers hidden gems, local recommendations, and insider secrets for planning your perfect beach retreat.',
    author: 'Sarah Chen',
    date: '2024-09-05',
    image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&h=600&fit=crop',
    readTime: '8 min read'
  },
  {
    id: 'tuscany-luxury',
    title: 'Luxury Stays in Tuscany',
    category: 'destinations',
    excerpt: 'Discover charming villas and boutique hotels nestled in the heart of Italy\'s wine country.',
    content: 'Discover charming villas and boutique hotels nestled in the heart of Italy\'s wine country. From historic estates to modern luxury retreats, Tuscany offers some of Europe\'s most romantic accommodation options. Learn about the best regions to stay, what to expect in terms of amenities, and how to plan the perfect Tuscan getaway with vineyard tours and local cuisine experiences.',
    author: 'Marco Rossi',
    date: '2024-08-28',
    image: 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&h=600&fit=crop',
    readTime: '6 min read'
  },
  {
    id: 'budget-travel',
    title: 'Budget Travel Hacks for 2024',
    category: 'tips',
    excerpt: 'Learn proven strategies to maximize your travel budget without sacrificing comfort and experiences.',
    content: 'Learn proven strategies to maximize your travel budget without sacrificing comfort and experiences. This guide covers booking strategies, timing tips, alternative accommodation options, and how to find authentic experiences at a fraction of the cost. Discover how to travel longer on less money while still enjoying quality accommodations and memorable experiences.',
    author: 'Alex Thompson',
    date: '2024-08-25',
    image: 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&h=600&fit=crop',
    readTime: '7 min read'
  },
  {
    id: 'tokyo-itinerary',
    title: '48-Hour Tokyo Itinerary',
    category: 'guides',
    excerpt: 'Make the most of your time in Tokyo with this carefully curated two-day adventure plan.',
    content: 'Make the most of your time in Tokyo with this carefully curated two-day adventure plan. From traditional temples to cutting-edge technology districts, this guide covers the essential must-see locations, hidden gems, and authentic dining experiences. Learn how to navigate the city efficiently and experience Tokyo like a local.',
    author: 'Yuki Tanaka',
    date: '2024-08-22',
    image: 'https://images.unsplash.com/photo-1493857671505-72967e2e2760?w=800&h=600&fit=crop',
    readTime: '10 min read'
  },
  {
    id: 'maldives-resorts',
    title: 'Five-Star Resorts in Maldives',
    category: 'reviews',
    excerpt: 'In-depth reviews of the most luxurious overwater bungalows and resort experiences.',
    content: 'In-depth reviews of the most luxurious overwater bungalows and resort experiences in the Maldives. Discover what makes these resorts worth the investment, from world-class dining to exceptional service and stunning natural beauty. This guide includes detailed reviews, pricing comparisons, and insider tips for booking.',
    author: 'Jennifer Lee',
    date: '2024-08-19',
    image: 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=800&h=600&fit=crop',
    readTime: '9 min read'
  },
  {
    id: 'barcelona-neighborhoods',
    title: 'Barcelona\'s Best Neighborhoods',
    category: 'destinations',
    excerpt: 'Explore the distinct character and attractions of Barcelona\'s most vibrant districts.',
    content: 'Explore the distinct character and attractions of Barcelona\'s most vibrant districts. From the Gothic Quarter to the bohemian Gràcia neighborhood, each area offers unique experiences, accommodations, and dining options. This guide helps you choose the best neighborhood for your stay based on your travel style and interests.',
    author: 'Carlos Garcia',
    date: '2024-08-16',
    image: 'https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&h=600&fit=crop',
    readTime: '7 min read'
  },
  {
    id: 'packing-guide',
    title: 'What to Pack for Every Climate',
    category: 'tips',
    excerpt: 'A complete packing guide that covers every destination type and season.',
    content: 'A complete packing guide that covers every destination type and season. Learn the essential items to pack for tropical climates, mountain adventures, urban exploration, and beach getaways. This comprehensive guide includes packing lists, smart packing techniques, and how to pack light while being prepared for any situation.',
    author: 'Emma Wilson',
    date: '2024-08-13',
    image: 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&h=600&fit=crop',
    readTime: '6 min read'
  },
  {
    id: 'ski-resorts',
    title: 'Top Alpine Ski Resorts',
    category: 'destinations',
    excerpt: 'Discover world-class skiing and luxury accommodations at the best alpine resorts.',
    content: 'Discover world-class skiing and luxury accommodations at the best alpine resorts across Europe and North America. This guide covers slope conditions, après-ski experiences, and luxury lodge options that cater to different skill levels and budgets.',
    author: 'Philippe Dubois',
    date: '2024-08-10',
    image: 'https://images.unsplash.com/photo-1551632786-5b2623b22e6d?w=800&h=600&fit=crop',
    readTime: '8 min read'
  },
  {
    id: 'sustainable-travel',
    title: 'Sustainable Travel Practices',
    category: 'tips',
    excerpt: 'Learn how to travel responsibly while supporting local communities and protecting the environment.',
    content: 'Learn how to travel responsibly while supporting local communities and protecting the environment. This guide covers eco-friendly accommodation options, sustainable tourism practices, and how to minimize your travel carbon footprint without compromising your experience.',
    author: 'David Green',
    date: '2024-08-07',
    image: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&h=600&fit=crop',
    readTime: '7 min read'
  },
  {
    id: 'food-tours',
    title: 'Culinary Travel Guide',
    category: 'guides',
    excerpt: 'Embark on gastronomic adventures through the world\'s most renowned food destinations.',
    content: 'Embark on gastronomic adventures through the world\'s most renowned food destinations. From street food in Bangkok to fine dining in Paris, learn how to explore destinations through food. This guide includes cooking classes, food tours, and dining recommendations for food enthusiasts.',
    author: 'Nina Rossi',
    date: '2024-08-04',
    image: 'https://images.unsplash.com/photo-1504674900787-2db66a33f05c?w=800&h=600&fit=crop',
    readTime: '9 min read'
  },
  {
    id: 'africa-safari',
    title: 'African Safari: A Wildlife Adventure',
    category: 'destinations',
    excerpt: 'Experience the majesty of African wildlife in carefully selected safari lodges and camps.',
    content: 'Experience the majesty of African wildlife in carefully selected safari lodges and camps. This comprehensive guide covers the best safari destinations, seasons for wildlife viewing, and luxury accommodation options that prioritize both comfort and conservation.',
    author: 'Amara Okonkwo',
    date: '2024-07-31',
    image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&h=600&fit=crop',
    readTime: '11 min read'
  },
  {
    id: 'luxury-cruises',
    title: 'Luxury Cruise Experiences',
    category: 'reviews',
    excerpt: 'Explore the world\'s finest cruise lines and their exclusive itineraries.',
    content: 'Explore the world\'s finest cruise lines and their exclusive itineraries. From Mediterranean voyages to Antarctic expeditions, this guide reviews luxury cruise options with premium dining, world-class entertainment, and exceptional service.',
    author: 'Richard Sterling',
    date: '2024-07-28',
    image: 'https://images.unsplash.com/photo-1517457373614-b7152f800fd1?w=800&h=600&fit=crop',
    readTime: '8 min read'
  }
];

/* ===========================
   STATE MANAGEMENT
   =========================== */

let currentFilter = 'all';
let currentPage = 1;
const postsPerPage = 6;
let filteredPosts = [...blogPosts];

/* ===========================
   INITIALIZATION
   =========================== */

document.addEventListener('DOMContentLoaded', () => {
  renderPosts();
  setupEventListeners();
});

/* ===========================
   EVENT LISTENERS
   =========================== */

function setupEventListeners() {
  const mobileToggle = document.getElementById('mobileToggle');
  const navLinks = document.querySelector('.nav-links');

  // Mobile menu toggle
  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }

  // Close mobile menu when a link is clicked
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('show');
    });
  });

  // Close modal when clicking outside
  document.getElementById('postModal').addEventListener('click', (e) => {
    if (e.target.id === 'postModal') {
      closeModal();
    }
  });

  // Close modal with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  });

  // Search functionality
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        performSearch();
      }
    });
  }
}

/* ===========================
   POST FILTERING & SEARCH
   =========================== */

function filterPosts(category, event) {
  currentFilter = category;
  currentPage = 1;

  // Update active filter tag
  document.querySelectorAll('.filter-tag').forEach(tag => {
    tag.classList.remove('active');
  });
  if (event) {
    event.target.classList.add('active');
  }

  // Filter posts
  if (category === 'all') {
    filteredPosts = [...blogPosts];
  } else {
    filteredPosts = blogPosts.filter(post => post.category === category);
  }

  // Clear search input
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.value = '';
  }

  renderPosts();
}

function performSearch() {
  const searchInput = document.getElementById('searchInput');
  const searchTerm = searchInput.value.toLowerCase().trim();

  if (!searchTerm) {
    filterPosts('all');
    return;
  }

  filteredPosts = blogPosts.filter(post =>
    post.title.toLowerCase().includes(searchTerm) ||
    post.excerpt.toLowerCase().includes(searchTerm) ||
    post.author.toLowerCase().includes(searchTerm) ||
    post.category.toLowerCase().includes(searchTerm)
  );

  currentPage = 1;
  currentFilter = 'search';

  // Reset active filter tags
  document.querySelectorAll('.filter-tag').forEach(tag => {
    tag.classList.remove('active');
  });

  renderPosts();
}

/* ===========================
   RENDERING POSTS
   =========================== */

function renderPosts() {
  const postsGrid = document.getElementById('postsGrid');
  postsGrid.innerHTML = '';

  // Calculate pagination
  const totalPages = Math.ceil(filteredPosts.length / postsPerPage);
  const startIndex = (currentPage - 1) * postsPerPage;
  const endIndex = startIndex + postsPerPage;
  const postsToDisplay = filteredPosts.slice(startIndex, endIndex);

  // Render posts
  if (postsToDisplay.length === 0) {
    postsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: #64748B;">No posts found. Try a different search or filter.</p>';
  } else {
    postsToDisplay.forEach(post => {
      const postCard = createPostCard(post);
      postsGrid.appendChild(postCard);
    });
  }

  // Render pagination
  renderPagination(totalPages);
}

function createPostCard(post) {
  const article = document.createElement('article');
  article.className = 'post-card';
  article.innerHTML = `
    <picture class="post-image">
      <img src="${post.image}" alt="${post.title}">
    </picture>
    <div class="post-content">
      <span class="post-category">${post.category}</span>
      <h3 class="post-title">${post.title}</h3>
      <p class="post-excerpt">${post.excerpt}</p>
      <span class="post-date">${formatDate(post.date)} • ${post.readTime}</span>
    </div>
  `;

  article.addEventListener('click', () => {
    openPostModal(post);
  });

  article.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      openPostModal(post);
    }
  });

  article.setAttribute('tabindex', '0');
  article.setAttribute('role', 'button');

  return article;
}

/* ===========================
   PAGINATION
   =========================== */

function renderPagination(totalPages) {
  const pagination = document.getElementById('pagination');
  pagination.innerHTML = '';

  if (totalPages <= 1) return;

  // Previous button
  const prevBtn = document.createElement('button');
  prevBtn.textContent = '← Previous';
  prevBtn.disabled = currentPage === 1;
  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderPosts();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
  pagination.appendChild(prevBtn);

  // Page numbers
  for (let i = 1; i <= totalPages; i++) {
    const pageBtn = document.createElement('button');
    pageBtn.textContent = i;
    if (i === currentPage) {
      pageBtn.classList.add('active');
    }
    pageBtn.addEventListener('click', () => {
      currentPage = i;
      renderPosts();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    pagination.appendChild(pageBtn);
  }

  // Next button
  const nextBtn = document.createElement('button');
  nextBtn.textContent = 'Next →';
  nextBtn.disabled = currentPage === totalPages;
  nextBtn.addEventListener('click', () => {
    if (currentPage < totalPages) {
      currentPage++;
      renderPosts();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
  pagination.appendChild(nextBtn);
}

/* ===========================
   MODAL FUNCTIONALITY
   =========================== */

function openPostModal(post) {
  const modal = document.getElementById('postModal');
  const postDetail = document.getElementById('postDetail');

  postDetail.innerHTML = `
    <button class="modal-close" onclick="closeModal()" aria-label="Close modal">&times;</button>
    <article>
      <h1>${post.title}</h1>
      <div class="post-detail-meta">
        <span>By ${post.author}</span>
        <span>•</span>
        <span>${formatDate(post.date)}</span>
        <span>•</span>
        <span>${post.readTime}</span>
      </div>
      <picture class="post-detail-image">
        <img src="${post.image}" alt="${post.title}">
      </picture>
      <div class="post-detail-content">
        <p>${post.content}</p>
        <p>This article covers important insights about traveling to this destination. Whether you\'re a first-time visitor or a seasoned traveler, you\'ll find valuable information to enhance your next trip.</p>
        <p><strong>Key Takeaways:</strong></p>
        <p>• Plan your trip during the optimal season for your destination<br>
        • Research local customs and travel requirements<br>
        • Book accommodations in advance for better rates<br>
        • Allow flexibility in your itinerary for spontaneous adventures<br>
        • Connect with local guides for authentic experiences</p>
      </div>
    </article>
  `;

  modal.classList.add('show');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  const modal = document.getElementById('postModal');
  modal.classList.remove('show');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = 'auto';
}

/* ===========================
   UTILITY FUNCTIONS
   =========================== */

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' });
  }
}

function navigateToBlog(postId) {
  const post = blogPosts.find(p => p.id === postId);
  if (post) {
    openPostModal(post);
  }
}

/* ===========================
   NEWSLETTER SIGNUP
   =========================== */

function handleNewsletterSignup(event) {
  event.preventDefault();

  const form = event.target;
  const email = form.querySelector('input[type="email"]').value;

  // Simulate form submission
  console.log('Newsletter signup:', email);

  // Show success message
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalText = submitBtn.textContent;
  submitBtn.textContent = '✓ Subscribed!';
  submitBtn.disabled = true;

  // Reset form after 2 seconds
  setTimeout(() => {
    form.reset();
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
  }, 2000);
}

/* ===========================
   PROGRESSIVE ENHANCEMENT
   =========================== */

// Lazy load images
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
        }
        observer.unobserve(img);
      }
    });
  });

  document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href !== '#' && document.querySelector(href)) {
      e.preventDefault();
      document.querySelector(href).scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

// Print debug info
console.log(`📝 AdvanceStay Blog loaded with ${blogPosts.length} posts`);
