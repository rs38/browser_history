# Plan: Expand Topic Classification with Sub-categories

## Overview
Replace the broad keyword lists with fine-grained sub-categories, add **bilingual (English + German) keywords**, extend classification to **all visited websites** (domains, page titles, URLs—not just Google search queries), and add new life domains (Health, Entertainment, Travel, Finance, Sports, Food, Work, Education). This keeps the simple matching logic but dramatically improves coverage from 27% to 60%+. Discuss ML/clustering approaches for later refinement.

**Key changes from original plan:**
1. Multi-language keyword support (English + German)
2. Classification scope: all visited content, not just Google search queries
3. Rationale for keyword-matching vs. ML approach

## Current State Analysis
- **73% of queries fall into "Other"** (4,377 out of 5,996 Google searches)
- Only 27% properly classified into specific topics
- Current analysis limited to **Google search query text only**
- Current scope: ~6K Google search queries
- **Untapped data**: ~100K+ other visited websites (domains, page titles, URLs) with zero classification
- Current keyword lists are extremely tech-centric and English-only
- Keyword specificity too narrow (e.g., "copilot" instead of broader patterns)

## Topic Coverage Breakdown (Current)
- AI/ML: 8.3% (497 queries)
- Hardware/Electronics: 8.0% (481 queries)
- Automotive/Vehicles: 4.4% (264 queries)
- Programming: 2.7% (160 queries)
- General Info: 1.8% (108 queries)
- Tools/Utilities: 0.7% (44 queries)
- Shopping/Ecommerce: 0.7% (43 queries)
- News/Current: 0.4% (22 queries)

## Scope Changes: From Google Searches to All Visited Content

### Current Scope (Limited)
- Only classifies **Google search query text** (~6K rows)
- Ignores all other visited websites (~100K+ rows)
- Only English keywords

### Proposed Extended Scope
Classify **all visited URLs** by extracting context from:
1. **Domain name** (e.g., `github.com` → Programming, `youtube.com` → Entertainment, `amazon.de` → Shopping)
2. **Page title** (IndexError: when available in CSV, e.g., "Sony A7IV Camera Review" → Photography/Hardware)
3. **URL path** (when meaningful, e.g., `/blog/python-tutorial` → Python/Programming)
4. **Full URL** (fallback keyword matching)

**New function signature:**
```python
def classify_visit(url: str, domain: str, page_title: str) -> str:
    """Classify a visit based on domain, title, and URL"""
    # Check domain first (most reliable)
    # Then page title (contextual)
    # Then URL path (when available)
    # First-match wins
```

**Data to work with:**
- `NavigatedToUrl`: full URL
- `domain`: extracted domain (already computed)
- `PageTitle`: page title (from CSV)

### Benefits of Extended Scope
- Classify 100%+ of visits, not just Google searches
- See distribution of interests across **all browsing**, not just searches
- Better insights into actual behavior (clicks reveal true interests)
- Identify sites you visit passively vs. actively search for

## Proposed Changes

### 0. Multi-Language Support

**Strategy: Bilingual keywords (English + German)**

Each keyword list includes both English and German terms. Case-insensitive matching applies to both.

**Example for "Python" category:**
```
"Python": [
    # English
    "python", "django", "flask", "pip", "pandas", "numpy", "jupyter", "anaconda",
    # German
    "python", "django", "flask", "pip", "pandas", "numpy", "jupyter", "anaconda",
    "python-programmierung", "pythonista"
]
```

**Approach:**
- Keep keywords simple: no accents/umlauts required (user types "muller" not "müller")
- Some keywords are identical across languages (e.g., "python", "flask")
- Add German-specific terms where they differ: "programmierung", "entwicklung", "verzeichnis", "datei"
- Use lowercase matching (`query_lower = text.lower()`)

**Supported languages initially:**
- English (primary)
- German (secondary, since user is likely German-speaking)

**Easy to extend to:** French, Dutch, Spanish, etc. by adding more keyword variants

### 1. Restructure Topic Categories with Finer Granularity

#### Current → New Structure

**Programming (2.7%)**
- Split into: "Python", "JavaScript/Web", "Systems/Backend" (C, Rust, Go), "Mobile Dev"
- Keywords for "Python": python, django, flask, pip, pandas, numpy, jupyter, anaconda
- Keywords for "JavaScript/Web": javascript, react, node, typescript, web, html, css, vue, angular, npm, webpack
- Keywords for "Systems/Backend": rust, go, c++, c#, java, kotlin, backend, server, microservice, database
- Keywords for "Mobile Dev": swift, kotlin, ios, android, mobile, app, flutter

