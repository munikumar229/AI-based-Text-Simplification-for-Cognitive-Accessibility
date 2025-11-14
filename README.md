# AI-Based Text Simplification for Cognitive Accessibility

A multilingual web application that simplifies text to improve cognitive accessibility. Built with Streamlit, Python, and advanced NLP models.

## Features

🌐 **Bilingual Support**: English and Telugu languages  
🎯 **Personalized Experience**: Questionnaire-guided customization with accessibility preferences  
🔧 **Reading Assistance Tools**: Font adjustments, letter spacing, bolding options, and visual themes  
🔊 **Text-to-Speech**: High-quality TTS with Fastspeech2_HS and gTTS fallback  
📱 **Responsive Design**: Works on desktop and mobile devices  
🎨 **Multiple Themes**: Light, Sepia, and Dark modes  
✨ **Advanced Text Processing**: Noun-preserving simplification, POS tagging, and intelligent summarization  
📝 **Interactive Examples**: Clickable demonstration cards showing different text enhancement techniques  

## Technology Stack

- **Framework**: Streamlit 1.28+
- **Language**: Python 3.8+
- **NLP Models**: Facebook NLLB (No Language Left Behind) for translation
- **POS Tagging**: Stanza for Telugu morphological analysis
- **Text-to-Speech**: FastSpeech2_HS for high-quality voices, gTTS as fallback
- **Translation**: Transformers library with pre-trained models
- **UI Components**: Streamlit components with custom CSS styling

## Quick Start

### Prerequisites

- **Python 3.8+** and pip
- **Git** for cloning the repository
- **Internet connection** for downloading ML models (first run)

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/munikumar229/AI-based-Text-Simplification-for-Cognitive-Accessibility.git

# Navigate to project directory
cd AI-based-Text-Simplification-for-Cognitive-Accessibility

# Install Python dependencies
pip install -r requirements.txt

# Run the application
streamlit run frontend.py
```

The application will open at `http://localhost:8501` and automatically download required ML models on first use.

### Alternative: Using Conda Environment

```bash
# Create and activate conda environment
conda create -n text-simplifier python=3.8
conda activate text-simplifier

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run frontend.py
```

## Project Structure

```
├── frontend.py              # Main Streamlit application
├── backend.py               # NLP and TTS processing functions
├── environment.yml          # Conda environment specification
├── requirements.txt         # Python dependencies
├── HCI_project_LLM.ipynb    # Research notebook with AI models
├── 1.html                   # Static HTML files
├── text-simplifier-woz-v3.html
├── README.md                # This file
└── .streamlit/             # Streamlit configuration (if present)
```

## Usage

### Application Flow

1. **Welcome**: Introduction screen
2. **Language Selection**: Choose English or Telugu
3. **Examples**: Interactive demonstration of text enhancement techniques
4. **Spacing Examples**: Letter spacing demonstration
5. **Questionnaire**: Answer questions about reading preferences and accessibility needs
6. **Text Input**: Paste text or upload a .txt file
7. **Processing**: AI-powered text simplification
8. **Results**: View, customize, and listen to simplified text

### Key Features

**🤖 AI-Powered Simplification**:
- Noun-preserving text summarization
- Intelligent sentence selection based on content importance
- Vocabulary simplification with synonym replacement
- Language detection and appropriate processing

**🎨 Accessibility Customizations**:
- Font size adjustment (14-30px)
- Line height and letter spacing controls
- Bold first letters of words
- Color-coded letters for enhanced readability
- Multiple visual themes (Light/Sepia/Dark)

**🔊 Text-to-Speech**:
- FastSpeech2_HS for high-quality Telugu voices
- gTTS fallback for reliable audio generation
- Adjustable speech speed and controls

**📱 Interactive Demonstrations**:
- Clickable example cards showing different techniques
- Real-time visual feedback on selections
- Progressive disclosure of accessibility features

## Backend Functions

The `backend.py` module provides:

- `simplify_text_with_nlp()` - Main text simplification with noun preservation
- `generate_tts_audio()` - TTS generation with fallback
- `convert_english_to_indic_lang()` / `convert_indic_lang_to_english()` - Translation
- `highlight_nouns_with_fallback()` - POS-based noun highlighting

## Configuration

### Environment Variables

Create a `.env` file for custom configurations:

```bash
# Model cache directory
TRANSFORMERS_CACHE=/path/to/cache

# TTS model paths
FASTSPEECH_PATH=/path/to/Fastspeech2_HS

# Streamlit settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### Model Downloads

The app automatically downloads required models:
- Facebook NLLB-200 distilled (1.3B parameters)
- Stanza Telugu POS tagger
- FastSpeech2_HS (if available)

Models are cached locally after first download.

## Development

### Running in Development Mode

```bash
# Enable debug mode
streamlit run frontend.py --logger.level=debug

# With custom port
streamlit run frontend.py --server.port=8502
```

### Testing Backend Functions

```python
from backend import simplify_text_with_nlp, generate_tts_audio

# Test simplification
text = "This is a complex sentence that needs simplification."
result = simplify_text_with_nlp(text, target_words=20)
print(result)

# Test TTS
audio = generate_tts_audio("Hello world", lang='en')
# audio is a BytesIO object
```

### Code Structure

- `frontend.py`: Main app with page routing and UI
- `backend.py`: Core processing functions
- Session state management for user preferences
- Custom CSS for enhanced styling
- Error handling with fallbacks

## Accessibility Features

- **Screen Reader Compatible**: Semantic HTML and ARIA labels
- **Keyboard Navigation**: Full keyboard accessibility
- **High Contrast Options**: Multiple theme support
- **Font Customization**: Adjustable typography settings
- **Reading Assistance**: Visual aids for text comprehension
- **Multilingual Interface**: Native language support

## Troubleshooting

### Common Issues

**Model Download Failures**:
```bash
# Clear cache and retry
rm -rf ~/.cache/huggingface
streamlit run frontend.py
```

**TTS Audio Issues**:
- Ensure FastSpeech2_HS is properly installed
- App falls back to gTTS automatically
- Check system audio permissions

**Memory Issues**:
- NLLB model requires ~2GB RAM
- Use smaller models for constrained environments
- Consider GPU acceleration for better performance

**Streamlit Errors**:
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit
streamlit run frontend.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly with different languages and inputs
5. Commit your changes (`git commit -m 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Open a Pull Request

## Research Context

This application was developed as part of a Human-Computer Interaction (HCI) research project focusing on cognitive accessibility. The `HCI_project_LLM.ipynb` notebook contains the original research and model development work.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for cognitive accessibility research
- Supports users with reading difficulties and learning disabilities
- Leverages state-of-the-art NLP models for multilingual text processing
- Designed with inclusive technology principles