#!/usr/bin/env python3

import os
import sys
import subprocess
import importlib
from pathlib import Path


def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'torch',
        'transformers',
        'scikit-learn',
        'flask',
        'numpy',
        'pandas',
        'spacy',
        'datasets',
        'nltk'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package}")

    return missing_packages


def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def download_spacy_model():
    """Download required spaCy model"""
    print("Downloading spaCy model...")

    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✓ spaCy model downloaded successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to download spaCy model")
        return False


def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")

    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✓ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to download NLTK data: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = [
        'models',
        'logs',
        'data',
        'results'
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")


def run_tests():
    """Run basic tests to verify installation"""
    print("Running basic tests...")

    try:
        # Test basic imports
        from src.models.abuse_detector import AbuseDetector
        from src.models.crisis_intervention import CrisisIntervention
        from src.models.escalation_detector import EscalationDetector
        from src.models.content_filter import ContentFilter

        print("✓ Model imports successful")

        # Test basic functionality
        crisis_detector = CrisisIntervention()
        result = crisis_detector.assess_crisis_level("I'm feeling okay today")

        if 'crisis_detected' in result:
            print("✓ Basic functionality test passed")
        else:
            print("✗ Basic functionality test failed")
            return False

        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("AI Safety POC - Setup Script")
    print("=" * 40)

    # Check dependencies
    print("\n1. Checking dependencies...")
    missing_packages = check_dependencies()

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        if input("Install missing packages? (y/n): ").lower() == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("Please install missing packages manually")
            sys.exit(1)

    # Create directories
    print("\n2. Creating directories...")
    create_directories()

    # Download models and data
    print("\n3. Downloading models and data...")
    if not download_spacy_model():
        print("Warning: spaCy model download failed")

    if not download_nltk_data():
        print("Warning: NLTK data download failed")

    # Run tests
    print("\n4. Running tests...")
    if not run_tests():
        print("Warning: Some tests failed")

    print("\n" + "=" * 40)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. Train models: python scripts/train_models.py")
    print("2. Run demo: python demo.py")
    print("3. Start API: python src/api/app.py")
    print("4. Evaluate: python scripts/evaluate_models.py")


if __name__ == "__main__":
    main()