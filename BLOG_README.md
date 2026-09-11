# AdvanceStay Professional Blog

A modern, responsive blog website built with HTML, CSS, and JavaScript. Features a professional design system, advanced filtering, search functionality, and an optimized user experience across all devices.

## 🎨 Design System

### Color Palette
- **Primary Navy**: `#0B1F3A` - Trust and professionalism
- **Teal Accent**: `#0EA5A0` - Modern and forward-thinking
- **Gold Highlight**: `#D4A574` - Warmth and welcome
- **Light Sand**: `#F5F3F0` - Clean and spacious background

### Typography
- **Display Font**: Playfair Display (headlines)
- **Body Font**: Inter (copy and UI text)
- **Utility Font**: Inter (consistent UI)

## 📁 Project Structure

```
AdvanceStay/
├── index.html              # Main blog homepage
├── styles.css              # All styling and responsive design
├── app.js                  # Blog functionality and interactions
├── Main.dc.html            # Design system artboard
├── advancestay-blog-design.html  # Published design canvas
└── canvas.json             # Design canvas layout
```

## ✨ Features

### Core Features
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Post Filtering**: Filter articles by category (Destinations, Tips, Guides, Reviews)
- **Full-Text Search**: Search posts by title, content, author, or category
- **Pagination**: Browse posts across multiple pages
- **Post Details**: Click any post to view the full article in a modal

### User Experience
- **Sticky Navigation**: Easy access to navigation at all times
- **Hero Section**: Engaging welcome area with featured content
- **Featured Article**: Highlighted post on the homepage
- **Newsletter Signup**: Email subscription form
- **Mobile Menu**: Toggle navigation on smaller screens
- **Smooth Scrolling**: Elegant navigation between sections

### Technical
- **Accessibility**: WCAG 2.1 compliance with semantic HTML, ARIA labels, keyboard navigation
- **Dark Mode**: Automatic dark theme support via `prefers-color-scheme`
- **Performance**: Optimized images, lazy loading support, minimal dependencies
- **Progressive Enhancement**: Works without JavaScript (core functionality)
- **Responsive Grid**: Modern CSS Grid and Flexbox layouts
- **Touch-Friendly**: 44px minimum touch targets on mobile

## 🚀 Getting Started

### Prerequisites
- Any modern web browser (Chrome, Firefox, Safari, Edge)
- No build tools or dependencies required

### Running Locally
1. Clone the repository
2. Open `index.html` in your browser
3. Or serve with a local server:
   ```bash
   python -m http.server 8000
   # or
   npx http-server
   ```

## 📝 Blog Posts

The blog comes with 12 sample posts organized by category:

### Destinations (4 posts)
- Hidden Beach Resorts
- Luxury Stays in Tuscany
- Barcelona's Best Neighborhoods
- Top Alpine Ski Resorts
- African Safari: A Wildlife Adventure

### Travel Tips (3 posts)
- Budget Travel Hacks
- What to Pack for Every Climate
- Sustainable Travel Practices

### Guides (3 posts)
- 48-Hour Tokyo Itinerary
- Culinary Travel Guide

### Reviews (2 posts)
- Five-Star Resorts in Maldives
- Luxury Cruise Experiences

## 🛠️ Customization

### Adding New Posts
Edit `app.js` and add new objects to the `blogPosts` array:

```javascript
{
  id: 'unique-id',
  title: 'Post Title',
  category: 'destinations', // or tips, guides, reviews
  excerpt: 'Short summary...',
  content: 'Full article content...',
  author: 'Author Name',
  date: 'YYYY-MM-DD',
  image: 'https://image-url.jpg',
  readTime: '8 min read'
}
```

### Changing Colors
Update CSS variables in `styles.css`:

```css
:root {
  --color-navy: #0B1F3A;
  --color-teal: #0EA5A0;
  --color-gold: #D4A574;
  /* ... */
}
```

### Modifying Layout
All spacing and sizing use CSS variables in `:root`. Adjust `--space-*` and `--radius-*` variables to customize the layout.

## 🎯 Responsive Breakpoints

- **Desktop**: 1200px+ (3-column grid)
- **Tablet**: 768px - 1199px (2-column or responsive)
- **Mobile**: Below 768px (1-column, optimized touch targets)
- **Small Mobile**: Below 480px (reduced spacing, single column)

## ♿ Accessibility

- **Keyboard Navigation**: Full keyboard support for all interactive elements
- **Screen Reader Ready**: Semantic HTML with ARIA labels
- **Color Contrast**: All text meets WCAG AA standards (4.5:1 minimum)
- **Focus Indicators**: Clear, visible focus states on all interactive elements
- **Reduced Motion**: Respects `prefers-reduced-motion` media query
- **Mobile Friendly**: Touch targets 44px minimum
- **Alt Text**: All images have descriptive alt attributes

## 📊 Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🔍 Search & Filter

### Search
Type in the search box to find posts by:
- Post title
- Excerpt/content
- Author name
- Category

### Filtering
Click category buttons to filter posts:
- All Articles (resets filter)
- Destinations
- Travel Tips
- Guides
- Reviews

## 📱 Mobile Optimization

- Touch-friendly interface with large tap targets
- Optimized touch performance
- Mobile menu that closes automatically when navigating
- Flexible grid that adapts to screen size
- Readable typography at all sizes
- No horizontal scrolling

## 🎨 Design Canvas

A professional design system is available in the published Claude Design canvas:
https://claude.ai/code/artifact/df86b8dd-5934-464e-9694-573f25988715

This includes:
- Homepage layout
- Color system visualization
- Typography scale
- Component library
- Responsive behavior documentation

## 📧 Newsletter Integration

The newsletter form is ready to integrate with an email service. Currently, it shows a success message. To connect a real service:

1. Update `handleNewsletterSignup()` in `app.js`
2. Add your email service API endpoint
3. Handle the subscription server-side

## 🚀 Deployment

### Static Hosting (Recommended)
This blog requires no backend and can be deployed to:
- Netlify (drag & drop)
- Vercel (git integration)
- GitHub Pages
- AWS S3 + CloudFront
- Cloudflare Pages
- Any static hosting service

### Environment Variables
No sensitive environment variables needed. All configuration is in the code.

## 📈 Future Enhancements

Potential features for future versions:
- Real database backend (MongoDB, PostgreSQL)
- User authentication
- Comment system
- Social sharing
- Advanced analytics
- Image optimization with WebP support
- CDN integration
- API for external content
- Admin dashboard
- Multiple authors with bios

## 📄 License

This blog website is built for AdvanceStay and follows the repository's licensing.

## 🤝 Contributing

Contributions are welcome! To add new features or fix issues:

1. Create a feature branch
2. Make your changes
3. Test across devices and browsers
4. Submit a pull request

## 📞 Support

For questions or issues, please refer to the main AdvanceStay repository documentation or create an issue in the GitHub repository.

---

Built with ❤️ using HTML5, CSS3, and vanilla JavaScript.
