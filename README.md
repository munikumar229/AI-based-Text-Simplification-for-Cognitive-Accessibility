# AI-Based Text Simplification for Cognitive Accessibility

A multilingual web application that simplifies text to improve cognitive accessibility for users with reading difficulties. Built with Streamlit, Python, and advanced NLP models.

## ✨ Features

🌐 **Bilingual Support**: English and Telugu languages with intelligent language detection  
🎯 **Personalized Experience**: Questionnaire-guided customization based on user accessibility preferences  
🔧 **Reading Assistance Tools**: Font adjustments, letter spacing, bolding options, and visual themes  
🔊 **Text-to-Speech**: High-quality TTS with adjustable speed control using gTTS and pydub  
📱 **Responsive Design**: Works seamlessly on desktop and mobile devices  
🎨 **Multiple Themes**: Light, Sepia, and Dark modes for comfortable reading  
✨ **Advanced Text Processing**: Noun-preserving simplification, POS tagging, and intelligent summarization  
📝 **Interactive Examples**: Clickable demonstration cards showing different text enhancement techniques  
🎵 **Audio Controls**: Play/pause functionality with speed adjustment (0.25x to 2.0x)  
💾 **Persistent Settings**: User preferences saved across sessions

## 🎥 Demo

Watch a live demo of the application in action: [Demo Video](https://github.com/user-attachments/assets/4071a726-bf71-4d6f-ab0f-7e195b7d9d55)

## 🛠️ Technology Stack

- **Framework**: Streamlit 1.40.1
- **Language**: Python 3.8+
- **NLP Models**: Facebook NLLB-200 (1.3B distilled) for translation
- **POS Tagging**: Stanza for Telugu morphological analysis
- **Text-to-Speech**: gTTS with pydub for speed manipulation
- **Translation**: Transformers library with pre-trained models
- **Database**: SQLite for user preference persistence
- **UI Components**: Streamlit with custom CSS styling

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** and pip/conda
- **Git** for cloning the repository
- **Internet connection** for downloading ML models (first run only)
- **4GB+ RAM** recommended for NLP models

### Installation & Setup

#### Option 1: Using Conda (Recommended)

```bash
# Clone the repository
git clone https://github.com/munikumar229/AI-based-Text-Simplification-for-Cognitive-Accessibility.git
cd AI-based-Text-Simplification-for-Cognitive-Accessibility

# Create and activate conda environment
conda env create -f environment.yml
conda activate text-simplifier

# Run the application
streamlit run frontend.py
```

#### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/munikumar229/AI-based-Text-Simplification-for-Cognitive-Accessibility.git
cd AI-based-Text-Simplification-for-Cognitive-Accessibility

# Install dependencies
pip install streamlit transformers stanza gtts pydub pyttsx3

# Run the application
streamlit run frontend.py
```

The application will open at `http://localhost:8501` and automatically download required ML models on first use.

## 📁 Project Structure

```
├── frontend.py              # Main Streamlit application with UI
├── backend.py               # NLP and TTS processing functions
├── utils.py                 # Utility functions
├── environment.yml          # Conda environment specification
├── user_data.db            # SQLite database for user preferences
├── database.json           # Alternative data storage
├── HCI_project_LLM.ipynb   # Research notebook with AI models
├── Design_Process/         # Design documentation and prototypes
├── Low-Fi-Prototype/       # Early prototype files
├── 1.html                  # Static HTML demonstration files
├── text-simplifier-woz-v3.html
└── README.md               # This file
```

## 📖 Usage

### Application Flow

1. **Welcome Screen**: Introduction and app overview
2. **Language Selection**: Choose between English and తెలుగు (Telugu)
3. **Login**: Enter name or continue as guest
4. **Bold Examples**: Interactive demonstration of bolding techniques
5. **Spacing Examples**: Letter spacing demonstration
6. **Questionnaire**: Answer questions about reading preferences and accessibility needs
7. **Text Input**: Paste text or upload a .txt file (max 10MB)
8. **Processing**: AI-powered text simplification with progress indicator
9. **Results**: View, customize, and listen to simplified text

### Key Features

**🤖 AI-Powered Simplification**:
- Intelligent noun-preserving text summarization
- Sentence selection based on content importance and noun frequency
- Vocabulary simplification with synonym replacement
- Automatic language detection and appropriate processing
- Configurable word count targets (50-300 words)

**🎨 Accessibility Customizations**:
- Font size adjustment (14-30px)
- Line height control (1.2x to 4.0x)
- Letter spacing adjustment (0.0em to 0.3em)
- Bold first N characters of words (1-3 characters)
- Color-coded letters for enhanced readability
- Multiple visual themes (Light/Sepia/Dark)

**🔊 Advanced Audio Features**:
- gTTS-powered text-to-speech for both languages
- Adjustable playback speed (0.25x to 2.0x)
- HTML5 audio player with play/pause controls
- Audio persistence across page refreshes
- Mute/unmute functionality

**📱 Interactive Demonstrations**:
- Clickable example cards showing different techniques
- Real-time visual feedback on selections
- Progressive disclosure of accessibility features
- Before/after text comparisons

## 🔧 Backend Functions

The `backend.py` module provides core functionality:

### Text Processing
- `simplify_text_with_nlp()` - Main text simplification with noun preservation
- `highlight_nouns_with_fallback()` - POS-based noun highlighting for Telugu
- `_create_noun_preserving_summary()` - Intelligent summarization algorithm
- `_basic_simplify_text()` - Vocabulary and sentence structure simplification

### Audio & Translation
- `generate_tts_audio()` - TTS generation with speed control using gTTS + pydub
- `convert_english_to_indic_lang()` / `convert_indic_lang_to_english()` - NLLB translation
- `add_spacing()` - Letter spacing utility for dyslexia support

### Utilities
- Lazy loading for translation models to reduce memory usage
- Error handling with fallbacks for robust operation
- Language detection and appropriate model selection

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

## ⚙️ Configuration

### Environment Variables

Create a `.env` file for custom configurations:

```bash
# Model cache directory
TRANSFORMERS_CACHE=/path/to/cache

# Streamlit settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Model Downloads

The app automatically downloads required models on first run:
- **Facebook NLLB-200 distilled (1.3B)**: Multilingual translation (~2GB)
- **Stanza Telugu POS tagger**: Morphological analysis for Telugu
- **gTTS models**: Text-to-speech (downloaded per request)

Models are cached locally in `~/.cache/huggingface/` and `~/.cache/stanza/`.

## 🛠️ Development

### Running in Development Mode

```bash
# Enable debug logging
streamlit run frontend.py --logger.level=debug

# Custom port and settings
streamlit run frontend.py --server.port=8502 --server.headless=false
```

### Testing Backend Functions

```python
from backend import simplify_text_with_nlp, generate_tts_audio

# Test text simplification
text = "This is a complex sentence that needs simplification for better accessibility."
result = simplify_text_with_nlp(text, target_language='eng_Latn', target_words=20)
print("Simplified:", result)

# Test TTS generation
audio = generate_tts_audio("Hello world", lang='en', speed=1.5)
print(f"Generated audio: {len(audio.getvalue())} bytes")
```

### Code Structure

- **`frontend.py`**: Complete Streamlit application with routing and UI
- **`backend.py`**: Core processing functions with error handling
- **Session state management**: Persistent user preferences across pages
- **Custom CSS**: Enhanced styling for accessibility
- **Database integration**: SQLite for user data persistence

## 🔍 Troubleshooting

### Common Issues

**Model Download Failures**:
```bash
# Clear caches and retry
rm -rf ~/.cache/huggingface ~/.cache/stanza
conda activate text-simplifier  # or your environment
streamlit run frontend.py
```

**Memory Issues**:
- NLLB model requires ~2GB RAM
- Close other applications during first run
- Consider using smaller models for constrained environments

**Audio Issues**:
- Ensure internet connection for gTTS
- Check system audio permissions
- Audio files are generated on-demand

**Streamlit Errors**:
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit
streamlit cache clear
streamlit run frontend.py
```

**Database Issues**:
```bash
# Reset user data
rm user_data.db database.json
# App will recreate with defaults
```

### Performance Tips

- **First run**: May take 5-10 minutes for model downloads
- **Subsequent runs**: Load in 30-60 seconds
- **GPU acceleration**: Install PyTorch with CUDA for faster processing
- **Memory optimization**: Models use lazy loading to reduce RAM usage

## ♿ Accessibility Features

- **Screen Reader Compatible**: Semantic HTML and proper labeling
- **Keyboard Navigation**: Full keyboard accessibility support
- **High Contrast Options**: Multiple theme support (Light/Sepia/Dark)
- **Font Customization**: Adjustable typography (size, spacing, weight)
- **Reading Assistance**: Visual aids including bolding and color coding
- **Multilingual Interface**: Native language support (English/Telugu)
- **Audio Support**: Text-to-speech with speed control
- **Progressive Enhancement**: Features work without JavaScript

## 📊 Research Context

This application was developed as part of a Human-Computer Interaction (HCI) research project focusing on cognitive accessibility for users with reading difficulties and learning disabilities.

### Key Research Areas

- **Text Simplification Algorithms**: Noun-preserving summarization techniques
- **Multilingual Accessibility**: Supporting both English and Telugu users
- **User-Centered Design**: Questionnaire-driven personalization
- **Audio Accessibility**: TTS integration with speed control
- **Visual Accessibility**: Font and spacing adjustments for readability

The `HCI_project_LLM.ipynb` notebook contains the original research methodology, model development, and evaluation metrics.

## 🤝 Contributing

We welcome contributions to improve accessibility and add new features!

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/AI-based-Text-Simplification-for-Cognitive-Accessibility.git`
3. Set up the environment: `conda env create -f environment.yml`
4. Create a feature branch: `git checkout -b feature/your-feature-name`
5. Make your changes with proper testing
6. Commit changes: `git commit -m 'Add: brief description of changes'`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request with detailed description

### Contribution Guidelines

- **Code Style**: Follow PEP 8 Python conventions
- **Testing**: Test with both English and Telugu inputs
- **Accessibility**: Ensure all new features are accessible
- **Documentation**: Update README and docstrings for new features
- **Performance**: Consider memory and processing time implications
- **Cross-platform**: Test on different operating systems

### Areas for Contribution

- **New Languages**: Add support for additional Indian languages
- **Enhanced TTS**: Integrate better TTS engines or voices
- **Accessibility Features**: New reading assistance tools
- **Performance Optimization**: Faster model loading and processing
- **UI/UX Improvements**: Better user interface design
- **Testing**: Comprehensive test suite development

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Research Team**: For the HCI study on cognitive accessibility
- **Open Source Community**: For the amazing libraries and models
- **Users**: For feedback and feature requests
- **Facebook AI**: For the NLLB translation models
- **Stanford NLP**: For the Stanza POS tagging library

## 📞 Support

For questions, issues, or feature requests:

1. Check the [Issues](https://github.com/munikumar229/AI-based-Text-Simplification-for-Cognitive-Accessibility/issues) page
2. Create a new issue with detailed description
3. Include your environment details and steps to reproduce

---

**Built with ❤️ for cognitive accessibility and inclusive technology**

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