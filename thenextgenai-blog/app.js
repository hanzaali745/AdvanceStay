/* ===========================
   AI BLOG POSTS DATA
   =========================== */

const blogPosts = [
  {
    id: 'understanding-llms',
    title: 'Understanding Large Language Models',
    category: 'research',
    excerpt: 'A deep dive into how LLMs work, their capabilities and limitations, and what\'s really happening under the hood.',
    content: 'Large Language Models have revolutionized AI, but understanding how they work is crucial. This comprehensive guide covers transformers, attention mechanisms, tokenization, and the mathematical foundations. We explore the limitations of LLMs, including hallucinations and reasoning gaps, and discuss what researchers are doing to address these challenges.',
    author: 'Dr. Alex Rivera',
    date: '2024-09-10',
    image: 'https://images.unsplash.com/photo-1677442d019cecf8fbf1a3a5b3a2a6f?w=800&h=600&fit=crop',
    readTime: '12 min read',
    confidence: 98
  },
  {
    id: 'building-first-ml-model',
    title: 'Building Your First ML Model',
    category: 'tutorials',
    excerpt: 'Step-by-step guide to creating and training a machine learning model using Python.',
    content: 'Learn how to build your first machine learning model from scratch. We cover data preparation, feature engineering, model selection, training, and evaluation. Using Python libraries like scikit-learn and TensorFlow, you\'ll build a complete end-to-end ML pipeline. This tutorial includes practical examples and best practices for production-ready code.',
    author: 'Sarah Chen',
    date: '2024-09-08',
    image: 'https://images.unsplash.com/photo-1516321318423-f06f70db4397?w=800&h=600&fit=crop',
    readTime: '15 min read',
    confidence: 92
  },
  {
    id: 'transformers-latest',
    title: 'Latest Developments in Transformers',
    category: 'research',
    excerpt: 'Analysis of recent breakthroughs in transformer architecture and their implications.',
    content: 'The transformer architecture continues to evolve rapidly. We analyze recent papers on Vision Transformers, mixture-of-experts models, and efficient attention mechanisms. Understand how these innovations improve performance, reduce computational costs, and enable new applications across NLP, computer vision, and multimodal learning.',
    author: 'Dr. James Park',
    date: '2024-09-05',
    image: 'https://images.unsplash.com/photo-1620712014307-1e91badde956?w=800&h=600&fit=crop',
    readTime: '10 min read',
    confidence: 95
  },
  {
    id: 'ai-ethics',
    title: 'AI Ethics Fundamentals',
    category: 'guides',
    excerpt: 'Understanding bias, fairness, and responsible AI development principles.',
    content: 'Building ethical AI systems requires understanding bias at every stage. This guide covers data bias, algorithmic bias, fairness metrics, and bias mitigation strategies. Learn how to build transparent, interpretable, and fair AI systems. We discuss real-world examples and practical approaches to responsible AI development.',
    author: 'Dr. Maria Santos',
    date: '2024-09-01',
    image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop',
    readTime: '9 min read',
    confidence: 88
  },
  {
    id: 'fine-tuning-vs-rag',
    title: 'Fine-Tuning vs RAG: When to Use Each',
    category: 'analysis',
    excerpt: 'Comprehensive comparison of fine-tuning and retrieval-augmented generation for your use case.',
    content: 'When should you fine-tune a model vs use RAG? We break down the tradeoffs, costs, performance implications, and implementation complexity of each approach. This analysis helps you make informed decisions based on your specific requirements, data availability, and computational resources.',
    author: 'Alex Thompson',
    date: '2024-08-29',
    image: 'https://images.unsplash.com/photo-1580894894513-541231154e45?w=800&h=600&fit=crop',
    readTime: '11 min read',
    confidence: 90
  },
  {
    id: 'computer-vision-basics',
    title: 'Computer Vision Fundamentals',
    category: 'tutorials',
    excerpt: 'Learn image processing, feature extraction, and deep learning for vision tasks.',
    content: 'Master computer vision from the ground up. This tutorial covers image fundamentals, convolutions, CNNs, and modern architectures like ResNets and Vision Transformers. Build practical applications including image classification, object detection, and segmentation using PyTorch and OpenCV.',
    author: 'Lisa Wang',
    date: '2024-08-26',
    image: 'https://images.unsplash.com/photo-1609034227505-5876f6aa4e90?w=800&h=600&fit=crop',
    readTime: '13 min read',
    confidence: 89
  },
  {
    id: 'nlp-pipeline',
    title: 'Building an NLP Pipeline from Scratch',
    category: 'tutorials',
    excerpt: 'Complete guide to creating production-ready NLP systems with preprocessing to inference.',
    content: 'Build a complete NLP pipeline from data collection to production deployment. We cover tokenization, embeddings, model training, evaluation, and serving. Learn best practices for handling edge cases, monitoring performance, and maintaining quality in production NLP systems.',
    author: 'Dr. Kumar Sharma',
    date: '2024-08-23',
    image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad576?w=800&h=600&fit=crop',
    readTime: '14 min read',
    confidence: 91
  },
  {
    id: 'prompt-engineering',
    title: 'Advanced Prompt Engineering Techniques',
    category: 'guides',
    excerpt: 'Master the art of crafting effective prompts for maximum model performance.',
    content: 'Prompt engineering is both art and science. This guide covers prompt structure, few-shot learning, chain-of-thought reasoning, and retrieval-augmented prompting. Learn techniques to improve accuracy, reduce hallucinations, and get consistent results from language models.',
    author: 'Emma Rodriguez',
    date: '2024-08-20',
    image: 'https://images.unsplash.com/photo-1531746790731-6c087fecd65b?w=800&h=600&fit=crop',
    readTime: '8 min read',
    confidence: 85
  },
  {
    id: 'reinforcement-learning',
    title: 'Introduction to Reinforcement Learning',
    category: 'guides',
    excerpt: 'Learn how agents learn through interaction: MDPs, Q-learning, policy gradients, and more.',
    content: 'Discover reinforcement learning fundamentals. We explain Markov Decision Processes, value functions, policy gradients, and deep Q-learning. Build agents that learn optimal behavior through trial and error, with applications from game playing to robotics.',
    author: 'Dr. Michael Zhang',
    date: '2024-08-17',
    image: 'https://images.unsplash.com/photo-1677442d019cecf8fbf1a3a5b3a2a6f?w=800&h=600&fit=crop',
    readTime: '12 min read',
    confidence: 87
  },
  {
    id: 'model-optimization',
    title: 'Model Optimization Techniques',
    category: 'analysis',
    excerpt: 'Quantization, pruning, distillation, and other methods to improve inference performance.',
    content: 'Deploy models faster and cheaper. We explore quantization strategies (int8, fp16), knowledge distillation for model compression, and pruning techniques. Learn how to maintain accuracy while reducing model size and latency for production deployment.',
    author: 'David Kim',
    date: '2024-08-14',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop',
    readTime: '10 min read',
    confidence: 86
  },
  {
    id: 'multimodal-ai',
    title: 'Multimodal AI: Text, Vision & Beyond',
    category: 'research',
    excerpt: 'Understanding models that process multiple types of data simultaneously.',
    content: 'Multimodal models like CLIP and GPT-4V are reshaping AI. Learn how these models combine text, images, and other modalities. Explore applications in visual question answering, image captioning, and cross-modal retrieval. Understand the architectures and training techniques behind state-of-the-art multimodal systems.',
    author: 'Dr. Priya Patel',
    date: '2024-08-11',
    image: 'https://images.unsplash.com/photo-1677442d019cecf8fbf1a3a5b3a2a6f?w=800&h=600&fit=crop',
    readTime: '11 min read',
    confidence: 93
  },
  {
    id: 'ml-deployment',
    title: 'Deploying ML Models to Production',
    category: 'guides',
    excerpt: 'Containerization, monitoring, scaling, and maintaining ML systems in production.',
    content: 'Moving from notebook to production requires new skills. This guide covers containerization with Docker, serving with FastAPI, monitoring performance, handling data drift, and scaling to handle production traffic. Learn DevOps practices specific to ML systems.',
    author: 'Tarek Hassan',
    date: '2024-08-08',
    image: 'https://images.unsplash.com/photo-1633356122544-f134324ef6db?w=800&h=600&fit=crop',
    readTime: '13 min read',
    confidence: 89
  },
  {
    id: 'graph-neural-networks',
    title: 'Graph Neural Networks Explained',
    category: 'tutorials',
    excerpt: 'Understanding GNNs: Graph convolutions, attention, and real-world applications.',
    content: 'Graph Neural Networks unlock patterns in connected data. Learn graph convolution networks, graph attention networks, and graph representation learning. Build applications for node classification, link prediction, and graph classification using PyTorch Geometric.',
    author: 'Dr. Julia Weber',
    date: '2024-08-05',
    image: 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=600&fit=crop',
    readTime: '12 min read',
    confidence: 91
  }
];

