#!/usr/bin/env python
import sys
import warnings
import argparse
import os
from datetime import datetime
from typing import Dict, Any

from game_devs.crew import GameDevs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def setup_output_directories():
    """Create the output directory structure for the human review workflow."""
    directories = [
        "outputs/logs",
        "outputs/pitch",
        "outputs/design",
        "outputs/technical",
        "outputs/final",
        "outputs/review"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def get_default_inputs() -> Dict[str, Any]:
    """
    Get default input configuration for the crew.
    These inputs are used to populate the {game} and other placeholders in YAML configurations.
    """
    return {
        "game": "Casual RTS Commander",
        "genre": "Real-Time Strategy",
        "platform": "PC/Mobile",
        "target_audience": "Casual gamers aged 18-35",
        "development_timeline": "6-12 months",
        "team_size": "Solo developer",
        "scope": "Small to medium scope project"
    }

def get_casual_rts_inputs() -> Dict[str, Any]:
    """Example inputs for a casual RTS game (from optimization document)."""
    return {
        "game": "Casual RTS Commander",
        "genre": "Real-Time Strategy",
        "platform": "PC and Mobile",
        "target_audience": "Casual gamers who want strategic gameplay without overwhelming complexity",
        "development_timeline": "8-10 months",
        "team_size": "Solo developer",
        "scope": "Medium scope - focused on core RTS mechanics with casual accessibility"
    }

def get_puzzle_platformer_inputs() -> Dict[str, Any]:
    """Example inputs for a puzzle platformer game."""
    return {
        "game": "Mind Shift",
        "genre": "Puzzle Platformer",
        "platform": "PC/Console",
        "target_audience": "Puzzle game enthusiasts and platformer fans",
        "development_timeline": "6-8 months",
        "team_size": "Solo developer",
        "scope": "Small scope - focused on innovative puzzle mechanics"
    }

def get_roguelike_inputs() -> Dict[str, Any]:
    """Example inputs for a roguelike game."""
    return {
        "game": "Dungeon Codex",
        "genre": "Roguelike",
        "platform": "PC/Mobile",
        "target_audience": "Roguelike enthusiasts and RPG fans",
        "development_timeline": "10-12 months",
        "team_size": "Solo developer",
        "scope": "Medium scope - procedural generation with deep systems"
    }

def parse_arguments():
    """Parse command line arguments for different game configurations."""
    parser = argparse.ArgumentParser(description="GameDevs CrewAI - Generate professional game design documents")

    parser.add_argument(
        "--game-type",
        choices=["default", "casual-rts", "puzzle-platformer", "roguelike", "custom"],
        default="default",
        help="Select predefined game type configuration"
    )

    parser.add_argument(
        "--game-name",
        type=str,
        help="Custom game name (used with --game-type=custom)"
    )

    parser.add_argument(
        "--genre",
        type=str,
        help="Game genre (used with --game-type=custom)"
    )

    parser.add_argument(
        "--platform",
        type=str,
        help="Target platform (used with --game-type=custom)"
    )

    parser.add_argument(
        "--audience",
        type=str,
        help="Target audience (used with --game-type=custom)"
    )

    parser.add_argument(
        "--timeline",
        type=str,
        help="Development timeline (used with --game-type=custom)"
    )

    parser.add_argument(
        "--team-size",
        type=str,
        default="Solo developer",
        help="Team size (used with --game-type=custom)"
    )

    parser.add_argument(
        "--scope",
        type=str,
        help="Project scope (used with --game-type=custom)"
    )

    parser.add_argument(
        "--production-models",
        action="store_true",
        help="Use production-grade Claude models (Sonnet 3.5) instead of cost-effective testing models (Haiku 3.5)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()

def get_inputs_from_args(args) -> Dict[str, Any]:
    """Convert command line arguments to input configuration."""
    if args.game_type == "casual-rts":
        return get_casual_rts_inputs()
    elif args.game_type == "puzzle-platformer":
        return get_puzzle_platformer_inputs()
    elif args.game_type == "roguelike":
        return get_roguelike_inputs()
    elif args.game_type == "custom":
        if not args.game_name:
            raise ValueError("--game-name is required when using --game-type=custom")

        return {
            "game": args.game_name,
            "genre": args.genre or "Unknown",
            "platform": args.platform or "PC",
            "target_audience": args.audience or "General gaming audience",
            "development_timeline": args.timeline or "6-12 months",
            "team_size": args.team_size,
            "scope": args.scope or "Medium scope project"
        }
    else:
        return get_default_inputs()

def print_workflow_info():
    """Print information about the human review workflow."""
    print("\n" + "="*80)
    print("🎮 CREWAI GAMEDEVS - HUMAN REVIEW WORKFLOW")
    print("="*80)
    print()
    print("This workflow includes strategic human review points:")
    print("  1. 📝 Pitch Review - Review and refine the game concept")
    print("  2. 🎯 Gameplay Review - Review and refine the game mechanics")
    print("  3. 📋 Final GDD Review - Final review of the complete document")
    print()
    print("During each review point, you'll be prompted to:")
    print("  • Provide feedback on the generated content")
    print("  • Suggest improvements or changes")
    print("  • Approve or request revisions")
    print()
    print("The workflow will pause at each review point waiting for your input.")
    print("="*80)
    print()

def print_model_info(use_production_models: bool):
    """Print information about the Claude models being used."""
    print("🤖 Claude Model Configuration:")
    if use_production_models:
        print("  Model: Claude Sonnet 3.5 (claude-3-5-sonnet-20241022)")
        print("  Tier: Production-grade quality")
        print("  Cost: $3/MTok input, $15/MTok output")
        print("  Features: High intelligence, superior reasoning")
    else:
        print("  Model: Claude Haiku 3.5 (claude-3-5-haiku-20241022)")
        print("  Tier: Cost-effective testing")
        print("  Cost: $0.80/MTok input, $4/MTok output")
        print("  Features: Fast responses, good quality")
    print()

def main():
    """Main execution function with enhanced input handling and human review workflow support."""
    try:
        # Parse command line arguments
        args = parse_arguments()

        # Set production models environment variable
        if args.production_models:
            os.environ['USE_PRODUCTION_MODELS'] = 'true'

        # Setup output directories
        print("Setting up output directories...")
        setup_output_directories()

        # Print workflow information
        print_workflow_info()

        # Print model information
        print_model_info(args.production_models)

        # Get inputs based on arguments
        inputs = get_inputs_from_args(args)

        # Print configuration
        print("🔧 Configuration:")
        print(f"  Game: {inputs['game']}")
        print(f"  Genre: {inputs['genre']}")
        print(f"  Platform: {inputs['platform']}")
        print(f"  Target Audience: {inputs['target_audience']}")
        print(f"  Timeline: {inputs['development_timeline']}")
        print(f"  Team Size: {inputs['team_size']}")
        print(f"  Scope: {inputs['scope']}")
        print()

        # Environment check
        if not os.getenv('ANTHROPIC_API_KEY'):
            print("⚠️  WARNING: ANTHROPIC_API_KEY environment variable not found.")
            print("   Please set your Anthropic API key to use Claude models.")
            print("   Example: export ANTHROPIC_API_KEY=your_api_key_here")
            print()

        # Initialize and run the crew
        print("🚀 Starting GameDevs CrewAI workflow...")
        print("Note: This workflow includes human review points where you'll be prompted for feedback.")
        print()

        crew = GameDevs().crew()

        # Start the crew with proper input handling
        start_time = datetime.now()
        result = crew.kickoff(inputs=inputs)
        end_time = datetime.now()

        # Print results
        print("\n" + "="*80)
        print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"⏱️  Total execution time: {end_time - start_time}")
        print(f"📁 Output files saved to: outputs/")
        print(f"📋 Final GDD: outputs/final/{inputs['game']}_final_gdd.md")
        print(f"📝 Execution log: outputs/logs/crew_execution.log")
        print()
        print("Result:")
        print(result)
        print("="*80)

    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
        print("Partial results may be available in the outputs/ directory")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check the configuration and try again.")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