**AI/ML (8.3%)**
- Split into: "AI/LLMs", "Data Science", "ML/Deep Learning"
- Keywords for "AI/LLMs": copilot, agent, gpt, llm, chatgpt, ai, openai, claude, deepseek, prompt engineering
- Keywords for "Data Science": numpy, pandas, scipy, scikit-learn, data science, data analysis, visualization, tableau, power bi
- Keywords for "ML/Deep Learning": neural, deep learning, tensorflow, pytorch, keras, training, model, algorithm

**Hardware/Electronics (8.0%)**
- Keep as-is or sub-divide by type
- Current keywords: arduino, raspberry, circuit, usb, microcontroller, fnirsi, multimeter, instek, breadboard, sensor
- Add: electronics, component, schematic, pcb, soldering, oscilloscope, embedded

**Automotive/Vehicles (4.4%)**
- Keep as broad category
- Add more keywords: vehicle, car, engine, motor, driving, automobile, repair, maintenance, fuel, tire, battery

**General Info (1.8%)**
- Broad category for abstract/how-to queries
- Keep: what, how, why, explain, definition, meaning, vs, comparison
- Add: learn, tutorial, guide, understand, help, question

**Tools/Utilities (0.7%)**
- Expand with more keywords
- Current: tool, utility, software, app, application, extension
- Add: download, installer, plugin, addon, script, cli, command line

**Shopping/Ecommerce (0.7%)**
- Expand keywords
- Current: amazon, ebay, shop, buy, price, product, sale, aliexpress, store
- Add: deal, coupon, discount, purchase, checkout, wishlist, order, retail

**News/Current (0.4%)**
- Expand slightly
- Current: news, breaking, update, announced, release, launched
- Add: latest, announcement, press release, bulletin, timeline, event

### 2. Add New Life Domain Categories

**Health/Medical** (estimated 5-10% of "Other")
- Keywords: health, medical, disease, symptom, doctor, nurse, treatment, medication, hospital, surgery, therapy, wellness, exercise, diet, nutrition, mental health, anxiety, depression

**Entertainment/Media** (estimated 8-12% of "Other")
- Keywords: movie, film, show, tv, game, video, stream, netflix, youtube, actor, director, imdb, music, song, artist, album, concert, book, author

**Travel/Location** (estimated 4-6% of "Other")
- Keywords: hotel, flight, airport, booking, vacation, travel, map, route, directions, city, country, tourism, hostel, resort, ticket

**Finance/Investment** (estimated 3-5% of "Other")
- Keywords: stock, crypto, bitcoin, finance, investment, bank, loan, mortgage, insurance, tax, savings, trading, portfolio, wealth, money, budget

**Sports** (estimated 2-4% of "Other")
- Keywords: sport, game, player, team, score, league, football, basketball, soccer, tennis, baseball, championship, tournament, coach

**Food/Cooking** (estimated 2-3% of "Other")
- Keywords: recipe, cook, food, restaurant, eating, ingredient, cooking, baking, cuisine, dish, menu, restaurant review, delivery

**Work/Career** (estimated 1-2% of "Other")
- Keywords: job, resume, interview, salary, employment, career, business, company, office, resume, linkedin, hiring, recruit, freelance

**Education/Learning** (estimated 1-2% of "Other")
- Keywords: course, tutorial, learn, class, school, university, degree, textbook, exam, study, certification, online learning, udemy, coursera

### 2. Domain-to-Category Mapping

**Approach: Create a hardcoded domain legend**

Since domain names are highly reliable indicators, map common domains directly:

```python
DOMAIN_CATEGORY_MAP = {
    # Programming
    "github.com": "Programming",
    "stackoverflow.com": "Programming",
    "reddit.com": "Programming",  # context-sensitive
    "python.org": "Python",
    "nodejs.org": "JavaScript/Web",
    "rust-lang.org": "Systems/Backend",
    
    # AI/ML
    "openai.com": "AI/LLMs",
    "huggingface.co": "AI/LLMs",
    "tensorflow.org": "ML/Deep Learning",
    "pytorch.org": "ML/Deep Learning",
    
    # Entertainment
    "youtube.com": "Entertainment/Media",
    "netflix.com": "Entertainment/Media",
    "twitch.tv": "Entertainment/Media",
    "imdb.com": "Entertainment/Media",
    "spotify.com": "Entertainment/Media",
    
    # Shopping
    "amazon.com": "Shopping/Ecommerce",
    "amazon.de": "Shopping/Ecommerce",
    "ebay.com": "Shopping/Ecommerce",
    "aliexpress.com": "Shopping/Ecommerce",
    
    # News
    "bbc.com": "News/Current",
    "cnn.com": "News/Current",
    "dw.com": "News/Current",
    "spiegel.de": "News/Current",
    "zeit.de": "News/Current",
    
    # Travel
    "booking.com": "Travel/Location",
    "airbnb.com": "Travel/Location",
    "maps.google.com": "Travel/Location",
    
    # Finance
    "coinbase.com": "Finance/Investment",
    "crypto.com": "Finance/Investment",
    "investing.com": "Finance/Investment",
    "coingecko.com": "Finance/Investment",
    
    # Work
    "linkedin.com": "Work/Career",
    "indeed.com": "Work/Career",
}
```

