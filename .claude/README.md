# Claude Code Agents for YouTube Transcript & Summary

This directory contains specialized AI agents (slash commands) designed to accelerate development of the YouTube Transcript & Summary app.

## Available Agents

### 🚀 Development Agents

#### `/implement-feature`
**Feature implementation specialist** - Implements new features from `next_level_features.md` or user requests with production-quality code.

Use when:
- Adding features from the feature wishlist
- Implementing user-requested functionality
- Building new capabilities

Example: `/implement-feature Add YouTube video embed preview to Streamlit UI`

---

#### `/enhance-ui`
**UI/UX specialist** - Improves the Streamlit web interface with better design, layouts, and user experience.

Use when:
- Improving visual design
- Adding interactive elements
- Implementing UX improvements
- Making the interface more intuitive

Example: `/enhance-ui Add dark mode toggle and improve layout`

---

#### `/add-export-format`
**Export format specialist** - Adds new export formats or enhances existing ones (DOCX, SRT, EPUB, etc.).

Use when:
- Adding new output format support
- Improving existing export formats
- Customizing export templates

Example: `/add-export-format Add SRT subtitle export for transcripts`

---

### 🧪 Quality & Testing Agents

#### `/test-app`
**QA specialist** - Thoroughly tests the application, identifies bugs, and verifies functionality.

Use when:
- Testing after major changes
- Verifying features work correctly
- Finding edge cases and issues
- Doing smoke tests

Example: `/test-app Test the PDF export with long transcripts`

---

#### `/add-tests`
**Testing specialist** - Creates comprehensive automated test suites (unit, integration, end-to-end tests).

Use when:
- Setting up test infrastructure
- Adding test coverage
- Creating unit tests for new features
- Implementing CI/CD testing

Example: `/add-tests Create unit tests for transcription functions`

---

#### `/review-code`
**Code review specialist** - Conducts thorough code reviews for quality, security, and best practices.

Use when:
- Before committing major changes
- Reviewing code quality
- Finding security issues
- Improving code maintainability

Example: `/review-code Review yt_transcribe_and_summarize.py for improvements`

---

### ⚡ Performance & Optimization Agents

#### `/optimize-performance`
**Performance specialist** - Identifies and implements performance improvements for speed, memory, and GPU utilization.

Use when:
- Processing is too slow
- Memory usage is high
- GPU is underutilized
- Batch processing needs optimization

Example: `/optimize-performance Improve Whisper model loading time`

---

#### `/batch-optimize`
**Batch processing specialist** - Enhances batch processing with parallel execution, progress tracking, and error recovery.

Use when:
- Processing multiple videos is slow
- Need better progress tracking
- Want parallel processing
- Need resume capability

Example: `/batch-optimize Add parallel processing for batch jobs`

---

### 🤖 AI & Analysis Agents

#### `/experiment-models`
**AI model specialist** - Researches and integrates better AI models for transcription, summarization, and diarization.

Use when:
- Want better transcription quality
- Testing different summarization models
- Comparing model performance
- Evaluating new models

Example: `/experiment-models Compare Whisper-large-v3 with current model`

---

#### `/analyze-video`
**Content analysis specialist** - Implements advanced analysis features (topic extraction, sentiment, chapters, etc.).

Use when:
- Adding content analysis features
- Extracting topics or key phrases
- Generating chapters automatically
- Performing sentiment analysis

Example: `/analyze-video Add automatic chapter generation based on topics`

---

### 🔧 Infrastructure Agents

#### `/manage-deps`
**Dependency management specialist** - Maintains dependencies, updates packages, and resolves conflicts.

Use when:
- Updating dependencies
- Fixing version conflicts
- Adding new packages
- Auditing security vulnerabilities

Example: `/manage-deps Update all dependencies and check for vulnerabilities`

---

#### `/plan-deployment`
**Deployment specialist** - Creates deployment strategies (Docker, cloud, web service, etc.).

Use when:
- Deploying to production
- Creating Docker containers
- Setting up cloud deployment
- Building distribution packages

