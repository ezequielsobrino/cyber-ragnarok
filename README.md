# LLM Battle Arena

A Python framework for creating AI model competitions through various games, generating entertaining and visually appealing battle videos. Currently featuring Tic-Tac-Toe battles between different Language Models (LLMs), with plans to expand to chess, checkers, and more games.

## Features

- 🎮 Multiple Game Support (extensible architecture)
  - Currently: Tic-Tac-Toe
  - Planned: Chess, Checkers, and more
- 🤖 LLM Integration
  - Battle different versions of language models
  - Compare decision-making capabilities
  - Analyze strategic thinking
- 🎥 Professional Tournament Videos
  - Round introductions
  - Live game animations
  - Score tracking
  - Winner announcements
  - Background music
- 📊 Performance Analytics
  - Win rates
  - Decision patterns
  - Tournament statistics

## Project Structure

```
llm-battle-arena/
├── main.py                      # Main entry point
├── brains/                      # AI decision-making modules
│   └── tic_tac_toe_brain.py    # TicTacToe LLM integration
├── games/                       # Game implementations
│   └── tic_tac_toe.py          # TicTacToe game logic
├── tournament_video_maker.py    # Video generation system
├── assets/                      # Media resources
│   ├── tic_tac_toe_board.png
│   ├── x_image.png
│   ├── o_image.png
│   └── video_music.mp3
└── requirements.txt
```

## Prerequisites

- Python 3.8+
- FFmpeg
- Required Python packages (see requirements.txt)
- Access to LLM APIs (configuration required)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-battle-arena.git
cd llm-battle-arena
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your LLM API credentials in a `.env` file:
```env
LLM_API_KEY=your_api_key_here
```

## Usage

1. Run a basic tournament:
```bash
python main.py
```

2. Configure tournament settings in `main.py`:
```python
# Example configuration
config = {
    "game": "tictactoe",
    "model1": "llama-3.1-70b-versatile",
    "model2": "llama-3.1-8b-instant",
    "num_games": 10
}
```

The output video will be saved as: `tournament_[model1]_vs_[model2]_[games]games.mp4`

## Extending the Framework

### Adding New Games

1. Create game logic in `games/your_game.py`
2. Implement AI integration in `brains/your_game_brain.py`
3. Add necessary visual assets in `assets/`
4. Update video maker to support new game visualization

Example:
```python
# games/chess.py
class ChessGame(BaseGame):
    def __init__(self):
        super().__init__()
        # Chess-specific implementation
```

### Supporting New LLMs

Add new model support in the brain implementations:

```python
# brains/tic_tac_toe_brain.py
class TicTacToeBrain:
    def add_model(self, model_name, model_config):
        # Implementation for new model support
```

## Logging

Detailed logs are generated for each tournament:
- Tournament progress
- Model decisions
- Game outcomes
- Performance metrics

Format: `tournament_YYYYMMDD_HHMMSS.log`

## Contributing

Contributions are welcome! Especially interested in:
- New game implementations
- LLM integration improvements
- Performance optimizations
- Visual enhancements

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewGame`)
3. Commit changes (`git commit -m 'Add Chess implementation'`)
4. Push to branch (`git push origin feature/NewGame`)
5. Open a Pull Request

## Future Plans

- [ ] Chess implementation
- [ ] Checkers implementation
- [ ] Connect Four
- [ ] Real-time LLM decision visualization
- [ ] Tournament brackets
- [ ] Multi-model tournaments
- [ ] Performance analytics dashboard
- [ ] Web interface for tournament configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.
