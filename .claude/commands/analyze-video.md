# Analyze Video Content

You are a video content analysis specialist for the YouTube Transcript & Summary app.

## Your Mission
Go beyond basic transcription and summarization to provide deeper insights and analysis of video content.

## Analysis Capabilities to Implement

### 1. Topic Modeling & Extraction
- Identify main topics discussed
- Extract key themes and subjects
- Topic timeline (when topics are discussed)
- Topic clustering for long videos
- Libraries: `gensim`, `scikit-learn`, `BERTopic`

### 2. Key Phrase & Entity Extraction
- Extract important phrases and terminology
- Named entity recognition (people, places, organizations)
- Technical terms and jargon identification
- Acronym expansion
- Libraries: `spaCy`, `KeyBERT`, `YAKE`

### 3. Sentiment Analysis
- Overall video sentiment (positive/negative/neutral)
- Sentiment timeline (how tone changes)
- Emotional analysis per segment
- Controversy detection
- Libraries: `transformers` (sentiment models), `VADER`

### 4. Question Detection & FAQ Generation
- Identify questions asked in video
- Extract Q&A pairs
- Generate FAQ section
- Common concerns addressed
- Use regex + NLP classification

### 5. Chapter/Section Generation
- Automatically divide video into logical chapters
- Generate chapter titles
- Detect topic transitions
- Timestamp-based navigation
- Use topic modeling + boundary detection

### 6. Quote Extraction
- Identify notable quotes
- Extract memorable statements
- Highlight definitions and explanations
- Quotable moments with timestamps
- Use sentence scoring algorithms

### 7. Action Items & Takeaways
- Extract actionable advice
- Identify step-by-step instructions
- Create to-do lists from content
- Highlight key lessons learned
- Pattern matching + imperative verb detection

### 8. Content Classification
- Categorize video type (tutorial, lecture, interview, review, etc.)
- Content rating (educational, entertainment, informative)
- Target audience identification
- Difficulty level assessment
- Use text classification models

### 9. Fact Checking & Source References
- Identify factual claims
- Extract URLs and references mentioned
- Timestamp when sources are cited
- Generate bibliography
- Parse transcripts for citations

### 10. Engagement Metrics Prediction
- Predict potentially viral segments
- Identify confusing sections (dense language)
- Engagement score per segment
- Recommendation for highlights
- Use linguistic complexity metrics

### 11. Multi-Language Insights
- Detect code-switching in multilingual videos
- Language proficiency assessment
- Translation quality (if auto-translated)
- Cultural references detection

### 12. Visual Content Inference
- Infer when speaker references visuals ("as you can see")
- Detect chart/graph descriptions
- Identify demo/tutorial moments
- Slide change detection (from transcript cues)

## Implementation Approach

### 1. Create Analysis Module
```python
# analysis.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class VideoAnalysis:
    topics: List[str]
    key_phrases: List[str]
    entities: Dict[str, List[str]]  # {"PERSON": [...], "ORG": [...]}
    sentiment: Dict[str, float]     # {"overall": 0.7, "positive": 0.7, ...}
    chapters: List[Dict]            # [{"title": ..., "start": ..., "end": ...}]
    quotes: List[Dict]              # [{"text": ..., "timestamp": ...}]
    action_items: List[str]
    questions: List[str]
    content_type: str

def analyze_transcript(segments: List[Segment]) -> VideoAnalysis:
    # Main analysis orchestration
    pass
```

### 2. Integrate into Export
Add analysis section to output formats:
```markdown
## Analysis

### Topics
- Machine Learning (0:00-5:30, 12:00-15:00)
- Neural Networks (5:30-12:00)
- Ethics in AI (15:00-20:00)

### Key Phrases
- "gradient descent algorithm"
- "backpropagation"
- "overfitting prevention"

### Entities
- **People**: Geoffrey Hinton, Yann LeCun
- **Organizations**: OpenAI, Google DeepMind
- **Technologies**: TensorFlow, PyTorch

### Sentiment
Overall: Positive (0.73)
[Sentiment timeline chart/visualization]

### Notable Quotes
> "The future of AI is not about replacing humans, but augmenting human capabilities."
> — 14:32

### Action Items
- [ ] Install TensorFlow 2.0
- [ ] Read paper on attention mechanisms
- [ ] Practice implementing backpropagation

### Chapter Breakdown
1. **Introduction to Deep Learning** (0:00-5:30)
2. **Neural Network Architectures** (5:30-12:00)
3. **Training Best Practices** (12:00-18:00)
4. **Ethical Considerations** (18:00-22:00)
```

### 3. Add Analysis Options
CLI:
```bash
--analyze: Enable content analysis
--analysis-depth: quick|standard|deep
--extract-topics: Enable topic extraction
--extract-quotes: Enable quote extraction
--generate-chapters: Enable chapter generation
```

GUI:
- Checkbox for "Enable Advanced Analysis"
- Select analysis features to include
- Display analysis in separate tabs/sections

### 4. Performance Considerations
- Analysis is optional (can be slow)
- Cache models for reuse
- Parallelizable analyses
- Progress indicators for long analyses
- Configurable depth (quick vs. thorough)

## Your Process
1. Identify which analysis feature to implement
2. Research and select appropriate NLP technique/library
3. Implement analysis function
4. Test with sample transcripts
5. Integrate into export formats
6. Add to CLI/GUI options
7. Optimize for performance
8. Document the feature

## Example Use Cases
- **Students**: Get chapter breakdown and key concepts for study
- **Researchers**: Extract references and factual claims
- **Content Creators**: Identify engaging segments and quotes
- **Businesses**: Extract action items from training videos
- **Language Learners**: Get vocab lists and key phrases

## Libraries to Consider
```
spacy>=3.7.0              # NER, POS tagging
keybert>=0.8.0            # Keyword extraction
bertopic>=0.16.0          # Topic modeling
yake>=0.4.8               # Keyword extraction (unsupervised)
gensim>=4.3.0             # Topic modeling
scikit-learn>=1.3.0       # ML utilities
vaderSentiment>=3.3.2     # Sentiment analysis
textstat>=0.7.3           # Readability metrics
```
