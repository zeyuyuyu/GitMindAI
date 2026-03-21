import openai
import git
from pathlib import Path
from typing import List, Dict

class GitMindAI:
    def __init__(self, repo_path: str, api_key: str):
        self.repo = git.Repo(repo_path)
        openai.api_key = api_key

    def get_diff_content(self) -> str:
        """Get the current unstaged changes in the repository"""
        diff = self.repo.git.diff()
        return diff if diff else ''

    def classify_changes(self, diff_content: str) -> Dict[str, float]:
        """Classify the type of changes using AI"""
        prompt = f"""Analyze this git diff and classify the type of changes:
        {diff_content}
        
        Classify into these categories with confidence scores (0-1):
        - feat (new feature)
        - fix (bug fix)
        - refactor (code restructuring)
        - docs (documentation)
        - test (testing changes)
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse the response and extract classifications
        classifications = {
            'feat': 0.0,
            'fix': 0.0,
            'refactor': 0.0,
            'docs': 0.0,
            'test': 0.0
        }
        
        analysis = response.choices[0].message.content
        # Add basic classification logic here
        return classifications

    def generate_commit_message(self, diff_content: str) -> str:
        """Generate an intelligent commit message based on the changes"""
        classifications = self.classify_changes(diff_content)
        
        # Get the primary change type
        primary_type = max(classifications.items(), key=lambda x: x[1])[0]

        prompt = f"""Generate a concise, descriptive commit message for these changes:
        {diff_content}
        
        Follow the conventional commits format, using type '{primary_type}'.
        Format: <type>: <description>
        Keep it under 72 characters.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    def suggest_commit(self) -> str:
        """Analyze current changes and suggest a commit message"""
        diff_content = self.get_diff_content()
        if not diff_content:
            return "No changes to commit"

        return self.generate_commit_message(diff_content)

    def auto_commit(self, review: bool = True) -> None:
        """Automatically commit changes with an AI-generated message"""
        message = self.suggest_commit()
        
        if review:
            print(f"Suggested commit message: {message}")
            confirm = input("Proceed with commit? (y/n): ")
            if confirm.lower() != 'y':
                return

        self.repo.index.add('*')
        self.repo.index.commit(message)

def main():
    # Example usage
    gitmind = GitMindAI(
        repo_path=".",
        api_key="your-openai-api-key"
    )
    
    # Generate and review a commit message
    message = gitmind.suggest_commit()
    print(f"Suggested commit message: {message}")

if __name__ == "__main__":
    main()