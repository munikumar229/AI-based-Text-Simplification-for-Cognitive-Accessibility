# AI-Based Text Simplification for Cognitive Accessibility

A multilingual web application that simplifies text to improve cognitive accessibility. Built with React, Vite, and Tailwind CSS.

## Features

🌐 **Multilingual Support**: Hindi, Telugu, and Gujarati languages  
🎯 **Personalized Experience**: Questionnaire-guided customization  
🔧 **Accessibility Tools**: Font adjustments, reading assists, and visual themes  
🔊 **Text-to-Speech**: Built-in TTS with language-specific voices  
📱 **Responsive Design**: Works on desktop and mobile devices  
🎨 **Multiple Themes**: Light, Sepia, and Dark modes  
✨ **Reading Assists**: Character highlighting and varṇa bolding for Indic scripts  

## Technology Stack

- **Frontend**: React 18 with Hooks
- **Build Tool**: Vite 4
- **Styling**: Tailwind CSS 3
- **Language**: Modern JavaScript/JSX
- **Development**: ESLint, Hot Module Replacement

## Quick Start

### Prerequisites

- **Node.js 16+** and npm
- **Python 3.8+** and pip  
- **Git LFS** (for FastSpeech2 TTS models)
- **System dependencies**: curl, lsof

### Automated Setup & Start

The easiest way to run the full application with AI backend:

```bash
# Clone the repository
git clone https://github.com/munikumar229/AI-based-Text-Simplification-for-Cognitive-Accessibility.git

# Navigate to project directory
cd AI-based-Text-Simplification-for-Cognitive-Accessibility

# Start everything (frontend + AI backend)
./start.sh
```

This will:
- Install all dependencies (Node.js and Python)
- Set up the AI backend with ML models
- Start both frontend and backend servers
- Open the application at http://localhost:3000

### Manual Setup

#### Frontend Only (Basic Mode)

```bash
# Install frontend dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

#### Full AI Backend Integration

```bash
# 1. Setup backend
cd backend
./setup.sh
cd ..

# 2. Start backend server
cd backend
source backend_env/bin/activate
python main.py &
cd ..

# 3. Start frontend
npm run dev
```

### Stopping the Application

```bash
# Stop all servers
./stop.sh
```

### Build for Production

```bash
# Build frontend
npm run build

# Preview production build
npm run preview

# Backend runs the same in production
cd backend && source backend_env/bin/activate && python main.py
```

## Project Structure

```
├── src/                    # React Frontend
│   ├── components/         # Reusable UI components (future)
│   ├── services/          # API integration services
│   │   └── api.js         # Backend API client
│   ├── utils/             # Utility functions and translations
│   │   └── translations.js # Multilingual content
│   ├── App.jsx           # Main application component
│   ├── main.jsx          # Application entry point
│   └── index.css         # Global styles and Tailwind
├── backend/               # Python AI Backend
│   ├── services/         # AI processing services
│   │   ├── translation_service.py    # NLLB translation
│   │   ├── text_processing_service.py # Text simplification
│   │   └── tts_service.py            # Text-to-Speech
│   ├── main.py           # FastAPI server
│   ├── requirements.txt  # Python dependencies
│   └── setup.sh         # Backend setup script
├── public/               # Static assets
├── dist/                # Production build output
├── HCI_project_LLM.ipynb # Research notebook with AI models
├── start.sh             # Start all services
├── stop.sh              # Stop all services
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── package.json         # Frontend dependencies and scripts
└── README.md            # This file
```

## Usage

### Application Modes

**🤖 AI Mode** (Backend Available):
- Real NLLB translation between languages
- Advanced noun highlighting with NLP
- High-quality FastSpeech2 TTS
- Intelligent text processing

**📱 Offline Mode** (Fallback):
- Client-side text processing
- Web Speech API for TTS
- Basic text transformations
- Full UI functionality

### User Flow

1. **Language Selection**: Choose your preferred language (Hindi, Telugu, or Gujarati)
2. **Accessibility Setup**: Answer questions about reading difficulties
3. **Text Input**: Paste text or upload a .txt file
4. **AI Processing**: Real-time translation and noun highlighting (AI mode)
5. **Customization**: Adjust font size, spacing, and visual preferences
6. **Simplification**: Apply vocabulary simplification and sentence splitting
7. **Reading Assists**: Enable character assists and varṇa bolding
8. **Text-to-Speech**: Listen to the simplified text with native-quality voices

## API Endpoints

The backend provides REST APIs for integration:

### Core APIs
- `GET /health` - Backend health check
- `POST /api/translate` - Multilingual translation  
- `POST /api/simplify` - Complete text simplification pipeline
- `POST /api/process-text` - Text accessibility processing
- `POST /api/tts` - Generate speech audio
- `POST /api/upload-text` - Upload and process text files
- `GET /api/languages` - Get supported languages

### Interactive Documentation
When running the backend, visit http://localhost:8000/docs for complete API documentation with interactive testing.

## Wizard of Oz (WoZ) Features

Press `Shift+W` to access the wizard panel for:
- Preset configurations for different user needs
- Manual text replacement for testing
- Theme switching and feature toggling
- Backend connectivity testing

## Accessibility Features

- **Font Customization**: Size (14-30px), line spacing, letter spacing
- **Visual Themes**: Light, sepia, and dark modes for different preferences
- **Reading Assists**: Bold first characters of words for easier reading
- **Hindi Script Support**: Special character assists for Devanagari
- **Text-to-Speech**: Multi-language voice synthesis
- **Keyboard Navigation**: Full keyboard accessibility

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for cognitive accessibility research and human-computer interaction
- Supports users with reading difficulties and learning disabilities
- Multilingual design for inclusive technology access