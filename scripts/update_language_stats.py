#!/usr/bin/env python3
"""
Script to automatically update language statistics in README.md
Fetches language data from all public repositories and calculates percentages
"""

import os
import re
import requests
import json
from typing import Dict, List, Tuple
import time

class LanguageStatsUpdater:
    def __init__(self, github_token: str, username: str):
        self.github_token = github_token
        self.username = username
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
        
        # Language color mapping for badges
        self.language_colors = {
            'TeX': '008080',
            'HTML': 'E34F26', 
            'Dart': '0175C2',
            'JavaScript': 'F7DF1E',
            'C++': '00599C',
            'CSS': '1572B6',
            'Python': '3776AB',
            'Java': 'ED8B00',
            'TypeScript': '3178C6',
            'Kotlin': '0095D5',
            'Swift': 'FA7343',
            'Go': '00ADD8',
            'Rust': '000000',
            'PHP': '777BB4',
            'C': '555555',
            'C#': '239120',
            'Shell': '89E051',
            'Vue': '4FC08D',
            'Ruby': 'CC342D'
        }
    
    def get_user_repositories(self) -> List[Dict]:
        """Fetch all public repositories for the user"""
        repositories = []
        page = 1
        
        while True:
            url = f'{self.base_url}/users/{self.username}/repos'
            params = {
                'type': 'public',
                'sort': 'updated',
                'per_page': 100,
                'page': page
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                repos = response.json()
                if not repos:
                    break
                    
                repositories.extend(repos)
                page += 1
                
                # Rate limiting
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching repositories: {e}")
                break
        
        return repositories
    
    def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """Get language statistics for a specific repository"""
        url = f'{self.base_url}/repos/{self.username}/{repo_name}/languages'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching languages for {repo_name}: {e}")
            return {}
    
    def calculate_language_statistics(self) -> Dict[str, float]:
        """Calculate language usage percentages across all repositories"""
        repositories = self.get_user_repositories()
        language_totals = {}
        
        print(f"Found {len(repositories)} repositories")
        
        for repo in repositories:
            if repo.get('fork', False):
                continue  # Skip forked repositories
                
            repo_name = repo['name']
            print(f"Processing repository: {repo_name}")
            
            languages = self.get_repository_languages(repo_name)
            
            for language, bytes_count in languages.items():
                if language not in language_totals:
                    language_totals[language] = 0
                language_totals[language] += bytes_count
            
            # Rate limiting
            time.sleep(0.1)
        
        # Calculate percentages
        total_bytes = sum(language_totals.values())
        if total_bytes == 0:
            return {}
        
        language_percentages = {}
        for language, bytes_count in language_totals.items():
            percentage = (bytes_count / total_bytes) * 100
            language_percentages[language] = percentage
        
        # Sort by percentage (descending)
        sorted_languages = dict(sorted(language_percentages.items(), 
                                     key=lambda x: x[1], reverse=True))
        
        return sorted_languages
    
    def get_language_color(self, language: str) -> str:
        """Get color code for a language badge"""
        return self.language_colors.get(language, '808080')  # Default gray
    
    def generate_language_table(self, language_stats: Dict[str, float]) -> str:
        """Generate the language statistics table for README"""
        if not language_stats:
            return ""
        
        # Take top 10 languages
        top_languages = dict(list(language_stats.items())[:10])
        
        table_lines = [
            "| Language   | Percentage | Progress Bar |",
            "|------------|------------|--------------|"
        ]
        
        for language, percentage in top_languages.items():
            color = self.get_language_color(language)
            percentage_str = f"{percentage:.2f}%"
            
            # Create badge with appropriate label color
            if language == 'JavaScript':
                badge = f"![{language}](https://img.shields.io/badge/{language}-{percentage_str.replace('%', '%25')}-{color}?style=flat-square&labelColor=black)"
            else:
                badge = f"![{language}](https://img.shields.io/badge/{language}-{percentage_str.replace('%', '%25')}-{color}?style=flat-square)"
            
            table_lines.append(f"| {language:<10} | {percentage_str:<10} | {badge} |")
        
        return "\n".join(table_lines)
    
    def update_readme(self, language_stats: Dict[str, float]) -> bool:
        """Update the README.md file with new language statistics"""
        readme_path = '/home/runner/work/UniqeBd/UniqeBd/README.md'
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print("README.md not found")
            return False
        
        # Generate new table
        new_table = self.generate_language_table(language_stats)
        if not new_table:
            print("No language statistics to update")
            return False
        
        # Find and replace the language statistics table
        pattern = r'(\| Language\s+\| Percentage\s+\| Progress Bar \|\s*\n\|[^\n]+\|\s*\n)(.*?)(?=\n</div>)'
        
        # Extract just the data rows from the new table
        table_lines = new_table.split('\n')
        data_rows = '\n'.join(table_lines[2:])  # Skip header and separator
        replacement = f"\\1{data_rows}\n"
        
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        # Check if content actually changed
        if new_content == content:
            print("No changes needed in README.md")
            return False
        
        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print("README.md updated successfully")
        return True
    
    def run(self):
        """Main execution function"""
        print(f"Starting language statistics update for user: {self.username}")
        
        # Calculate language statistics
        language_stats = self.calculate_language_statistics()
        
        if not language_stats:
            print("No language statistics found")
            return
        
        print("\nLanguage Statistics:")
        for language, percentage in language_stats.items():
            print(f"  {language}: {percentage:.2f}%")
        
        # Update README
        self.update_readme(language_stats)

def main():
    github_token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME')
    
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return 1
    
    if not username:
        print("Error: GITHUB_USERNAME environment variable not set")
        return 1
    
    updater = LanguageStatsUpdater(github_token, username)
    updater.run()
    
    return 0

if __name__ == '__main__':
    exit(main())