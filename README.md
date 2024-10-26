# AI Model Arena: Cyber Ragnarok

A platform for creating epic video battles between different Large Language Models (LLMs) through strategic games. Currently featuring Tic Tac Toe matches with high-quality video generation of the competitions.

## 🎮 Current Game Support

### Tic Tac Toe
- Strategic decision-making with full game analysis
- Move validation and state management
- Fork detection and critical move analysis
- Win condition verification

## 🤖 Supported LLM Providers

The platform supports multiple LLM providers through a modular provider system:
- Anthropic (Claude models)
- Groq
- OpenAI

## ✨ Key Features

### Battle System
- Model vs Model competitions
- Multiple rounds per match
- Automatic move validation
- Strategy analysis and logging
- Provider factory for easy model integration

### Video Generation
- Epic intro screens with model matchups
- Round-by-round visualization
- Real-time game state rendering
- Score tracking and winner announcements
- Professional video editing with transitions
- Background music integration

### Asset Management
- Dynamic image scaling
- Color overlay effects
- Model-specific imagery
- Board and piece visualization

## 🛠️ Technical Architecture

```
project/
├── assets/             # Asset management and processing
├── brains/             # LLM integration
│   └── providers/      # Different LLM providers
├── config/             # Configuration and settings
├── games/              # Game implementations
├── screens/            # Video screen generators
├── scripts_utils/      # Utility scripts
├── video/             # Video creation and editing
└── main.py            # Main tournament runner
```

## 🎥 Screen Types

- Intro Screen: Epic VS screen with model matchups
- Game Screen: Live game board visualization
- Round Screen: Score tracking and round information
- Winner Screen: Final results and statistics

## 🚀 Getting Started

1. **Installation**
```bash
git clone [repository-url]
cd [project-directory]
pip install -r requirements.txt
```

2. **Configuration**
Create a `.env` file with your API keys:
```env
ANTHROPIC_API_KEY=your_anthropic_key
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
```

3. **Run a Match**
```bash
python main.py
```

## 🎯 Project Structure Highlights

### Core Components
- `TicTacToeBrain`: Handles game strategy and move analysis
- `AssetsManager`: Manages game assets and image processing
- `VideoMaker`: Creates professional match videos
- `ProviderFactory`: Manages LLM provider instantiation

### Screen Components
- `BaseScreen`: Template for all screen types
- `GameScreen`: Renders live gameplay
- `IntroScreen`: Creates epic match intros
- `RoundScreen`: Shows match progress
- `WinnerScreen`: Displays final results

## 📈 Future Enhancements

- Additional game types (Chess, Checkers, etc.)
- Enhanced video effects and transitions
- Tournament bracket system
- Performance analytics dashboard
- Additional LLM provider integration

## 💡 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Anthropic, Groq, and OpenAI for their APIs
- Pygame community for game rendering support
- MoviePy and OpenCV for video processing capabilities