#!/usr/bin/env python
import sys
import warnings
import argparse
from datetime import datetime
from typing import Dict, Any

from game_devs.crew import GameDevs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def get_default_inputs() -> Dict[str, Any]:
    """
    Get default input configuration for the crew.
    These inputs are used to populate the {game} and other placeholders in YAML configurations.
    """
    return {
        'game': 'Casual RTS Adventure',
        'genre': 'Real-Time Strategy',
        'platform': 'PC',
        'target_audience': 'Casual gamers',
        'development_timeline': '6-12 months',
        'team_size': 'Solo developer',
        'project_scope': 'Prototype and early development'
    }

def get_casual_rts_inputs() -> Dict[str, Any]:
    """
    Get input configuration for the casual RTS example from the optimization document.
    """
    return {
        'game': 'Casual RTS: Crystal Kingdoms',
        'genre': 'Casual Real-Time Strategy',
        'platform': 'PC',
        'target_audience': 'Casual strategy game players',
        'development_timeline': '8 months',
        'team_size': 'Solo developer',
        'project_scope': 'Full prototype with 3 playable scenarios'
    }

def get_platformer_inputs() -> Dict[str, Any]:
    """
    Get input configuration for a platformer game example.
    """
    return {
        'game': 'Rapid Prototype Platformer',
        'genre': 'Platformer',
        'platform': 'PC',
        'target_audience': 'Indie game enthusiasts',
        'development_timeline': '6 months',
        'team_size': 'Solo developer',
        'project_scope': 'Rapid prototype with core mechanics'
    }

def run():
    """
    Run the crew for a specific game prototype. Create a game design document.
    """
    print("🎮 Starting Game Design Document Generation...")
    print("=" * 50)

    # Use default inputs - can be customized for different game types
    inputs = get_default_inputs()

    print(f"Game: {inputs['game']}")
    print(f"Genre: {inputs['genre']}")
    print(f"Platform: {inputs['platform']}")
    print(f"Timeline: {inputs['development_timeline']}")
    print("=" * 50)

    try:
        result = GameDevs().crew().kickoff(inputs=inputs)

        print("\n✅ Game Design Document generation completed successfully!")
        print(f"🕐 Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📁 Check the 'out/' directory for generated files.")

        return result

    except Exception as e:
        print(f"❌ An error occurred while running the crew: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")

def run_casual_rts():
    """
    Run the crew specifically for the casual RTS example from the optimization document.
    """
    print("🎮 Starting Casual RTS Game Design Document Generation...")
    print("=" * 50)

    inputs = get_casual_rts_inputs()

    print(f"Game: {inputs['game']}")
    print(f"Genre: {inputs['genre']}")
    print(f"Platform: {inputs['platform']}")
    print(f"Timeline: {inputs['development_timeline']}")
    print("=" * 50)

    try:
        result = GameDevs().crew().kickoff(inputs=inputs)

        print("\n✅ Casual RTS Game Design Document generation completed successfully!")
        print(f"🕐 Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📁 Check the 'out/' directory for generated files.")

        return result

    except Exception as e:
        print(f"❌ An error occurred while running the crew: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations on a specific game prototype.
    """
    inputs = get_platformer_inputs()

    print(f"🎯 Training crew with {inputs['game']}...")

    try:
        GameDevs().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        print("✅ Training completed successfully!")

    except Exception as e:
        print(f"❌ An error occurred while training the crew: {e}")
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    print(f"🔄 Replaying crew execution from task: {sys.argv[1]}")

    try:
        GameDevs().crew().replay(task_id=sys.argv[1])
        print("✅ Replay completed successfully!")

    except Exception as e:
        print(f"❌ An error occurred while replaying the crew: {e}")
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results for a specific game prototype.
    """
    inputs = get_platformer_inputs()

    print(f"🧪 Testing crew with {inputs['game']}...")

    try:
        GameDevs().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        print("✅ Testing completed successfully!")

    except Exception as e:
        print(f"❌ An error occurred while testing the crew: {e}")
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    # Allow running specific configurations from command line
    if len(sys.argv) > 1 and sys.argv[1] == "casual_rts":
        run_casual_rts()
    else:
        run()
