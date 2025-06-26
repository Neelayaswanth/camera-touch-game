# Camera Touch Game - Level System

A fun camera-based game where you need to touch a moving object with your body using your webcam! The game displays your camera feed with game objects overlaid on top, creating an augmented reality experience. Complete 5 increasingly difficult levels with customizable settings!

## Features

- **Level Selection Menu** - Choose your starting level and star size before playing
- **Real-time webcam feed** as the game background
- **Overlay game objects** (star, collision area) on top of your camera view
- **5 Progressive Levels** with increasing difficulty
- **Customizable Star Sizes** - Small, Medium, Large, Extra Large
- **Motion tracking** using MediaPipe pose estimation
- **Moving target object** that changes color and speed per level
- **Collision detection** between your body and the target
- **Timer** showing how long it takes to complete each level
- **Visual feedback** showing your movement trail
- **Augmented reality experience** - see yourself and game objects together

## Level System

### Level Progression:
- **Level 1**: Yellow star, slow speed (2.0)
- **Level 2**: Orange star, medium speed (3.0)
- **Level 3**: Red star, fast speed (4.0)
- **Level 4**: Purple star, very fast speed (5.0)
- **Level 5**: Cyan star, fastest speed (6.0)

### Star Size Options:
- **Small**: 15px - Most challenging
- **Medium**: 20px - Balanced difficulty
- **Large**: 25px - Easier target
- **Extra Large**: 30px - Easiest target

## Requirements

- Python 3.7 or higher
- Webcam
- Good lighting for pose detection

## Installation

### Step 1: Install Python Dependencies

Install the required packages:

```bash
pip install opencv-python mediapipe pygame numpy
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Game

```bash
python camera_game_levels.py
```

## How to Play

### Level Selection Menu:
1. **Start the game** by running `python camera_game_levels.py`
2. **Select your starting level** using UP/DOWN arrow keys
3. **Choose star size** using LEFT/RIGHT arrow keys
4. **Press ENTER** to start the game

### Gameplay:
1. **Stand in front of your webcam** with good lighting
2. **Move your body** to control your on-screen position
3. **Touch the colored star** that's bouncing around the screen
4. **Complete each level** to progress to the next (harder) level
5. **When you complete all 5 levels**, you win the game!
6. **Press SPACE** to continue to next level or restart after winning
7. **Press ESC** to quit

## Game Controls

### Menu Controls:
- **UP/DOWN arrows** - Select starting level
- **LEFT/RIGHT arrows** - Select star size
- **ENTER** - Start game
- **ESC** - Quit

### Game Controls:
- **Move your body** - Control your on-screen position
- **SPACE** - Continue to next level or restart game
- **ESC** - Quit the game

## Tips for Better Performance

- Ensure good lighting in your room
- Stand at a reasonable distance from the camera (3-6 feet)
- Wear clothing that contrasts with your background
- Make sure your full body is visible in the camera frame
- Close other applications that might be using the camera
- Choose a star size that matches your skill level

## Technical Details

- Uses **MediaPipe** for real-time pose estimation
- **OpenCV** for webcam capture and image processing
- **Pygame** for game rendering and collision detection
- **Threading** for smooth camera processing
- **Overlay rendering** - game objects drawn on top of camera feed
- **Level progression system** with configurable difficulty
- **Customizable star sizes** for different skill levels

## Troubleshooting

### Camera Issues
- **Camera not detected**: Make sure your webcam is connected and not being used by another application
- **Poor tracking**: Improve lighting and ensure your full body is visible
- **Performance issues**: Close other applications that might be using the camera

### Installation Issues
- **Python version error**: Make sure you have Python 3.7 or higher installed
- **Package installation fails**: Try running `pip install --upgrade pip` first
- **MediaPipe issues**: Make sure you have a compatible Python version

### Game Performance
- **Low frame rate**: Reduce the camera resolution or close other applications
- **Tracking lag**: Ensure good lighting and stand closer to the camera
- **Game crashes**: Check that all dependencies are properly installed

## File Structure

```
├── camera_game_levels.py    # Main game file (5-level system with menu)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Game Features

- **Level Selection Menu**: Choose your starting level and star size
- **Augmented Reality**: See yourself and game objects in the same window
- **Real-time tracking**: Your body position is tracked in real-time
- **Progressive difficulty**: Each level gets harder with faster stars
- **Customizable challenge**: Choose star size to match your skill level
- **Color-coded levels**: Each level has a different colored star
- **Visual feedback**: Movement trail shows your recent positions
- **Collision detection**: Touch the star to complete each level
- **Timer**: Track how long it takes to complete each level
- **Level completion screens**: See your progress and time for each level

## Level Completion

- **Level 1-4**: Shows completion time and prompts to continue
- **Level 5**: Shows game completion with total time and restart option
- **Progressive challenge**: Each level increases speed
- **Custom star size**: Your chosen star size applies to all levels
- **Visual indicators**: UI shows current level, speed, and star size

## Customization Options

- **Starting Level**: Begin at any level (1-5)
- **Star Size**: Choose from 4 different sizes
- **Difficulty Scaling**: Speed increases with each level
- **Visual Preferences**: Different colored stars per level

Enjoy the game! 🎮 