/* ===========================
   STATE MANAGEMENT
   =========================== */

let currentFilter = 'all';
let currentPage = 1;
const articlesPerPage = 6;
let filteredPosts = [...blogPosts];

/* ===========================
   INITIALIZATION
   =========================== */

document.addEventListener('DOMContentLoaded', () => {
  renderArticles();
  setupEventListeners();
});

/* ===========================
   EVENT LISTENERS
   =========================== */

function setupEventListeners() {
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navLinks = document.querySelector('.nav-links');

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
      const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
      mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
      navLinks.classList.toggle('show');
    });
  }

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenuBtn?.setAttribute('aria-expanded', 'false');
      navLinks?.classList.remove('show');
    });
  });

  document.getElementById('articleModal').addEventListener('click', (e) => {
    if (e.target.id === 'articleModal') {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  });

  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        performSearch();
      }
    });
  }
}

/* ===========================
   ARTICLE FILTERING & SEARCH
   =========================== */

function filterPosts(category, event) {
  currentFilter = category;
  currentPage = 1;

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  if (event) {
    event.target.classList.add('active');
  }

  if (category === 'all') {
    filteredPosts = [...blogPosts];
  } else {
    filteredPosts = blogPosts.filter(post => post.category === category);
  }

  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.value = '';
  }

  renderArticles();
}

