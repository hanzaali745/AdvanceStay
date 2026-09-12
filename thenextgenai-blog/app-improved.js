/* ===========================
   BLOG POSTS DATA - ENHANCED
   =========================== */

const blogPosts = [
  {
    id: 'understanding-llms',
    title: 'Understanding Large Language Models',
    category: 'research',
    excerpt: 'A deep dive into how LLMs work, their capabilities and limitations, and what\'s really happening under the hood.',
    content: 'Large Language Models have revolutionized AI, but understanding how they work is crucial. This comprehensive guide covers transformers, attention mechanisms, tokenization, and the mathematical foundations. We explore the limitations of LLMs, including hallucinations and reasoning gaps, and discuss what researchers are doing to address these challenges. Learn the fundamentals that power GPT, Claude, and other state-of-the-art language models.',
    author: 'Dr. Alex Rivera',
    authorTitle: 'AI Researcher',
    authorAffiliation: 'MIT',
    authorInitials: 'AR',
    date: '2024-09-10',
    image: 'https://images.unsplash.com/photo-1677442d019cecf8fbf1a3a5b3a2a6f?w=800&h=600&fit=crop',
    readTime: '12 min',
    confidence: 98,
    difficulty: 'Intermediate'
  },
  {
    id: 'building-first-ml-model',
    title: 'Building Your First ML Model',
    category: 'tutorials',
    excerpt: 'Step-by-step guide to creating and training a machine learning model using Python.',
    content: 'Learn how to build your first machine learning model from scratch. We cover data preparation, feature engineering, model selection, training, and evaluation. Using Python libraries like scikit-learn and TensorFlow, you\'ll build a complete end-to-end ML pipeline. This tutorial includes practical examples and best practices for production-ready code. Perfect for beginners looking to transition from theory to practice.',
    author: 'Sarah Chen',
    authorTitle: 'ML Engineer',
    authorAffiliation: 'Google Brain',
    authorInitials: 'SC',
    date: '2024-09-08',
    image: 'https://images.unsplash.com/photo-1516321318423-f06f70db4397?w=800&h=600&fit=crop',
    readTime: '15 min',
    confidence: 92,
    difficulty: 'Beginner'
  },
  {
    id: 'transformers-latest',
    title: 'Latest Developments in Transformers',
    category: 'research',
    excerpt: 'Analysis of recent breakthroughs in transformer architecture and their implications.',
    content: 'The transformer architecture continues to evolve rapidly. We analyze recent papers on Vision Transformers, mixture-of-experts models, and efficient attention mechanisms. Understand how these innovations improve performance, reduce computational costs, and enable new applications across NLP, computer vision, and multimodal learning. Stay current with cutting-edge research.',
    author: 'Dr. James Park',
    authorTitle: 'Research Scientist',
    authorAffiliation: 'DeepMind',
    authorInitials: 'JP',
    date: '2024-09-05',
    image: 'https://images.unsplash.com/photo-1620712014307-1e91badde956?w=800&h=600&fit=crop',
    readTime: '10 min',
    confidence: 95,
    difficulty: 'Advanced'
  },
  {
    id: 'ai-ethics',
    title: 'AI Ethics Fundamentals',
    category: 'guides',
    excerpt: 'Understanding bias, fairness, and responsible AI development principles.',
    content: 'Building ethical AI systems requires understanding bias at every stage. This guide covers data bias, algorithmic bias, fairness metrics, and bias mitigation strategies. Learn how to build transparent, interpretable, and fair AI systems. We discuss real-world examples and practical approaches to responsible AI development that matter in production systems.',
    author: 'Dr. Maria Santos',
    authorTitle: 'AI Ethics Lead',
    authorAffiliation: 'Anthropic',
    authorInitials: 'MS',
    date: '2024-09-01',
    image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop',
    readTime: '9 min',
    confidence: 88,
    difficulty: 'Intermediate'
  },
  {
    id: 'fine-tuning-vs-rag',
    title: 'Fine-Tuning vs RAG: When to Use Each',
    category: 'analysis',
    excerpt: 'Comprehensive comparison of fine-tuning and retrieval-augmented generation for your use case.',
    content: 'When should you fine-tune a model vs use RAG? We break down the tradeoffs, costs, performance implications, and implementation complexity of each approach. This analysis helps you make informed decisions based on your specific requirements, data availability, and computational resources. Includes cost calculators and real-world case studies.',
    author: 'Alex Thompson',
    authorTitle: 'ML Architect',
    authorAffiliation: 'OpenAI',
    authorInitials: 'AT',
    date: '2024-08-29',
    image: 'https://images.unsplash.com/photo-1580894894513-541231154e45?w=800&h=600&fit=crop',
    readTime: '11 min',
    confidence: 90,
    difficulty: 'Intermediate'
  },
  {
    id: 'computer-vision-basics',
    title: 'Computer Vision Fundamentals',
    category: 'tutorials',
    excerpt: 'Learn image processing, feature extraction, and deep learning for vision tasks.',
    content: 'Master computer vision from the ground up. This tutorial covers image fundamentals, convolutions, CNNs, and modern architectures like ResNets and Vision Transformers. Build practical applications including image classification, object detection, and segmentation using PyTorch and OpenCV. Hands-on code examples included.',
    author: 'Lisa Wang',
    authorTitle: 'Computer Vision Engineer',
    authorAffiliation: 'Tesla',
    authorInitials: 'LW',
    date: '2024-08-26',
    image: 'https://images.unsplash.com/photo-1609034227505-5876f6aa4e90?w=800&h=600&fit=crop',
    readTime: '13 min',
    confidence: 89,
    difficulty: 'Intermediate'
  },
  {
    id: 'nlp-pipeline',
    title: 'Building an NLP Pipeline from Scratch',
    category: 'tutorials',
    excerpt: 'Complete guide to creating production-ready NLP systems with preprocessing to inference.',
    content: 'Build a complete NLP pipeline from data collection to production deployment. We cover tokenization, embeddings, model training, evaluation, and serving. Learn best practices for handling edge cases, monitoring performance, and maintaining quality in production NLP systems. Real-world optimizations for latency and throughput.',
    author: 'Dr. Kumar Sharma',
    authorTitle: 'NLP Specialist',
    authorAffiliation: 'Stanford',
    authorInitials: 'KS',
    date: '2024-08-23',
    image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad576?w=800&h=600&fit=crop',
    readTime: '14 min',
    confidence: 91,
    difficulty: 'Advanced'
  },
  {
    id: 'prompt-engineering',
    title: 'Advanced Prompt Engineering Techniques',
    category: 'guides',
    excerpt: 'Master the art of crafting effective prompts for maximum model performance.',
    content: 'Prompt engineering is both art and science. This guide covers prompt structure, few-shot learning, chain-of-thought reasoning, and retrieval-augmented prompting. Learn techniques to improve accuracy, reduce hallucinations, and get consistent results from language models. Includes templates and evaluation frameworks.',
    author: 'Emma Rodriguez',
    authorTitle: 'Prompt Engineer',
    authorAffiliation: 'Hugging Face',
    authorInitials: 'ER',
    date: '2024-08-20',
    image: 'https://images.unsplash.com/photo-1531746790731-6c087fecd65b?w=800&h=600&fit=crop',
    readTime: '8 min',
    confidence: 85,
    difficulty: 'Beginner'
  },
  {
    id: 'reinforcement-learning',
    title: 'Introduction to Reinforcement Learning',
    category: 'guides',
    excerpt: 'Learn how agents learn through interaction: MDPs, Q-learning, policy gradients, and more.',
    content: 'Discover reinforcement learning fundamentals. We explain Markov Decision Processes, value functions, policy gradients, and deep Q-learning. Build agents that learn optimal behavior through trial and error, with applications from game playing to robotics. Implemented examples using OpenAI Gym and PyTorch.',
    author: 'Dr. Michael Zhang',
    authorTitle: 'Reinforcement Learning Researcher',
    authorAffiliation: 'UC Berkeley',
    authorInitials: 'MZ',
    date: '2024-08-17',
    image: 'https://images.unsplash.com/photo-1677442d019cecf8fbf1a3a5b3a2a6f?w=800&h=600&fit=crop',
    readTime: '12 min',
    confidence: 87,
    difficulty: 'Advanced'
  },
  {
    id: 'model-optimization',
    title: 'Model Optimization Techniques',
    category: 'analysis',
    excerpt: 'Quantization, pruning, distillation, and other methods to improve inference performance.',
    content: 'Deploy models faster and cheaper. We explore quantization strategies (int8, fp16), knowledge distillation for model compression, and pruning techniques. Learn how to maintain accuracy while reducing model size and latency for production deployment. Benchmarks and comparison tables included.',
    author: 'David Kim',
    authorTitle: 'Performance Engineer',
    authorAffiliation: 'NVIDIA',
    authorInitials: 'DK',
    date: '2024-08-14',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop',
    readTime: '10 min',
    confidence: 86,
    difficulty: 'Advanced'
  },
  {
    id: 'multimodal-ai',
    title: 'Multimodal AI: Text, Vision & Beyond',
    category: 'research',
    excerpt: 'Understanding models that process multiple types of data simultaneously.',
    content: 'Multimodal models like CLIP and GPT-4V are reshaping AI. Learn how these models combine text, images, and other modalities. Explore applications in visual question answering, image captioning, and cross-modal retrieval. Understand the architectures and training techniques behind state-of-the-art multimodal systems.',
    author: 'Dr. Priya Patel',
    authorTitle: 'Multimodal Research Lead',
    authorAffiliation: 'Meta AI',
    authorInitials: 'PP',
    date: '2024-08-11',
    image: 'https://images.unsplash.com/photo-1677442d019cecf8fbf1a3a5b3a2a6f?w=800&h=600&fit=crop',
    readTime: '11 min',
    confidence: 93,
    difficulty: 'Advanced'
  },
  {
    id: 'ml-deployment',
    title: 'Deploying ML Models to Production',
    category: 'guides',
    excerpt: 'Containerization, monitoring, scaling, and maintaining ML systems in production.',
    content: 'Moving from notebook to production requires new skills. This guide covers containerization with Docker, serving with FastAPI, monitoring performance, handling data drift, and scaling to handle production traffic. Learn DevOps practices specific to ML systems with real-world examples.',
    author: 'Tarek Hassan',
    authorTitle: 'MLOps Engineer',
    authorAffiliation: 'Amazon',
    authorInitials: 'TH',
    date: '2024-08-08',
    image: 'https://images.unsplash.com/photo-1633356122544-f134324ef6db?w=800&h=600&fit=crop',
    readTime: '13 min',
    confidence: 89,
    difficulty: 'Advanced'
  }
];