**Fallback:** If domain not in map, use keyword matching on domain + page title + URL.

### 3. Update Code Structure

**Old function structure:**
```python
topics = {
    "Category1": [keywords...],
    "Category2": [keywords...],
}
```

**New function structure (flattened for simple matching):**
```python
topics = {
    "Python": [...],
    "JavaScript/Web": [...],
    "Systems/Backend": [...],
    "Mobile Dev": [...],
    "AI/LLMs": [...],
    "Data Science": [...],
    "ML/Deep Learning": [...],
    "Hardware/Electronics": [...],
    "Automotive/Vehicles": [...],
    "General Info": [...],
    "Tools/Utilities": [...],
    "Shopping/Ecommerce": [...],
    "News/Current": [...],
    "Health/Medical": [...],
    "Entertainment/Media": [...],
    "Travel/Location": [...],
    "Finance/Investment": [...],
    "Sports": [...],
    "Food/Cooking": [...],
    "Work/Career": [...],
    "Education/Learning": [...],
}
```

Keep the simple first-match logic (no scoring changes).

### 4. Classification Priority Order

**For each visit, check in this order:**
1. **Domain mapping (DOMAIN_CATEGORY_MAP)** — fastest, most reliable
2. **Page title keywords** — contextual, catches nuance
3. **Domain name keywords** — fallback, handles unmapped domains
4. **URL path keywords** — least reliable, use last
5. **Return "Other"** if no match

**Example flow:**
```python
def classify_visit(url: str, domain: str, page_title: str) -> str:
    # Check domain map first
    if domain in DOMAIN_CATEGORY_MAP:
        return DOMAIN_CATEGORY_MAP[domain]
    
    # Check page title
    if page_title:
        topic = match_keywords(page_title, topics)
        if topic != "Other":
            return topic
    
    # Check domain name itself
    topic = match_keywords(domain, topics)
    if topic != "Other":
        return topic
    
    return "Other"
```

### 5. Execution Steps

1. Create `DOMAIN_CATEGORY_MAP` dictionary (100+ common domains mapped by hand)
2. Create expanded `topics` dictionary with 250+ bilingual keywords (English + German)
3. Implement new `classify_visit()` function following priority order above
4. Apply to entire DataFrame: `df["category"] = df.apply(lambda row: classify_visit(row["NavigatedToUrl"], row["domain"], row["PageTitle"]), axis=1)`
5. Analyze distribution across ALL 100K+ visits (not just Google searches)
6. Generate statistics:
   - Pie chart: category distribution
   - Top 10 domains per category
   - Sample page titles per category
   - Count and percentage of "Other"
7. Manual review of "Other" entries to identify missed patterns

## Expected Outcomes (Phase 1: Keyword + Domain Mapping)

### Before (Current State)
- Google searches only: 73% in "Other", 27% properly classified
- All visits: 0% classified (no existing system)

### After Keyword + Domain Expansion
- **Google searches**: Expected 30-40% in "Other", 60-70% properly classified
- **All visits**: Expected 40-50% in "Other", 50-60% properly classified
- More granular insights (Python vs. JavaScript vs. Rust)
- Better visibility into actual interests across **all browsing**, not just searches
- Identify passive browsing (clicks) vs. active searching (Google queries)

## Machine Learning Approaches: When & Why They Make Sense

### Current Keyword-Matching Approach

**Strengths:**
- ✅ Fast — O(keyword count) per visit, no model training
- ✅ Interpretable — clear why each visit gets a category
- ✅ Multilingual-friendly — just add keywords in any language
- ✅ Works offline — no API calls or cloud dependency
- ✅ Debuggable — easy to see which keyword matched

**Weaknesses:**
- ❌ Manual maintenance — need to hand-curate 200+ keywords
- ❌ Misses subtle patterns — "gaming chair" typed as URL won't match "Gaming"
- ❌ No semantic understanding — only substring matching
- ❌ Hidden context — page title alone may be misleading ("Best Python Tutorials" could be entertainment or education)

### Should We Add ML?

**Recommendation: Try Phase 1 first, then evaluate.**

After keyword expansion, check:
1. **Is "Other" < 40%?** → Keyword matching is probably sufficient. Done.
2. **Is "Other" 40-60%?** → Consider Phase 2 clustering
3. **Is "Other" > 60%?** → Definitely invest in ML

### ML Option A: Clustering (Unsupervised Discovery)

**Goal:** Find natural groupings in unclassified "Other" visits

