# Plan: Expand Topic Classification with Sub-categories

## Overview
Replace the broad keyword lists with fine-grained sub-categories (e.g., split "Programming" into "Python", "JavaScript", "Web Development"), expand existing keywords, and add new life domains (Health, Entertainment, Travel, Finance, Sports, Food, Work, Education). This keeps the simple matching logic but dramatically improves coverage from 27% to 60%+. Update the `classify_search_topic()` function and add output analysis to see the new distribution.

## Current State Analysis
- **73% of queries fall into "Other"** (4,377 out of 5,996)
- Only 27% properly classified into specific topics
- Current keyword lists are extremely tech-centric
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

## Proposed Changes

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

### 4. Execution Steps

1. Replace the `classify_search_topic()` function in the notebook with expanded topic dictionary
2. Re-run the topic classification cells (cells 7-9)
3. Analyze new distribution:
   - Expected "Other" percentage to drop from 73% to ~40-50%
   - Expect more balanced distribution across topics
4. Spot-check output of "Top searches by topic" to validate sub-categories make sense
5. (Optional) Sample 20-30 remaining "Other" queries to identify gaps for future refinement

## Expected Outcomes

- **Before**: 73% in "Other", 27% properly classified
- **After**: ~40-50% in "Other", 50-60% properly classified
- More granular insights (e.g., Python searches separate from JavaScript)
- Better visibility into user's actual interests

## Refinement Strategy

If "Other" still remains high after this expansion:
- Option A: Add scoring-based matching (highest-scoring topic wins instead of first match)
- Option B: Use fuzzy/regex matching for edge cases
- Option C: Sample and manually review remaining "Other" queries for missed patterns

## Notes

- Keeping logic simple: first-match wins, no scoring complexity
- Total keywords expanding from ~70 to 200+
- Prioritizing common, broad terms over hyper-specific ones
- Open to iteration based on results
