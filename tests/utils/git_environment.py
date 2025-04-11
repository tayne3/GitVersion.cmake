#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Git environment utilities for testing GitVersion.cmake.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional


class GitEnvironment:
    """Class to manage a temporary Git repository for testing."""
    
    def __init__(self, root_dir: Optional[str] = None):
        """Initialize a temporary Git repository.
        
        Args:
            root_dir: Optional directory to create the repository in. If None, a temporary directory is created.
        """
        self.temp_dir = None
        if root_dir is None:
            self.temp_dir = tempfile.TemporaryDirectory()
            self.root_dir = Path(self.temp_dir.name)
        else:
            self.root_dir = Path(root_dir)
            os.makedirs(self.root_dir, exist_ok=True)
            
        # Initialize Git repository
        self._run_git_command("init")
        
        # Configure Git user
        self._run_git_command("config", "user.name", "GitVersion Test")
        self._run_git_command("config", "user.email", "test@example.com")
    
    def _run_git_command(self, *args) -> str:
        """Run a Git command in the repository.
        
        Args:
            *args: Git command and arguments
            
        Returns:
            The command output
        """
        result = subprocess.run(
            ["git"] + list(args),
            cwd=self.root_dir,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    def create_file(self, filename: str, content: str = "") -> None:
        """Create a file in the repository.
        
        Args:
            filename: The file name
            content: The file content
        """
        file_path = self.root_dir / filename
        # ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
    
    def commit(self, message: str = "Test commit") -> str:
        """Create a commit.
        
        Args:
            message: The commit message
            
        Returns:
            The commit hash
        """
        self._run_git_command("add", ".")
        self._run_git_command("commit", "-m", message)
        return self._run_git_command("rev-parse", "HEAD")
    
    def tag(self, tag_name: str) -> None:
        """Create a tag.
        
        Args:
            tag_name: The tag name
        """
        self._run_git_command("tag", tag_name)
    
    def get_commit_count(self) -> int:
        """Get the number of commits in the repository.
        
        Returns:
            The number of commits
        """
        return int(self._run_git_command("rev-list", "--count", "HEAD"))
    
    def get_short_hash(self) -> str:
        """Get the short hash of the current commit.
        
        Returns:
            The short hash
        """
        return self._run_git_command("rev-parse", "--short=9", "HEAD")
    
    def debug_git_describe(self, prefix: str = "") -> str:
        """Run git describe command and return the result for debugging.
        
        Args:
            prefix: Tag prefix
            
        Returns:
            Command output
        """
        try:
            return self._run_git_command("describe", f"--match={prefix}*.*.*", "--tags", "--abbrev=9")
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
    
    def checkout(self, branch_name: str, create: bool = False) -> None:
        """Checkout a branch.
        
        Args:
            branch_name: The branch name
            create: Whether to create the branch if it doesn't exist
        """
        if create:
            self._run_git_command("checkout", "-b", branch_name)
        else:
            self._run_git_command("checkout", branch_name)
    
    def __del__(self):
        """Clean up the temporary directory if created."""
        if self.temp_dir:
            self.temp_dir.cleanup() 