Example: `/plan-deployment Create Docker container with GPU support`

---

#### `/create-plugin`
**Plugin architecture specialist** - Designs and implements a plugin system for extensibility.

Use when:
- Adding plugin support
- Creating extension points
- Building plugin examples
- Designing modular architecture

Example: `/create-plugin Design plugin system for custom export formats`

---

### 📚 Documentation Agents

#### `/update-docs`
**Documentation specialist** - Creates and maintains comprehensive documentation for users and developers.

Use when:
- Adding new features (document them!)
- Updating installation instructions
- Improving user guides
- Writing developer documentation

Example: `/update-docs Update README with new export formats`

---

### 🐛 Bug Fixing Agent

#### `/fix-bug`
**Debugging specialist** - Systematically identifies, diagnoses, and fixes bugs.

Use when:
- Encountering errors
- Debugging issues
- Fixing reported bugs
- Investigating unexpected behavior

Example: `/fix-bug Audio download fails for some videos`

---

## Quick Start Guide

### Using Agents

1. **Invoke an agent** by typing `/` followed by the agent name:
   ```
   /implement-feature Add video preview
   ```

2. **Be specific** in your request. The more context you provide, the better the agent can help:
   ```
   /optimize-performance The Whisper model loading takes 30 seconds. Can we cache it?
   ```

3. **Combine agents** for complex tasks:
   ```
   /implement-feature Add dark mode toggle
   /test-app Test dark mode in different scenarios
   /update-docs Document the new dark mode feature
   ```

### Workflow Examples

#### Adding a New Feature
```
/implement-feature Add YouTube video embed to Streamlit UI
/test-app Verify video embed works with different URLs
/update-docs Add video embed to README
```

#### Improving Performance
```
/optimize-performance Profile the summarization step
/batch-optimize Add parallel processing for multiple videos
/test-app Benchmark the improvements
```

#### Major Refactoring
```
/review-code Check yt_transcribe_and_summarize.py for improvements
/add-tests Create comprehensive test suite first
# Then make changes...
/test-app Run full test suite
```

#### Preparing for Production
```
/review-code Security audit
/add-tests Ensure test coverage
/plan-deployment Create Docker setup
/update-docs Complete documentation
```

## Development Philosophy

These agents follow the project's conventions:
- **Optional dependencies**: Graceful handling with try-except
- **Fallback patterns**: Always provide alternatives
- **Local-first**: No cloud dependencies, privacy-focused
- **User-friendly**: Clear error messages and documentation
- **Performance-aware**: Consider GPU/CPU implications

## Tips for Best Results

1. **Be specific**: Instead of "improve the app", say "add progress bars to batch processing"
2. **Provide context**: Mention error messages, file names, or specific use cases
3. **One task at a time**: Let the agent complete one task before moving to the next
4. **Review the work**: Agents are powerful but always verify their output
5. **Iterate**: Use multiple agents in sequence for complex tasks

## Agent Architecture

Each agent is a specialized prompt that:
- Understands the project architecture
- Follows established patterns
- Has specific expertise in its domain
- Provides actionable, tested solutions
- Updates relevant documentation

## Contributing New Agents

To create a new agent:

1. Create a new `.md` file in `.claude/commands/`
2. Name it descriptively (kebab-case)
3. Include:
   - Clear mission statement
   - Context about the project
   - Step-by-step process
   - Guidelines and best practices
   - Examples

See existing agents as templates.

## Troubleshooting

**Agent not found**: Make sure the file is in `.claude/commands/` and has a `.md` extension.

**Agent gives unexpected results**: Provide more context in your request.

**Agent seems stuck**: Break down your request into smaller, more specific tasks.

**Need human review**: Some changes are complex - always review agent output before committing.

## Next Steps

Ready to supercharge your development? Start with:

1. `/implement-feature` - Pick a feature from `next_level_features.md`
2. `/test-app` - Make sure everything works
3. `/update-docs` - Keep documentation current

Happy coding! 🚀