/* ===========================
   PAGINATION
   =========================== */

const ARTICLES_PER_PAGE = 6;
let currentPage = 1;
let filteredPosts = [...blogPosts];

/* ===========================
   UTILITY FUNCTIONS
   =========================== */

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
}

function navigateToBlog(postId) {
  const post = blogPosts.find(p => p.id === postId);
  if (post) {
    showArticleModal(post);
  }
}

/* ===========================
   FILTER & SEARCH
   =========================== */

function filterPosts(category, event) {
  if (event) event.preventDefault();

  const buttons = document.querySelectorAll('.filter-tag');
  buttons.forEach(btn => btn.classList.remove('active'));

  if (event) {
    event.target.classList.add('active');
  } else {
    document.querySelector(`[data-filter="${category}"]`)?.classList.add('active');
  }

  currentPage = 1;

  if (category === 'all') {
    filteredPosts = [...blogPosts];
  } else {
    filteredPosts = blogPosts.filter(post => post.category === category);
  }

  renderArticles();
  renderPagination();
}

function performSearch() {
  const searchInput = document.getElementById('search-field');
  const query = searchInput.value.toLowerCase().trim();

  if (!query) {
    filteredPosts = [...blogPosts];
  } else {
    filteredPosts = blogPosts.filter(post =>
      post.title.toLowerCase().includes(query) ||
      post.excerpt.toLowerCase().includes(query) ||
      post.author.toLowerCase().includes(query) ||
      post.content.toLowerCase().includes(query)
    );
  }

  currentPage = 1;
  renderArticles();
  renderPagination();
}

