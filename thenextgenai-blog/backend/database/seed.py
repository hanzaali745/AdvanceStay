"""
Database seeding script - Initialize with sample data
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from database.models import Author, Article, NewsletterSubscriber
from auth.password import hash_password

def seed_database(db: Session):
    """Seed database with sample data"""

    # Clear existing data
    db.query(Article).delete()
    db.query(Author).delete()
    db.query(NewsletterSubscriber).delete()
    db.commit()

    # Create authors
    authors_data = [
        {
            "name": "Dr. Alex Rivera",
            "slug": "alex-rivera",
            "title": "AI Researcher",
            "affiliation": "MIT CSAIL",
            "bio": "PhD in AI from Stanford. 8+ years at MIT CSAIL researching transformer architectures and LLM scaling laws.",
            "email": "alex@mit.edu",
            "twitter": "alexrivera",
            "github": "alexrivera",
            "verification_status": "expert"
        },
        {
            "name": "Sarah Chen",
            "slug": "sarah-chen",
            "title": "ML Engineer",
            "affiliation": "OpenAI",
            "bio": "Deep learning specialist at OpenAI. Published 15+ papers on attention mechanisms and prompt optimization.",
            "email": "sarah@openai.com",
            "twitter": "sarahchen_ml",
            "github": "sarahchen",
            "verification_status": "verified"
        },
        {
            "name": "Marcus Thompson",
            "slug": "marcus-thompson",
            "title": "Research Lead",
            "affiliation": "Google DeepMind",
            "bio": "Leading research team at DeepMind. 12 years in NLP and computer vision.",
            "email": "marcus@deepmind.com",
            "twitter": "marcust",
            "github": "marcusthompson",
            "verification_status": "expert"
        },
        {
            "name": "Emma Wilson",
            "slug": "emma-wilson",
            "title": "AI Researcher",
            "affiliation": "UC Berkeley",
            "bio": "Postdoc at UC Berkeley. Research focused on interpretability and alignment.",
            "email": "emma@berkeley.edu",
            "twitter": "emmaw_ai",
            "github": "emmawilson",
            "verification_status": "verified"
        },
        {
            "name": "James Liu",
            "slug": "james-liu",
            "title": "NLP Engineer",
            "affiliation": "Meta AI",
            "bio": "Building LLM infrastructure at Meta. 6 years in large-scale model training.",
            "email": "james@meta.com",
            "twitter": "jamesliu_nlp",
            "github": "jamesliu",
            "verification_status": "verified"
        },
        {
            "name": "Dr. Lisa Anderson",
            "slug": "lisa-anderson",
            "title": "Senior Researcher",
            "affiliation": "Stanford AI Lab",
            "bio": "Director of Stanford AI Lab. Pioneering work in prompt engineering and few-shot learning.",
            "email": "lisa@stanford.edu",
            "twitter": "lisaanderson_ai",
            "github": "lisaanderson",
            "verification_status": "expert"
        },
    ]

    authors = []
    for author_data in authors_data:
        author = Author(**author_data)
        db.add(author)
        authors.append(author)

    db.commit()

    # Create articles
    articles_data = [
        {
            "title": "Understanding Large Language Models",
            "slug": "understanding-llms",
            "content": "# Understanding Large Language Models\n\nLarge Language Models (LLMs) represent a paradigm shift in natural language processing...",
            "excerpt": "A comprehensive breakdown of how LLMs work, their capabilities, limitations, and what's really happening under the hood.",
            "author_id": authors[0].id,
            "category": "research",
            "difficulty": "intermediate",
            "image_url": "https://images.unsplash.com/photo-1677442d019cecf8d6cb94183d71a44b6?w=600&h=400&fit=crop",
            "confidence_score": 98,
            "tags": ["llms", "transformers", "deep-learning"],
            "is_published": True,
            "published_at": datetime.utcnow() - timedelta(days=5),
            "view_count": 350,
            "read_count": 280,
            "trending_rank": 1
        },
        {
            "title": "Prompt Engineering Best Practices",
            "slug": "prompt-engineering-best-practices",
            "content": "# Prompt Engineering Best Practices\n\nPrompt engineering is the art and science of crafting effective prompts...",
            "excerpt": "Master the techniques that make LLMs behave exactly how you want them to.",
            "author_id": authors[1].id,
            "category": "tutorials",
            "difficulty": "beginner",
            "image_url": "https://images.unsplash.com/photo-1677442d019cecf8d6cb94183d71a44d5?w=600&h=400&fit=crop",
            "confidence_score": 95,
            "tags": ["prompting", "llms", "techniques"],
            "is_published": True,
            "published_at": datetime.utcnow() - timedelta(days=3),
            "view_count": 420,
            "read_count": 360,
            "trending_rank": 2
        },
        {
            "title": "Transformer Architecture Deep Dive",
            "slug": "transformer-architecture-deep-dive",
            "content": "# Transformer Architecture Deep Dive\n\nThe transformer architecture is the foundation of modern LLMs...",
            "excerpt": "Understand the inner workings of attention mechanisms and multi-head attention.",
            "author_id": authors[2].id,
            "category": "research",
            "difficulty": "advanced",
            "image_url": "https://images.unsplash.com/photo-1677442d019cecf8d6cb94183d71a44d6?w=600&h=400&fit=crop",
            "confidence_score": 96,
            "tags": ["transformers", "attention", "architecture"],
            "is_published": True,
            "published_at": datetime.utcnow() - timedelta(days=7),
            "view_count": 280,
            "read_count": 220,
            "trending_rank": 3
        },
        {
            "title": "Fine-tuning LLMs for Your Domain",
            "slug": "fine-tuning-llms",
            "content": "# Fine-tuning LLMs for Your Domain\n\nLearn how to adapt pre-trained models to your specific use case...",
            "excerpt": "Complete guide to domain-specific model adaptation with practical examples.",
            "author_id": authors[3].id,
            "category": "guides",
            "difficulty": "intermediate",
            "image_url": "https://images.unsplash.com/photo-1677442d019cecf8d6cb94183d71a44d7?w=600&h=400&fit=crop",
            "confidence_score": 92,
            "tags": ["fine-tuning", "transfer-learning", "llms"],
            "is_published": True,
            "published_at": datetime.utcnow() - timedelta(days=2),
            "view_count": 310,
            "read_count": 260,
            "trending_rank": 4
        },
        {
            "title": "Retrieval Augmented Generation (RAG)",
            "slug": "retrieval-augmented-generation",
            "content": "# Retrieval Augmented Generation (RAG)\n\nRAG systems enhance LLMs by incorporating external knowledge sources...",
            "excerpt": "How to build systems that ground LLM outputs in real data and documents.",
            "author_id": authors[4].id,
            "category": "analysis",
            "difficulty": "advanced",
            "image_url": "https://images.unsplash.com/photo-1677442d019cecf8d6cb94183d71a44d8?w=600&h=400&fit=crop",
            "confidence_score": 94,
            "tags": ["rag", "retrieval", "knowledge"],
            "is_published": True,
            "published_at": datetime.utcnow() - timedelta(days=4),
            "view_count": 220,
            "read_count": 180,
            "trending_rank": 5
        },
        {
            "title": "LLM Safety and Alignment",
            "slug": "llm-safety-alignment",
            "content": "# LLM Safety and Alignment\n\nEnsuring LLMs behave safely and align with human values...",
            "excerpt": "Critical approaches to AI safety and techniques for reducing harmful outputs.",
            "author_id": authors[5].id,
            "category": "research",
            "difficulty": "advanced",
            "image_url": "https://images.unsplash.com/photo-1677442d019cecf8d6cb94183d71a44d9?w=600&h=400&fit=crop",
            "confidence_score": 97,
            "tags": ["safety", "alignment", "ethics"],
            "is_published": True,
            "published_at": datetime.utcnow() - timedelta(days=6),
            "view_count": 190,
            "read_count": 140,
            "trending_rank": 6
        },
    ]

    for article_data in articles_data:
        article = Article(**article_data)
        db.add(article)

    db.commit()

    # Create newsletter subscribers
    subscribers_data = [
        {"email": "subscriber1@example.com", "name": "John Doe", "is_verified": True},
        {"email": "subscriber2@example.com", "name": "Jane Smith", "is_verified": True},
        {"email": "subscriber3@example.com", "name": "Bob Wilson", "is_verified": True},
        {"email": "subscriber4@example.com", "name": "Alice Johnson", "is_verified": False},
        {"email": "subscriber5@example.com", "name": "Charlie Brown", "is_verified": True},
    ]

    for sub_data in subscribers_data:
        subscriber = NewsletterSubscriber(**sub_data)
        db.add(subscriber)

    db.commit()

    print("✅ Database seeded successfully!")
    print(f"   - {len(authors)} authors created")
    print(f"   - {len(articles_data)} articles created")
    print(f"   - {len(subscribers_data)} newsletter subscribers created")
