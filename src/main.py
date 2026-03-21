import os
import openai
from git import Repo
from typing import List, Dict

class GitMindAI:
    def __init__(self, repo_path: str, openai_api_key: str):
        self.repo = Repo(repo_path)
        openai.api_key = openai_api_key

    def get_diff_context(self) -> List[str]:
        """Get the diff context from staged changes"""
        diffs = []
        for diff in self.repo.index.diff('HEAD'):
            diffs.append(f'File: {diff.a_path}\n{diff.diff.decode("utf-8")}')
        return diffs

    def generate_commit_message(self) -> str:
        """Generate an intelligent commit message based on changes"""
        diffs = self.get_diff_context()
        if not diffs:
            return "No changes staged for commit"

        prompt = f"""Generate a concise, conventional commit message for these changes:

{chr(10).join(diffs)}

Follow the format: <type>(<scope>): <description>
where type is one of: feat, fix, docs, style, refactor, test, chore"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful git commit message generator."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    def smart_commit(self) -> Dict[str, str]:
        """Create a commit with an AI-generated message"""
        try:
            message = self.generate_commit_message()
            if message == "No changes staged for commit":
                return {"status": "error", "message": message}

            self.repo.index.commit(message)
            return {"status": "success", "message": message}

        except Exception as e:
            return {"status": "error", "message": str(e)}

def main():
    repo_path = os.getenv("GITMIND_REPO_PATH", ".")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return

    git_mind = GitMindAI(repo_path, api_key)
    result = git_mind.smart_commit()
    print(f"Status: {result['status']}\nMessage: {result['message']}")

if __name__ == "__main__":
    main()