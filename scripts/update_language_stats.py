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
            'Authorization': f'token {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}',
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
            'Ruby': 'CC342D',
            'React': '61DAFB',
            'JSX': '61DAFB'
        }
    
    def get_user_repositories(self) -> List[Dict]:
        """Fetch all public repositories for the user, sorted by last updated for immediate detection"""
        repositories = []
        page = 1
        
        print(f"Fetching repositories for user: {self.username}")
        
        while True:
            url = f'{self.base_url}/users/{self.username}/repos'
            params = {
                'type': 'public',
                'sort': 'updated',  # Sort by most recently updated first
                'direction': 'desc',  # Newest first for immediate detection
                'per_page': 100,
                'page': page
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                repos = response.json()
                if not repos:
                    break
                    
                # Log repository info for new repository detection
                for repo in repos:
                    repo_name = repo['name']
                    updated_at = repo.get('updated_at', 'unknown')
                    created_at = repo.get('created_at', 'unknown')
                    print(f"  Found repository: {repo_name} (updated: {updated_at})")
                    
                repositories.extend(repos)
                page += 1
                
                # Rate limiting
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching repositories: {e}")
                break
        
        print(f"Total repositories found: {len(repositories)}")
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
    
    def detect_new_repositories(self, repositories: List[Dict]) -> List[Dict]:
        """Detect recently created repositories (within last 30 days) for immediate updates"""
        from datetime import datetime, timezone, timedelta
        
        recent_repos = []
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
        
        for repo in repositories:
            if repo.get('fork', False):
                continue
                
            created_at_str = repo.get('created_at')
            if created_at_str:
                try:
                    created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                    if created_at > cutoff_date:
                        recent_repos.append(repo)
                        print(f"  🆕 New repository detected: {repo['name']} (created: {created_at_str})")
                except ValueError:
                    continue
        
        if recent_repos:
            print(f"Found {len(recent_repos)} recently created repositories!")
        else:
            print("No recently created repositories found.")
            
        return recent_repos
    
    def is_react_project(self, repo_name: str, repo_data: Dict) -> bool:
        """Detect if a repository is a React project"""
        # Check if repo name contains react
        if 'react' in repo_name.lower():
            return True
            
        # Check if repository description mentions React
        description = repo_data.get('description', '').lower()
        if 'react' in description:
            return True
            
        # For comprehensive detection, we could check for package.json with React deps
        # but that would require additional API calls. The name-based detection
        # should be sufficient for most cases.
        return False
    
    def calculate_language_statistics(self, repositories: List[Dict] = None) -> Dict[str, float]:
        """Calculate language usage percentages across all repositories"""
        if repositories is None:
            repositories = self.get_user_repositories()
        
        language_totals = {}
        
        print(f"Found {len(repositories)} repositories")
        
        for repo in repositories:
            if repo.get('fork', False):
                continue  # Skip forked repositories
                
            repo_name = repo['name']
            print(f"Processing repository: {repo_name}")
            
            languages = self.get_repository_languages(repo_name)
            
            # Check if this is a React project
            is_react = self.is_react_project(repo_name, repo)
            
            if is_react and 'JavaScript' in languages:
                # For React projects, convert a portion of JavaScript to React
                js_bytes = languages['JavaScript']
                # Assume 60% of JavaScript in React projects is actually React code
                react_bytes = int(js_bytes * 0.6)
                remaining_js = js_bytes - react_bytes
                
                print(f"  Detected React project! Converting {react_bytes} bytes to React")
                
                # Add React bytes
                if 'React' not in language_totals:
                    language_totals['React'] = 0
                language_totals['React'] += react_bytes
                
                # Add remaining JavaScript bytes if any
                if remaining_js > 0:
                    if 'JavaScript' not in language_totals:
                        language_totals['JavaScript'] = 0
                    language_totals['JavaScript'] += remaining_js
                
                # Add other languages as-is
                for language, bytes_count in languages.items():
                    if language != 'JavaScript':
                        if language not in language_totals:
                            language_totals[language] = 0
                        language_totals[language] += bytes_count
            else:
                # Add all languages as-is for non-React projects
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
    
    def detect_frameworks_and_tools(self, repositories: List[Dict]) -> Dict[str, bool]:
        """Detect frameworks and tools used across repositories"""
        detected = {
            'Flutter': False,
            'React': False,
            'Node.js': False,
            'Firebase': False,
            'MySQL': False,
            'Android Studio': False
        }
        
        for repo in repositories:
            if repo.get('fork', False):
                continue
                
            repo_name = repo['name'].lower()
            description = repo.get('description', '').lower() if repo.get('description') else ''
            
            # Detect frameworks based on repo name and description
            if 'flutter' in repo_name or 'flutter' in description:
                detected['Flutter'] = True
            if 'react' in repo_name or 'react' in description:
                detected['React'] = True
            if 'node' in repo_name or 'nodejs' in description or 'node.js' in description:
                detected['Node.js'] = True
            if 'firebase' in repo_name or 'firebase' in description:
                detected['Firebase'] = True
            if 'mysql' in repo_name or 'mysql' in description or 'database' in description:
                detected['MySQL'] = True
            if 'android' in repo_name or 'android' in description:
                detected['Android Studio'] = True
        
        return detected
    
    def generate_languages_and_tools_section(self, language_stats: Dict[str, float], repositories: List[Dict]) -> str:
        """Generate the complete Languages and Tools section"""
        if not language_stats:
            return ""
        
        # Get top languages (limit to most relevant ones)
        top_languages = dict(list(language_stats.items())[:8])
        
        # Generate programming languages badges
        lang_badges = []
        for language, _ in top_languages.items():
            color = self.get_language_color(language)
            badge = f'  <img src="https://img.shields.io/badge/{language}-{color}?style=for-the-badge&logo={language.lower()}&logoColor=white" alt="{language}"/>'
            lang_badges.append(badge)
        
        # Detect frameworks and tools
        frameworks = self.detect_frameworks_and_tools(repositories)
        
        # Generate framework badges for detected tools
        framework_mapping = {
            'Flutter': ('Flutter', '02569B', 'flutter'),
            'React': ('React', '20232A', 'react'),
            'Node.js': ('Node.js', '43853D', 'node.js'),
            'Firebase': ('Firebase', '039BE5', 'Firebase'),
            'MySQL': ('MySQL', '005C84', 'mysql'),
            'Android Studio': ('Android_Studio', '3DDC84', 'android-studio')
        }
        
        framework_badges = []
        for framework, is_detected in frameworks.items():
            if is_detected and framework in framework_mapping:
                name, color, logo = framework_mapping[framework]
                badge = f'  <img src="https://img.shields.io/badge/{name}-{color}?style=for-the-badge&logo={logo}&logoColor=white" alt="{framework}"/>'
                framework_badges.append(badge)
        
        # Build the complete section
        section = """<div align="center">

### Programming Languages
<p>
""" + "\n".join(lang_badges) + """
</p>

### Frameworks & Tools
<p>
""" + "\n".join(framework_badges) + """
</p>

</div>"""
        
        return section
    
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
    
    def update_readme(self, language_stats: Dict[str, float], repositories: List[Dict]) -> bool:
        """Update the README.md file with new language statistics and tools"""
        readme_path = '/home/runner/work/UniqeBd/UniqeBd/README.md'
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print("README.md not found")
            return False
        
        # Generate new content
        new_table = self.generate_language_table(language_stats)
        new_tools_section = self.generate_languages_and_tools_section(language_stats, repositories)
        
        if not new_table or not new_tools_section:
            print("No language statistics to update")
            return False
        
        # Find and replace the language statistics table
        table_pattern = r'(\| Language\s+\| Percentage\s+\| Progress Bar \|\s*\n\|[^\n]+\|\s*\n)(.*?)(?=\n</div>)'
        table_lines = new_table.split('\n')
        table_data_rows = '\n'.join(table_lines[2:])  # Skip header and separator
        table_replacement = f"\\1{table_data_rows}\n"
        new_content = re.sub(table_pattern, table_replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        # Find and replace the Languages and Tools section
        tools_pattern = r'(## 🛠️ Languages and Tools\s*\n\s*)(.*?)(?=\n---)'
        tools_replacement = f"\\1{new_tools_section}\n"
        new_content = re.sub(tools_pattern, tools_replacement, new_content, flags=re.MULTILINE | re.DOTALL)
        
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
        """Main execution function with enhanced repository detection"""
        print(f"🚀 Starting language statistics update for user: {self.username}")
        print("=" * 50)
        
        # Get repositories first
        repositories = self.get_user_repositories()
        
        # Detect new repositories for immediate attention
        print("\n🔍 Checking for recently created repositories...")
        recent_repos = self.detect_new_repositories(repositories)
        
        # Calculate language statistics using all repositories
        print(f"\n📊 Calculating language statistics across {len(repositories)} repositories...")
        language_stats = self.calculate_language_statistics(repositories)
        
        if not language_stats:
            print("❌ No language statistics found")
            return
        
        print(f"\n📈 Language Statistics (Top {len(language_stats)} languages):")
        for i, (language, percentage) in enumerate(language_stats.items(), 1):
            print(f"  {i:2d}. {language}: {percentage:.2f}%")
        
        # Update README with both language stats and tools
        print(f"\n📝 Updating README.md with latest statistics...")
        updated = self.update_readme(language_stats, repositories)
        
        if updated:
            print("✅ README.md updated successfully!")
            if recent_repos:
                print(f"🎉 Included {len(recent_repos)} recently created repositories in the update!")
        else:
            print("ℹ️  No changes needed - statistics are already up to date")
        
        print("=" * 50)
        print("🏁 Language statistics update completed")

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