function performSearch() {
  const searchInput = document.getElementById('search-input');
  const searchTerm = searchInput.value.toLowerCase().trim();

  if (!searchTerm) {
    filterPosts('all');
    return;
  }

  filteredPosts = blogPosts.filter(post =>
    post.title.toLowerCase().includes(searchTerm) ||
    post.excerpt.toLowerCase().includes(searchTerm) ||
    post.author.toLowerCase().includes(searchTerm) ||
    post.content.toLowerCase().includes(searchTerm)
  );

  currentPage = 1;
  currentFilter = 'search';

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
  });

  renderArticles();
}

/* ===========================
   RENDERING ARTICLES
   =========================== */

function renderArticles() {
  const articlesGrid = document.getElementById('articlesGrid');
  articlesGrid.innerHTML = '';

  const totalPages = Math.ceil(filteredPosts.length / articlesPerPage);
  const startIndex = (currentPage - 1) * articlesPerPage;
  const endIndex = startIndex + articlesPerPage;
  const articlesToDisplay = filteredPosts.slice(startIndex, endIndex);

  if (articlesToDisplay.length === 0) {
    articlesGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: #cbd5e1;">No articles found. Try a different search or filter.</div>';
  } else {
    articlesToDisplay.forEach(article => {
      const articleCard = createArticleCard(article);
      articlesGrid.appendChild(articleCard);
    });
  }

  renderPagination(totalPages);
}

function createArticleCard(article) {
  const card = document.createElement('article');
  card.className = 'article-card';
  card.setAttribute('tabindex', '0');
  card.setAttribute('role', 'button');
  card.setAttribute('aria-label', `Read article: ${article.title}`);

  card.innerHTML = `
    <div class="article-image">
      <img src="${article.image}" alt="${article.title}">
    </div>
    <div class="article-header">
      <span class="article-category">${article.category}</span>
      <h3 class="article-title">${article.title}</h3>
      <p class="article-excerpt">${article.excerpt}</p>
    </div>
    <div class="article-footer">
      <span class="article-author">${article.author}</span>
      <span class="article-read-time">${article.readTime}</span>
    </div>
  `;

  card.addEventListener('click', () => {
    openArticleModal(article);
  });

  card.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      openArticleModal(article);
    }
  });

  return card;
}

/* ===========================
   PAGINATION
   =========================== */

