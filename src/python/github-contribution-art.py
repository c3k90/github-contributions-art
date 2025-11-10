#!/usr/bin/env python3
"""
GitHub Contributions Art Generator

This script generates text on the GitHub contributions graph by creating commits
on specific dates. It simulates a 7x52 grid (52 weeks, 7 days) and automatically
centers the text. Commits have different intensities based on pixel brightness.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

FONT_5X7 = {
    "A": [
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],
    "B": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110",
    ],
    "C": [
        "01110",
        "10001",
        "10000",
        "10000",
        "10000",
        "10001",
        "01110",
    ],
    "D": [
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110",
    ],
    "E": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ],
    "F": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000",
    ],
    "G": [
        "01110",
        "10001",
        "10000",
        "10111",
        "10001",
        "10001",
        "01111",
    ],
    "H": [
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],
    "I": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "11111",
    ],
    "J": [
        "00111",
        "00010",
        "00010",
        "00010",
        "00010",
        "10010",
        "01100",
    ],
    "K": [
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001",
    ],
    "L": [
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111",
    ],
    "M": [
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001",
    ],
    "N": [
        "10001",
        "11001",
        "10101",
        "10101",
        "10011",
        "10001",
        "10001",
    ],
    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "P": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000",
    ],
    "Q": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10101",
        "10010",
        "01101",
    ],
    "R": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001",
    ],
    "S": [
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110",
    ],
    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
    "U": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "V": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01010",
        "00100",
    ],
    "W": [
        "10001",
        "10001",
        "10001",
        "10101",
        "10101",
        "11011",
        "10001",
    ],
    "X": [
        "10001",
        "10001",
        "01010",
        "00100",
        "01010",
        "10001",
        "10001",
    ],
    "Y": [
        "10001",
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
    "Z": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "11111",
    ],
    "0": [
        "01110",
        "10011",
        "10101",
        "10101",
        "10101",
        "11001",
        "01110",
    ],
    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ],
    "2": [
        "01110",
        "10001",
        "00001",
        "00110",
        "01000",
        "10000",
        "11111",
    ],
    "3": [
        "11111",
        "00010",
        "00100",
        "00010",
        "00001",
        "10001",
        "01110",
    ],
    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010",
    ],
    "5": [
        "11111",
        "10000",
        "11110",
        "00001",
        "00001",
        "10001",
        "01110",
    ],
    "6": [
        "00110",
        "01000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110",
    ],
    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000",
    ],
    "8": [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110",
    ],
    "9": [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00010",
        "01100",
    ],
    " ": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
    ],
}


class GitHubContributionsArt:
    """Generate text art on GitHub contributions graph."""

    GRID_WIDTH = 52
    GRID_HEIGHT = 7
    CHAR_WIDTH = 5
    CHAR_HEIGHT = 7
    CHAR_SPACING = 1

    def __init__(
        self,
        text: str,
        repo_path: str = "./contribution_repo",
        *,
        remote_url: Optional[str] = None,
        branch: str = "main",
        verbose: bool = True,
        git_user_name: str = "Contributions Art",
        git_user_email: str = "art@contributions.local",
    ):
        self.text = text.upper()
        self.repo_path = Path(repo_path).expanduser().resolve()
        self.remote_url = remote_url
        self.branch = branch
        self.verbose = verbose
        self.git_user_name = git_user_name
        self.git_user_email = git_user_email
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.art_dir = self.repo_path / "art"
        self.start_date_used: Optional[datetime] = None

    def log(self, message: str) -> None:
        if self.verbose:
            print(message)

    def git(self, args: List[str], env: Optional[dict] = None) -> subprocess.CompletedProcess:
        stdout = None if self.verbose else subprocess.PIPE
        stderr = None if self.verbose else subprocess.PIPE
        return subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            env=env,
            check=True,
            stdout=stdout,
            stderr=stderr,
        )

    def text_to_grid(self) -> List[List[int]]:
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        text_width = 0
        for char in self.text:
            if char in FONT_5X7:
                text_width += self.CHAR_WIDTH + self.CHAR_SPACING
        if text_width > 0:
            text_width -= self.CHAR_SPACING

        start_x = max(0, (self.GRID_WIDTH - text_width) // 2)
        current_x = start_x

        for char in self.text:
            if char not in FONT_5X7:
                continue
            for y, row in enumerate(FONT_5X7[char]):
                for x, pixel in enumerate(row):
                    grid_x = current_x + x
                    grid_y = y
                    if 0 <= grid_x < self.GRID_WIDTH and 0 <= grid_y < self.GRID_HEIGHT:
                        self.grid[grid_y][grid_x] = int(pixel)
            current_x += self.CHAR_WIDTH + self.CHAR_SPACING

        return self.grid

    def prepare_repository(self) -> None:
        if self.repo_path.exists():
            shutil.rmtree(self.repo_path)
        self.repo_path.mkdir(parents=True, exist_ok=True)

        try:
            self.git(["init", "-b", self.branch])
        except subprocess.CalledProcessError:
            self.git(["init"])
            self.git(["checkout", "-B", self.branch])

        self.git(["config", "user.name", self.git_user_name])
        self.git(["config", "user.email", self.git_user_email])

        if self.remote_url:
            self.git(["remote", "add", "origin", self.remote_url])

        self.art_dir.mkdir(parents=True, exist_ok=True)

    def make_commit(self, date: datetime, intensity: int) -> int:
        if intensity == 0:
            return 0

        commits_count = min(intensity * 3, 10)
        date_str = date.strftime("%Y-%m-%d %H:%M:%S")

        for index in range(commits_count):
            file_path = self.art_dir / f"commit_{date.strftime('%Y%m%d')}_{index}.txt"
            file_path.write_text(f"Commit {index} on {date_str}\n", encoding="utf-8")
            relative_path = str(file_path.relative_to(self.repo_path))

            self.git(["add", relative_path])

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str

            self.git(["commit", "-m", f"Contribution art commit {index}"], env=env)

        return commits_count

    def generate_contributions(self, start_date: Optional[datetime] = None) -> int:
        if start_date is None:
            today = datetime.now()
            start_date = today - timedelta(weeks=52)
            start_date = start_date - timedelta(days=(start_date.weekday() + 1) % 7)

        self.start_date_used = start_date
        commit_total = 0

        for week in range(self.GRID_WIDTH):
            for day in range(self.GRID_HEIGHT):
                intensity = self.grid[day][week]
                if intensity > 0:
                    commit_date = start_date + timedelta(weeks=week, days=day)
                    commit_total += self.make_commit(commit_date, intensity)

        return commit_total

    def visualize_grid(self) -> None:
        header = "  " + "".join(str(i % 10) for i in range(self.GRID_WIDTH))
        self.log(header)
        for y in range(self.GRID_HEIGHT):
            row = "".join("█" if self.grid[y][x] > 0 else "·" for x in range(self.GRID_WIDTH))
            self.log(f"{y} {row}")

    def finalize_repository(self) -> None:
        if self.verbose:
            self.git(["status", "--short"])
        if self.remote_url:
            self.git(["push", "--force", "--set-upstream", "origin", self.branch])

    def generate(self, start_date: Optional[datetime] = None) -> dict:
        self.log("=" * 60)
        self.log("GitHub Contributions Art Generator")
        self.log("=" * 60)

        self.text_to_grid()

        if self.verbose:
            self.log("\nGrid visualization:")
            self.visualize_grid()

        self.prepare_repository()
        commit_total = self.generate_contributions(start_date)
        self.finalize_repository()

        summary = {
            "text": self.text,
            "repo_path": str(self.repo_path),
            "start_date": self.start_date_used.isoformat() if self.start_date_used else None,
            "commits": commit_total,
            "remote_url": self.remote_url,
            "branch": self.branch,
        }

        self.log(f"\n✓ Successfully generated {commit_total} commits!")
        self.log(f"✓ Repository created at: {self.repo_path}")
        if self.remote_url:
            self.log(f"✓ Force pushed to: {self.remote_url} ({self.branch})")
        else:
            self.log("⚠ Remote URL not provided; changes remain local.")
        self.log("=" * 60)

        return summary


def normalize_and_validate_text(text: str) -> str:
    uppercase_text = text.upper()
    char_width = sum(
        GitHubContributionsArt.CHAR_WIDTH + GitHubContributionsArt.CHAR_SPACING
        for char in uppercase_text
        if char in FONT_5X7
    )
    if char_width > 0:
        char_width -= GitHubContributionsArt.CHAR_SPACING

    if char_width > GitHubContributionsArt.GRID_WIDTH:
        raise ValueError(
            f"Text '{text}' is too long ({char_width} columns, max {GitHubContributionsArt.GRID_WIDTH})"
        )

    invalid_chars = [char for char in uppercase_text if char not in FONT_5X7]
    if invalid_chars:
        unique = ", ".join(sorted(set(invalid_chars)))
        raise ValueError(f"Unsupported characters: {unique}")

    return uppercase_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate GitHub contribution graph art.")
    parser.add_argument("--text", "-t", dest="text_override", help="Text to render on the contribution graph.")
    parser.add_argument(
        "--repo-path",
        "-r",
        dest="repo_path_override",
        default="./contribution_repo",
        help="Path to the working repository.",
    )
    parser.add_argument("--remote-url", help="Remote repository URL to push to.")
    parser.add_argument("--branch", "-b", default="main", help="Branch name to push (default: main).")
    parser.add_argument("--start-date", help="Override the starting date (YYYY-MM-DD).")
    parser.add_argument("--quiet", action="store_true", help="Reduce output to errors only.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON summary.")
    parser.add_argument("text", nargs="?", help="Text to render (if --text is not provided).")
    parser.add_argument("repo_path", nargs="?", help="Optional repository path override.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    raw_text = args.text_override or args.text
    if not raw_text:
        parser.error("Text is required (use --text or positional argument).")

    try:
        normalized_text = normalize_and_validate_text(raw_text)
    except ValueError as exc:
        parser.error(str(exc))

    repo_path = args.repo_path or args.repo_path_override

    start_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError as exc:
            parser.error(f"Invalid --start-date '{args.start_date}': {exc}")

    generator = GitHubContributionsArt(
        normalized_text,
        repo_path,
        remote_url=args.remote_url,
        branch=args.branch,
        verbose=not args.quiet,
    )

    summary = generator.generate(start_date=start_date)

    if args.json:
        print(json.dumps(summary))
    elif not args.quiet:
        print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())