/* ===========================
   RENDER ARTICLES
   =========================== */

function renderArticles() {
  const grid = document.getElementById('articlesGrid');
  if (!grid) return;

  grid.innerHTML = '';

  const start = (currentPage - 1) * ARTICLES_PER_PAGE;
  const end = start + ARTICLES_PER_PAGE;
  const paginatedPosts = filteredPosts.slice(start, end);

  if (paginatedPosts.length === 0) {
    grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--color-text-muted); padding: var(--spacing-3xl);">No articles found. Try adjusting your filters or search.</p>';
    return;
  }

  paginatedPosts.forEach(post => {
    const card = createArticleCard(post);
    grid.appendChild(card);
  });
}

function createArticleCard(post) {
  const card = document.createElement('article');
  card.className = 'article-card';
  card.onclick = () => showArticleModal(post);

  const difficultyColor = {
    'Beginner': '#00d9ff',
    'Intermediate': '#6b5b95',
    'Advanced': '#ff6b35'
  };

  card.innerHTML = `
    <div class="article-image">
      <img src="${post.image}" alt="${post.title}">
    </div>
    <div class="article-body">
      <div class="article-meta">
        <span class="category-badge" data-category="${post.category}">${post.category}</span>
        <span style="color: ${difficultyColor[post.difficulty] || '#cbd5e1'}; font-size: 11px; font-weight: 600;">${post.difficulty}</span>
        <span style="color: #00d9ff; font-family: var(--font-mono); font-size: 11px;">${post.confidence}%</span>
      </div>
      <h3 class="article-title">${post.title}</h3>
      <p class="article-excerpt">${post.excerpt}</p>
      <div class="article-footer">
        <span class="article-author">${post.author}</span>
        <span class="article-date">${post.readTime}</span>
      </div>
    </div>
  `;

  return card;
}