**When it helps:**
- You have 5K+ "Other" visits and want to know what you're missing
- Discover new interest areas (e.g., "Gardening" that keywords didn't catch)
- No labeled training data available

**Approach:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Vectorize domain + title
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2,3), max_features=500)
X = vectorizer.fit_transform(
    df["domain"].fillna("") + " " + df["PageTitle"].fillna("")
)

# Find 30 clusters
kmeans = KMeans(n_clusters=30, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

# Inspect each cluster manually
for cluster_id in range(30):
    cluster_rows = df[df["cluster"] == cluster_id]
    print(f"\nCluster {cluster_id} ({len(cluster_rows)} rows):")
    print(cluster_rows[["domain", "PageTitle"]].head(5).to_string())
    # Decide: is this a new category? Or noise?
```

**Time cost:** ~5-10 minutes (vectorization + clustering + manual review)

**Benefit:** Discover what ~10-20% of "Other" is (often worth it)

### ML Option B: Supervised Classification (If Labeled Data Exists)

**Goal:** Train a classifier on manually-labeled visits

**When it helps:**
- You've already classified 1-2K visits manually
- "Other" has complex patterns that keywords can't capture
- Want production-quality classification

**Approach:**
```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Assume df["category_labeled"] exists (human-annotated)
X = df["domain"] + " " + df["PageTitle"].fillna("")
y = df["category_labeled"]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(analyzer='char', ngram_range=(2,3), max_features=500)),
    ("clf", RandomForestClassifier(n_estimators=100, max_depth=15))
])

pipeline.fit(X, y)

# Predict remaining "Other" entries
df.loc[df["category"] == "Other", "category_ml"] = pipeline.predict(
    X[df["category"] == "Other"]
)
```

**Time cost:** ~30-60 minutes (labeling 1-2K entries is tedious)

**Benefit:** High-confidence classifications for hard-to-keyword-match content

### ML Option C: Embeddings + Similarity (Modern Approach)

**Goal:** Use semantic embeddings to match visits to category prototypes

**When it helps:**
- Want "understanding" beyond keyword matching
- Have multilingual content (German + English)
- Okay with slightly higher computation

**Approach:**
```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Load multilingual model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Works for 100+ languages

# Embed all visits
texts = df["domain"] + " " + df["PageTitle"].fillna("")
embeddings = model.encode(texts, batch_size=32)

# Define category prototypes
prototypes = {
    "Python": model.encode("Python programming django flask"),
    "JavaScript/Web": model.encode("JavaScript React Node web development"),
    "Entertainment/Media": model.encode("YouTube Netflix movie film gaming"),
    # ... etc
}

# For each unclassified visit, find closest prototype
from sklearn.metrics.pairwise import cosine_similarity

for idx, row in df[df["category"] == "Other"].iterrows():
    embedding = embeddings[idx].reshape(1, -1)
    similarities = {
        cat: cosine_similarity(embedding, proto.reshape(1, -1))[0][0]
        for cat, proto in prototypes.items()
    }
    best_cat = max(similarities, key=similarities.get)
    best_score = similarities[best_cat]
    
    if best_score > 0.5:  # Confidence threshold
        df.loc[idx, "category"] = best_cat
```

**Time cost:** ~10-15 minutes (one-time embedding computation)

**Benefit:** Catches semantic similarity (e.g., "Python tutorial" if "Python" wasn't in keywords)

### Recommendation: Phased Approach

**Phase 1 (Now):**
- Implement keyword + domain mapping (focus here first)
- Expected to classify 50-60% of all visits correctly
- Takes 2-4 hours to build robust keyword lists

**Phase 2 (If "Other" > 40%):**
- Run unsupervised clustering on "Other" entries
- Discover ~3-5 new categories humans missed
- Takes ~1 hour

**Phase 3 (If pursuing perfection):**
- Start labeling remaining "Other" visits incrementally
- After 500-1K labeled, train supervised classifier
- Takes ~1-2 days of labeling effort

**Why start without ML:**
- Keyword lists are cheaper to build and maintain
- Easier to explain ("Why is this Gaming?")
- No risk of Black Box errors
- German support is trivial (just add keywords)
- Fast to iterate and debug

## Implementation Notes

- **Scope:** All ~100K+ visited URLs, not just Google searches (domain + title + URL)
- **Languages:** English + German keywords with case-insensitive matching
- **Domain mapping:** 100+ hardcoded domain→category mappings (github.com → Programming, etc.)
- **Keyword lists:** Expanded from ~70 to 250+ bilingual keywords
- **Logic:** Simple first-match, no scoring complexity (keeps it fast & interpretable)
- **Fallback:** Graceful "Other" category for truly unclassifiable visits
- **ML ready:** Architecture designed for easy ML integration later (Phase 2+)
