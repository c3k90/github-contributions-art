#!/usr/bin/env python3
"""
GitHub Contributions Art Generator

This script generates text on the GitHub contributions graph by creating commits
on specific dates. It simulates a 7x52 grid (52 weeks, 7 days) and automatically
centers the text. Commits have different intensities based on pixel brightness.
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont


# Simple 5x7 pixel font for letters (A-Z, 0-9, space)
FONT_5X7 = {
    'A': [
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001"
    ],
    'B': [
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110"
    ],
    'C': [
        "01110",
        "10001",
        "10000",
        "10000",
        "10000",
        "10001",
        "01110"
    ],
    'D': [
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110"
    ],
    'E': [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111"
    ],
    'F': [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000"
    ],
    'G': [
        "01110",
        "10001",
        "10000",
        "10111",
        "10001",
        "10001",
        "01111"
    ],
    'H': [
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001"
    ],
    'I': [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "11111"
    ],
    'J': [
        "00111",
        "00010",
        "00010",
        "00010",
        "00010",
        "10010",
        "01100"
    ],
    'K': [
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001"
    ],
    'L': [
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111"
    ],
    'M': [
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001"
    ],
    'N': [
        "10001",
        "11001",
        "10101",
        "10101",
        "10011",
        "10001",
        "10001"
    ],
    'O': [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110"
    ],
    'P': [
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000"
    ],
    'Q': [
        "01110",
        "10001",
        "10001",
        "10001",
        "10101",
        "10010",
        "01101"
    ],
    'R': [
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001"
    ],
    'S': [
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110"
    ],
    'T': [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100"
    ],
    'U': [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110"
    ],
    'V': [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01010",
        "00100"
    ],
    'W': [
        "10001",
        "10001",
        "10001",
        "10101",
        "10101",
        "11011",
        "10001"
    ],
    'X': [
        "10001",
        "10001",
        "01010",
        "00100",
        "01010",
        "10001",
        "10001"
    ],
    'Y': [
        "10001",
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100"
    ],
    'Z': [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "11111"
    ],
    '0': [
        "01110",
        "10011",
        "10101",
        "10101",
        "10101",
        "11001",
        "01110"
    ],
    '1': [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110"
    ],
    '2': [
        "01110",
        "10001",
        "00001",
        "00110",
        "01000",
        "10000",
        "11111"
    ],
    '3': [
        "11111",
        "00010",
        "00100",
        "00010",
        "00001",
        "10001",
        "01110"
    ],
    '4': [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010"
    ],
    '5': [
        "11111",
        "10000",
        "11110",
        "00001",
        "00001",
        "10001",
        "01110"
    ],
    '6': [
        "00110",
        "01000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110"
    ],
    '7': [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000"
    ],
    '8': [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110"
    ],
    '9': [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00010",
        "01100"
    ],
    ' ': [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000"
    ]
}


class GitHubContributionsArt:
    """Generate text art on GitHub contributions graph."""
    
    GRID_WIDTH = 52  # 52 weeks
    GRID_HEIGHT = 7  # 7 days (Sunday to Saturday)
    CHAR_WIDTH = 5
    CHAR_HEIGHT = 7
    CHAR_SPACING = 1
    
    def __init__(self, text: str, repo_path: str = "./contribution_repo"):
        """
        Initialize the contributions art generator.
        
        Args:
            text: Text to display on the contribution graph
            repo_path: Path where the git repository will be created
        """
        self.text = text.upper()
        self.repo_path = repo_path
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        
    def text_to_grid(self) -> List[List[int]]:
        """
        Convert text to a grid representation with automatic centering.
        
        Returns:
            2D list representing the contribution grid
        """
        # Calculate text dimensions
        text_width = 0
        for char in self.text:
            if char in FONT_5X7:
                text_width += self.CHAR_WIDTH + self.CHAR_SPACING
        text_width -= self.CHAR_SPACING  # Remove trailing spacing
        
        # Calculate starting position to center text
        start_x = max(0, (self.GRID_WIDTH - text_width) // 2)
        start_y = 0  # Text height is fixed at 7, matching grid height
        
        # Render text to grid
        current_x = start_x
        for char in self.text:
            if char in FONT_5X7:
                char_pattern = FONT_5X7[char]
                for y, row in enumerate(char_pattern):
                    for x, pixel in enumerate(row):
                        grid_x = current_x + x
                        grid_y = start_y + y
                        if 0 <= grid_x < self.GRID_WIDTH and 0 <= grid_y < self.GRID_HEIGHT:
                            # Convert character '1' to intensity value
                            self.grid[grid_y][grid_x] = int(pixel)
                current_x += self.CHAR_WIDTH + self.CHAR_SPACING
        
        return self.grid
    
    def create_git_repo(self):
        """Create and initialize a git repository."""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        
        os.chdir(self.repo_path)
        
        # Initialize git repo if not already initialized
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "config", "user.name", "Contributions Art"], check=True)
            subprocess.run(["git", "config", "user.email", "art@contributions.local"], check=True)
    
    def make_commit(self, date: datetime, intensity: int):
        """
        Make a commit on a specific date with given intensity.
        
        Args:
            date: Date for the commit
            intensity: Number of commits to make (1-4 for different intensities)
        """
        if intensity == 0:
            return
        
        # Map intensity: 1 means pixel is on, create multiple commits for visibility
        commits_count = min(intensity * 3, 10)  # 3-10 commits per active pixel
        
        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        
        for i in range(commits_count):
            # Create a file with timestamp to ensure unique commits
            filename = f"commit_{date.strftime('%Y%m%d')}_{i}.txt"
            with open(filename, "w") as f:
                f.write(f"Commit {i} on {date_str}\n")
            
            subprocess.run(["git", "add", filename], check=True, capture_output=True)
            
            # Set the commit date
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str
            
            subprocess.run(
                ["git", "commit", "-m", f"Contribution art commit {i}"],
                env=env,
                check=True,
                capture_output=True
            )
    
    def generate_contributions(self, start_date: datetime = None):
        """
        Generate contributions based on the text grid.
        
        Args:
            start_date: Starting date for contributions (defaults to 52 weeks ago from today)
        """
        if start_date is None:
            # Start from 52 weeks ago, on a Sunday
            today = datetime.now()
            start_date = today - timedelta(weeks=52)
            # Adjust to previous Sunday
            start_date = start_date - timedelta(days=start_date.weekday() + 1)
            if start_date.weekday() != 6:  # If not Sunday
                start_date = start_date - timedelta(days=(start_date.weekday() + 1) % 7)
        
        print(f"Generating contributions starting from {start_date.strftime('%Y-%m-%d')}...")
        print(f"Text: '{self.text}'")
        print("\nGrid visualization:")
        self.visualize_grid()
        
        # Create git repository
        self.create_git_repo()
        
        # Generate commits based on grid
        for week in range(self.GRID_WIDTH):
            for day in range(self.GRID_HEIGHT):
                intensity = self.grid[day][week]
                if intensity > 0:
                    commit_date = start_date + timedelta(weeks=week, days=day)
                    self.make_commit(commit_date, intensity)
        
        print(f"\n✓ Successfully generated {self.count_commits()} commits!")
        print(f"✓ Repository created at: {os.path.abspath(self.repo_path)}")
        print("\nTo view the contributions:")
        print(f"  cd {self.repo_path}")
        print("  git log --oneline | wc -l")
        
    def visualize_grid(self):
        """Print a visual representation of the grid."""
        print("  " + "".join([str(i % 10) for i in range(self.GRID_WIDTH)]))
        for y in range(self.GRID_HEIGHT):
            row_str = "".join(["█" if self.grid[y][x] > 0 else "·" for x in range(self.GRID_WIDTH)])
            print(f"{y} {row_str}")
    
    def count_commits(self) -> int:
        """Count total number of commits in the grid."""
        total = 0
        for row in self.grid:
            for cell in row:
                if cell > 0:
                    total += min(cell * 3, 10)
        return total
    
    def generate(self, start_date: datetime = None):
        """
        Main method to generate the contributions art.
        
        Args:
            start_date: Starting date for contributions (defaults to 52 weeks ago)
        """
        print("=" * 60)
        print("GitHub Contributions Art Generator")
        print("=" * 60)
        
        # Convert text to grid
        self.text_to_grid()
        
        # Generate contributions
        self.generate_contributions(start_date)
        
        print("=" * 60)


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python contributions_art.py <text> [repo_path]")
        print("\nExample:")
        print("  python contributions_art.py 'HELLO'")
        print("  python contributions_art.py 'CODE' ./my_art_repo")
        sys.exit(1)
    
    text = sys.argv[1]
    repo_path = sys.argv[2] if len(sys.argv) > 2 else "./contribution_repo"
    
    # Validate text length
    char_width = sum(5 + 1 for c in text.upper() if c in FONT_5X7) - 1
    if char_width > 52:
        print(f"Error: Text '{text}' is too long ({char_width} columns, max 52)")
        print("Try a shorter text or fewer characters.")
        sys.exit(1)
    
    # Validate characters
    invalid_chars = [c for c in text.upper() if c not in FONT_5X7]
    if invalid_chars:
        print(f"Error: Unsupported characters: {', '.join(invalid_chars)}")
        print(f"Supported characters: A-Z, 0-9, space")
        sys.exit(1)
    
    generator = GitHubContributionsArt(text, repo_path)
    generator.generate()


if __name__ == "__main__":
    main()
