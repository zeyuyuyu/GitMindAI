import os
import subprocess
from typing import List, Dict
import openai
from pathlib import Path

class GitMindAI:
    def __init__(self, repo_path: str, api_key: str):
        self.repo_path = Path(repo_path)
        openai.api_key = api_key

    def get_diff_content(self) -> str:
        """Get the current git diff content"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f'Failed to get git diff: {str(e)}')

    def generate_commit_message(self, diff_content: str) -> str:
        """Generate an intelligent commit message using GPT"""
        if not diff_content:
            return 'No changes to commit'

        prompt = f"""Generate a concise and descriptive commit message following conventional commits format based on this git diff:

{diff_content}

Commit message format should be one of:
feat: <description>
fix: <description>
refactor: <description>
docs: <description>
test: <description>
chore: <description>
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful git commit message generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f'Failed to generate commit message: {str(e)}')

    def suggest_commit(self) -> Dict[str, str]:
        """Get diff and generate commit message suggestion"""
        diff = self.get_diff_content()
        message = self.generate_commit_message(diff)
        return {
            'diff': diff,
            'suggested_message': message
        }

def main():
    # Example usage
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise Exception('Please set OPENAI_API_KEY environment variable')

    git_mind = GitMindAI('.', api_key)
    suggestion = git_mind.suggest_commit()
    
    print('\nSuggested commit message:')
    print(suggestion['suggested_message'])

if __name__ == '__main__':
    main()