#!/usr/bin/env python
"""
Setup script for the Karteikarten application.
Creates virtual environment, installs dependencies, and initializes the database.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print status."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent)
    if result.returncode != 0:
        print(f"❌ Error: {description} failed!")
        return False
    print(f"✓ {description} completed successfully!")
    return True


def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("  Karteikarten Application Setup")
    print("="*60)
    
    project_root = Path(__file__).parent
    venv_path = project_root / "venv"
    
    # Step 1: Create virtual environment
    if not venv_path.exists():
        print("\n📦 Creating virtual environment...")
        if sys.platform == "win32":
            if not run_command(f"python -m venv venv", "Create venv"):
                return
            pip_cmd = str(venv_path / "Scripts" / "pip")
        else:
            if not run_command("python3 -m venv venv", "Create venv"):
                return
            pip_cmd = str(venv_path / "bin" / "pip")
    else:
        print("\n✓ Virtual environment already exists")
        pip_cmd = "pip" if sys.platform != "win32" else str(venv_path / "Scripts" / "pip")
    
    # Step 2: Upgrade pip
    print("\n📦 Upgrading pip...")
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrade pip")
    
    # Step 3: Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Install dependencies"):
        return
    
    # Step 4: Create .env file if it doesn't exist
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    if not env_file.exists():
        print("\n📝 Creating .env file...")
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✓ .env file created from .env.example")
        else:
            with open(env_file, 'w') as f:
                f.write("""# Datenbank URL
DATABASE_URL=sqlite:///karteikarten.db

# JWT Secret Key (Ändere diesen in Production!)
SECRET_KEY=your-secret-key-change-this-in-production

# App Settings
APP_HOST=0.0.0.0
APP_PORT=8080
APP_DEBUG=False
""")
            print("✓ .env file created")
    else:
        print("✓ .env file already exists")
    
    # Step 5: Initialize database with sample data
    print("\n📊 Initializing database with sample cards...")
    if sys.platform == "win32":
        python_cmd = str(venv_path / "Scripts" / "python")
    else:
        python_cmd = str(venv_path / "bin" / "python")
    
    run_command(f"{python_cmd} -m app.seed_data", "Seed database")
    
    # Success message
    print("\n" + "="*60)
    print("  ✓ Setup completed successfully!")
    print("="*60)
    print("""
To start the application:

  Linux/macOS:
    source venv/bin/activate
    python -m app.main

  Windows:
    venv\\Scripts\\activate
    python -m app.main

Then open http://localhost:8080 in your browser.

Demo credentials:
  Username: demo
  Password: demo123
""")


if __name__ == "__main__":
    main()