function renderPagination(totalPages) {
  const pagination = document.getElementById('pagination');
  pagination.innerHTML = '';

  if (totalPages <= 1) return;

  const prevBtn = document.createElement('button');
  prevBtn.className = 'pagination-btn';
  prevBtn.textContent = '← Previous';
  prevBtn.disabled = currentPage === 1;
  prevBtn.setAttribute('aria-label', 'Previous page');
  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderArticles();
      window.scrollTo({ top: document.querySelector('.articles-section').offsetTop, behavior: 'smooth' });
    }
  });
  pagination.appendChild(prevBtn);

  for (let i = 1; i <= totalPages; i++) {
    const pageBtn = document.createElement('button');
    pageBtn.className = 'pagination-btn';
    pageBtn.textContent = i;
    pageBtn.setAttribute('aria-label', `Go to page ${i}`);
    pageBtn.setAttribute('aria-current', i === currentPage ? 'page' : 'false');
    if (i === currentPage) {
      pageBtn.classList.add('active');
    }
    pageBtn.addEventListener('click', () => {
      currentPage = i;
      renderArticles();
      window.scrollTo({ top: document.querySelector('.articles-section').offsetTop, behavior: 'smooth' });
    });
    pagination.appendChild(pageBtn);
  }

  const nextBtn = document.createElement('button');
  nextBtn.className = 'pagination-btn';
  nextBtn.textContent = 'Next →';
  nextBtn.disabled = currentPage === totalPages;
  nextBtn.setAttribute('aria-label', 'Next page');
  nextBtn.addEventListener('click', () => {
    if (currentPage < totalPages) {
      currentPage++;
      renderArticles();
      window.scrollTo({ top: document.querySelector('.articles-section').offsetTop, behavior: 'smooth' });
    }
  });
  pagination.appendChild(nextBtn);
}

/* ===========================
   MODAL FUNCTIONALITY
   =========================== */

function openArticleModal(article) {
  const modal = document.getElementById('articleModal');
  const articleDetail = document.getElementById('articleDetail');

  articleDetail.innerHTML = `
    <h1>${article.title}</h1>
    <div class="article-meta">
      <strong>By ${article.author}</strong>
      <span>•</span>
      <span>${formatDate(article.date)}</span>
      <span>•</span>
      <span>${article.readTime}</span>
      ${article.confidence ? `<span>•</span><span class="confidence-badge">Confidence: ${article.confidence}%</span>` : ''}
    </div>
    <img src="${article.image}" alt="${article.title}" style="width: 100%; border-radius: 8px; margin: 20px 0; max-height: 400px; object-fit: cover;">
    <div class="article-body">
      <p>${article.content}</p>
      <h2>Key Concepts Covered</h2>
      <ul style="margin-left: 20px; line-height: 1.8; color: #cbd5e1;">
        <li>Fundamental principles and theory</li>
        <li>Practical implementation techniques</li>
        <li>Real-world applications and use cases</li>
        <li>Performance considerations and optimization</li>
        <li>Best practices and common pitfalls to avoid</li>
      </ul>
      <p style="margin-top: 20px;">This article provides both theoretical understanding and practical guidance for applying these concepts in your own projects.</p>
    </div>
  `;

  modal.classList.add('active');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';

  const closeBtn = modal.querySelector('.modal-close');
  if (closeBtn) {
    closeBtn.focus();
  }
}

function closeModal() {
  const modal = document.getElementById('articleModal');
  modal.classList.remove('active');
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
    openArticleModal(post);
  }
}

/* ===========================
   NEWSLETTER SIGNUP
   =========================== */

function handleNewsletterSignup(event) {
  event.preventDefault();

  const form = event.target;
  const email = form.querySelector('input[type="email"]').value;

  console.log('Newsletter subscription:', email);

  const submitBtn = form.querySelector('button[type="submit"]');
  const originalText = submitBtn.textContent;
  submitBtn.textContent = '✓ Subscribed!';
  submitBtn.disabled = true;

  setTimeout(() => {
    form.reset();
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
  }, 2000);
}

/* ===========================
   INITIALIZATION LOGGING
   =========================== */

console.log(`🤖 The Next Gen AI Blog redesigned with ${blogPosts.length} articles`);
console.log(`📚 Categories: ${[...new Set(blogPosts.map(p => p.category))].join(', ')}`);