/* ===========================
   PAGINATION
   =========================== */

function renderPagination() {
  const paginationContainer = document.getElementById('pagination');
  if (!paginationContainer) return;

  paginationContainer.innerHTML = '';

  const totalPages = Math.ceil(filteredPosts.length / ARTICLES_PER_PAGE);

  if (totalPages <= 1) return;

  const prevBtn = document.createElement('button');
  prevBtn.className = 'pagination-btn';
  prevBtn.textContent = '← Previous';
  prevBtn.disabled = currentPage === 1;
  prevBtn.onclick = () => {
    if (currentPage > 1) {
      currentPage--;
      renderArticles();
      renderPagination();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };
  paginationContainer.appendChild(prevBtn);

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement('button');
    btn.className = `pagination-btn ${i === currentPage ? 'active' : ''}`;
    btn.textContent = i;
    btn.onclick = () => {
      currentPage = i;
      renderArticles();
      renderPagination();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    paginationContainer.appendChild(btn);
  }

  const nextBtn = document.createElement('button');
  nextBtn.className = 'pagination-btn';
  nextBtn.textContent = 'Next →';
  nextBtn.disabled = currentPage === totalPages;
  nextBtn.onclick = () => {
    if (currentPage < totalPages) {
      currentPage++;
      renderArticles();
      renderPagination();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };
  paginationContainer.appendChild(nextBtn);
}

/* ===========================
   MODAL
   =========================== */

function showArticleModal(post) {
  const modal = document.getElementById('articleModal');
  const content = document.getElementById('articleContent');

  if (!modal || !content) return;

  const fullContent = `
    <h2>${post.title}</h2>
    <div style="display: flex; gap: var(--spacing-md); margin: var(--spacing-lg) 0; padding-bottom: var(--spacing-lg); border-bottom: 1px solid var(--color-border);">
      <div>
        <span class="category-badge" data-category="${post.category}">${post.category}</span>
      </div>
      <div style="font-size: 12px; color: var(--color-text-muted);">
        <strong>${formatDate(post.date)}</strong> • ${post.readTime}
      </div>
    </div>
    <div style="display: flex; align-items: center; gap: var(--spacing-md); margin: var(--spacing-xl) 0; padding: var(--spacing-lg); background: rgba(26, 36, 68, 0.3); border-radius: var(--radius-md);">
      <div style="width: 48px; height: 48px; border-radius: 50%; background: var(--color-cyan); color: var(--color-navy-dark); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px;">
        ${post.authorInitials}
      </div>
      <div>
        <div style="font-weight: 600; color: var(--color-text-primary);">${post.author}</div>
        <div style="font-size: 13px; color: var(--color-text-muted);">${post.authorTitle} • ${post.authorAffiliation}</div>
      </div>
    </div>
    <p>${post.content}</p>
  `;

  content.innerHTML = fullContent;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  const modal = document.getElementById('articleModal');
  if (modal) {
    modal.classList.remove('open');
    document.body.style.overflow = 'auto';
  }
}

/* ===========================
   NEWSLETTER
   =========================== */

function handleNewsletterSignup(event) {
  event.preventDefault();
  const form = event.target;
  const email = form.querySelector('input[type="email"]').value;

  if (email) {
    alert(`Thank you for subscribing! We'll send verified AI insights to ${email}`);
    form.reset();
  }
}

/* ===========================
   MOBILE MENU
   =========================== */

function setupMobileMenu() {
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  if (!navToggle || !navMenu) return;

  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('open');
    const isOpen = navMenu.classList.contains('open');
    navToggle.setAttribute('aria-expanded', isOpen);
  });

  navMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ===========================
   MODAL CLOSE
   =========================== */

function setupModalClose() {
  const modal = document.getElementById('articleModal');
  if (!modal) return;

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

/* ===========================
   INITIALIZATION
   =========================== */

document.addEventListener('DOMContentLoaded', () => {
  renderArticles();
  renderPagination();
  setupMobileMenu();
  setupModalClose();
});
