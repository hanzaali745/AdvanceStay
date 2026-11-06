# GA4 Setup Guide — TheNextGenAI

## Step 1: Create GA4 Account (Manual — You do this)

1. Go to https://analytics.google.com
2. Click **"Create Account"** (or **"+ Create"** if you have existing accounts)
3. Fill in:
   - **Account name:** TheNextGenAI
   - **Website URL:** https://thenextgenai.com
   - **Industry category:** Media & Publishing
   - **Business size:** Small

4. On the next screen, create a **Property**:
   - **Property name:** TheNextGenAI Blog
      - **Reporting timezone:** UTC (or your timezone)
   - **Currency:** USD

5. Create a **Web Data Stream**:
   - **Website URL:** https://thenextgenai.com
   - **Stream name:** TheNextGenAI Website
   - Copy the **Measurement ID** (format: `G-XXXXXXXXXX`)

---

## Step 2: Add GA4 Tracking Code to Website

Once you have your **Measurement ID**, provide it to me and I'll add this code to the HTML file:

```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX', {
    'page_path': window.location.pathname,
    'page_title': document.title
  });
</script>
```

**Replace `G-XXXXXXXXXX` with your Measurement ID.**

---

## Step 3: Custom Events Setup

I'll configure these custom events to track monetization:

### Affiliate Tracking
```javascript
gtag('event', 'affiliate_click', {
  'affiliate_program': 'claude',  // or openai, midjourney, etc.
  'tool_name': 'Claude AI',
  'page_location': window.location.href,
  'timestamp': new Date().toISOString()
});
```

### Sponsorship Tracking
```javascript
gtag('event', 'sponsor_impression', {
  'sponsor_type': 'newsletter',  // or article, featured
  'sponsor_name': 'Sponsor Name',
  'page_location': window.location.href
});
```

### Newsletter Signup
```javascript
gtag('event', 'newsletter_signup', {
  'email_provided': true,
  'signup_location': 'homepage'  // or sidebar, post, etc.
});
```

### Product View
```javascript
gtag('event', 'view_product', {
  'product_name': 'AI Tools Spreadsheet',
  'product_category': 'lead_magnet'
});
```

### AdSense Impression
```javascript
gtag('event', 'adsense_impression', {
  'ad_type': 'display',
  'ad_size': '300x250',
  'page_location': window.location.href
});
```

---

## Step 4: Link to Google Search Console

1. In GA4, go to **Admin → Property Settings → Data Streams**
2. Click your web stream
3. Look for **Enhanced measurement** — enable all:
   - ✅ Scrolls
   - ✅ Outbound clicks
   - ✅ File downloads
   - ✅ Video engagement
   - ✅ Form interactions

4. Go to **Admin → Search Console Links**
5. Click **Link Search Console**
6. Select your thenextgenai.com property (must be verified in Search Console first)

---

## Step 5: Create Custom Reports

### Revenue Dashboard
In GA4, create these **Custom Reports** to track money:

**Report 1: Affiliate Performance**
- Rows: Event name, Parameter (affiliate_program)
- Values: Event count
- Filter: event = affiliate_click

**Report 2: Sponsorship Metrics**
- Rows: Event name, Parameter (sponsor_type)
- Values: Event count, Users
- Filter: event = sponsor_impression

**Report 3: Newsletter Growth**
- Rows: Date
- Values: Event count (newsletter_signup)
- Comparison: Month over month

**Report 4: Content Performance**
- Rows: Page path and screen class
- Values: Users, Avg. engagement time, Events
- Filter: Page path = /blog or /post

---

## Step 6: Set Up Conversion Goals

In GA4, go to **Admin → Conversions** and mark these as **Key Events**:

- [ ] `affiliate_click` — User clicks affiliate link
- [ ] `newsletter_signup` — User subscribes to newsletter
- [ ] `sponsor_impression` — User sees sponsor content
- [ ] `view_product` — User views digital product

These will appear in your conversion funnel reports.

---

## Step 7: Create Audiences

In GA4, go to **Admin → Audiences** and create:

**Audience 1: Affiliate Clickers**
- Condition: `affiliate_click` event
- Description: Users who clicked at least one affiliate link

**Audience 2: Newsletter Subscribers**
- Condition: `newsletter_signup` event
- Description: Users who subscribed to email list

**Audience 3: Returning Readers**
- Condition: Sessions >= 3
- Description: Users who came back 3+ times

**Audience 4: High Engagement**
- Condition: Engagement time >= 2 minutes
- Description: Users who spent 2+ minutes on site

---

## Step 8: Revenue Tracking Spreadsheet

Create a Google Sheet to manually track daily/weekly revenue:

| Date | Source | Clicks | Conversions | Amount | Notes |
|------|--------|--------|-------------|--------|-------|
| 2026-11-07 | Affiliate-Claude | 5 | 1 | $45 | First affiliate sale |
| 2026-11-07 | Newsletter | 120 | 15 | $0 | Lead generation |
| 2026-11-08 | Affiliate-ChatGPT | 8 | 2 | $60 | Growing interest |

**Purpose:** GA4 tracks interactions, but affiliate commissions are reported separately by each program. This spreadsheet bridges the gap.

---

## Step 9: Verify Everything Works

### Test Affiliate Click Tracking
1. Go to #recommended-tools on website
2. Click an affiliate link
3. In GA4, go to **Real-time** → watch for `affiliate_click` event

### Test Newsletter Signup
1. Submit the newsletter form
2. Check GA4 Real-time for `newsletter_signup` event

### Test Page Views
1. Navigate to different pages
2. GA4 should show page titles and paths
3. Check **Engagement** → **Pages and screens**

---

## Step 10: Set Up Alerts

In GA4, go to **Admin → Anomaly Detection**:
- Alert if affiliate clicks spike 2x above normal
- Alert if newsletter signups drop 50% below average
- Alert if page bounce rate exceeds 80%

---

## Monthly Review Checklist

- [ ] Check GA4 dashboard for top-performing blog posts
- [ ] Check which affiliate programs drive most clicks
- [ ] Review newsletter growth rate
- [ ] Analyze which content types get highest engagement
- [ ] Update revenue spreadsheet with actual commissions
- [ ] Identify low-performing content for improvement
- [ ] Plan next month's content based on data

---

## Resources

- **GA4 Help:** https://support.google.com/analytics/answer/10089681
- **Custom Events Guide:** https://support.google.com/analytics/answer/9322688
- **Conversion Setup:** https://support.google.com/analytics/answer/9267568
- **Search Console Link:** https://support.google.com/analytics/answer/10313292

---

## Your GA4 Measurement ID

**Once you create your GA4 account, copy your Measurement ID here:**

```
Measurement ID: G-________________
```

**Send me your Measurement ID and I'll:**
1. Add it to the HTML file
2. Implement all custom event tracking
3. Create test events
4. Verify everything works
