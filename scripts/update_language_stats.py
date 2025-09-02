#!/usr/bin/env python3
"""
Script to automatically update language statistics in README.md
Fetches language data from all public repositories and calculates percentages
"""

import os
import re
import requests
from typing import Dict, List
import time

class LanguageStatsUpdater:
    def __init__(self, github_token: str, username: str):
        self.github_token = github_token
        self.username = username
        self.headers = {
            'Authorization': f'token {self.github_token}',
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
        
        # Logo slug mapping for shields.io badges
        self.logo_slugs = {
            'TeX': 'latex',
            'HTML': 'html5',
            'Dart': 'dart',
            'JavaScript': 'javascript',
            'C++': 'cplusplus',
            'CSS': 'css3',
            'Python': 'python',
            'Java': 'java',
            'TypeScript': 'typescript',
            'Kotlin': 'kotlin',
            'Swift': 'swift',
            'Go': 'go',
            'Rust': 'rust',
            'PHP': 'php',
            'C': 'c',
            'C#': 'csharp',
            'Shell': 'gnubash',
            'Vue': 'vuedotjs',
            'Ruby': 'ruby',
            'React': 'react',
            'JSX': 'react'
        }
    
    def make_github_request(self, url: str, params: dict = None) -> dict:
        """Make a GitHub API request with retry logic and fallback to unauthenticated"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Try authenticated request first if token is available
                if self.github_token and self.github_token != "dummy_token":
                    response = requests.get(url, headers=self.headers, params=params, timeout=10)
                else:
                    # Use unauthenticated request
                    headers = {'Accept': 'application/vnd.github.v3+json'}
                    response = requests.get(url, headers=headers, params=params, timeout=10)
                
                # Check rate limit
                if response.status_code == 403 and 'rate limit' in response.text.lower():
                    print(f"⚠️  Rate limit hit. Waiting 60 seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(60)
                    continue
                
                # If authenticated request fails with auth error, try unauthenticated
                if response.status_code == 401 and self.github_token:
                    print(f"🔄 Authentication failed, trying unauthenticated request...")
                    headers = {'Accept': 'application/vnd.github.v3+json'}
                    response = requests.get(url, headers=headers, params=params, timeout=10)
                    
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"❌ Failed to make request after {max_retries} attempts")
                    return {}
    
    def validate_github_token(self) -> bool:
        """Validate GitHub token by making a test API call"""
        if not self.github_token or self.github_token == "dummy_token":
            print("⚠️  No valid GitHub token provided, will use unauthenticated requests")
            return True  # Allow unauthenticated access for public repos
            
        try:
            url = f'{self.base_url}/user'
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 401:
                print("⚠️  GitHub token is invalid, will try unauthenticated requests")
                return True  # Fallback to unauthenticated
            elif response.status_code == 403:
                print("⚠️  GitHub token has limited permissions, will try unauthenticated requests")
                return True  # Fallback to unauthenticated
            elif response.status_code == 200:
                user_data = response.json()
                print(f"✅ GitHub token validated for user: {user_data.get('login', 'unknown')}")
                return True
            else:
                print(f"⚠️  Unexpected response from GitHub API: {response.status_code}, continuing anyway")
                return True  # Continue anyway
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error validating GitHub token: {e}, will try without authentication")
            return True  # Continue without authentication
    
    def get_user_repositories(self) -> List[Dict]:
        """Fetch all repositories (public and private if authenticated) for the user"""
        repositories = []
        page = 1
        
        print(f"Fetching repositories for user: {self.username}")
        
        while True:
            # Try to get both private and public repos if authenticated
            url = f'{self.base_url}/user/repos'  # This endpoint includes private repos if authenticated
            params = {
                'visibility': 'all',  # Get both public and private
                'affiliation': 'owner',  # Only repos owned by the user
                'sort': 'updated',
                'direction': 'desc',
                'per_page': 100,
                'page': page
            }
            
            # If that fails, fallback to public repos only
            fallback_url = f'{self.base_url}/users/{self.username}/repos'
            fallback_params = {
                'type': 'public',
                'sort': 'updated',
                'direction': 'desc',
                'per_page': 100,
                'page': page
            }
            
            try:
                # Try authenticated endpoint first (includes private repos)
                repos = self.make_github_request(url, params)
                if not repos:
                    print(f"⚠️  No repositories returned from authenticated endpoint for page {page}")
                    # Try public endpoint as fallback
                    print("🔄 Trying public repositories endpoint...")
                    repos = self.make_github_request(fallback_url, fallback_params)
                    
                if not repos:
                    print(f"⚠️  No repositories returned for page {page}")
                    break
                    
                # Log repository info
                for repo in repos:
                    repo_name = repo['name']
                    private = repo.get('private', False)
                    updated_at = repo.get('updated_at', 'unknown')
                    privacy_status = "🔒 Private" if private else "🌐 Public"
                    print(f"  Found repository: {repo_name} ({privacy_status}) (updated: {updated_at})")
                    
                repositories.extend(repos)
                page += 1
                
                # Rate limiting
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching repositories: {e}")
                
                # If authenticated request fails, try public-only endpoint
                if page == 1:
                    print("🔄 Attempting public repositories only...")
                    try:
                        repos = self.make_github_request(fallback_url, fallback_params)
                        if repos:
                            print(f"✅ Fallback successful - fetched {len(repos)} public repositories")
                            repositories.extend(repos)
                            page += 1
                            continue
                    except Exception as fallback_error:
                        print(f"❌ Fallback also failed: {fallback_error}")
                
                break
        
        # Count private vs public repos
        private_count = sum(1 for repo in repositories if repo.get('private', False))
        public_count = len(repositories) - private_count
        
        print(f"Total repositories found: {len(repositories)}")
        print(f"  🌐 Public: {public_count}")
        print(f"  🔒 Private: {private_count}")
        
        return repositories
    
    def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """Get language statistics for a specific repository"""
        url = f'{self.base_url}/repos/{self.username}/{repo_name}/languages'
        
        try:
            return self.make_github_request(url)
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
            
        # Check if repository description mentions React (handle None description)
        description = repo_data.get('description') or ''
        if 'react' in description.lower():
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
            
            # Skip if no language data available (rate limit, private repo, etc.)
            if not languages:
                print(f"  ⚠️  No language data available for {repo_name}")
                continue
            
            # Check if this is a React project and React conversion is enabled
            react_conversion_percent = int(os.getenv('REACT_JS_ALLOCATION_PERCENT', '0'))
            is_react = self.is_react_project(repo_name, repo)
            
            if is_react and 'JavaScript' in languages and react_conversion_percent > 0:
                # For React projects, convert a portion of JavaScript to React
                js_bytes = languages['JavaScript']
                # Use configurable percentage (default 0% = disabled)
                react_bytes = int(js_bytes * (react_conversion_percent / 100))
                remaining_js = js_bytes - react_bytes
                
                print(f"  Detected React project! Converting {react_bytes} bytes ({react_conversion_percent}%) to React")
                
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
                # Add all languages as-is for non-React projects or when conversion is disabled
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
            description = (repo.get('description') or '').lower()
            topics = repo.get('topics', []) if repo.get('topics') else []
            
            # Convert topics to lowercase for comparison
            topics_lower = [topic.lower() for topic in topics]
            
            # Detect frameworks based on repo name, description, and topics
            if any(keyword in repo_name for keyword in ['flutter']) or \
               any(keyword in description for keyword in ['flutter']) or \
               'flutter' in topics_lower:
                detected['Flutter'] = True
                
            if any(keyword in repo_name for keyword in ['react']) or \
               any(keyword in description for keyword in ['react']) or \
               'react' in topics_lower:
                detected['React'] = True
                
            if any(keyword in repo_name for keyword in ['node', 'nodejs']) or \
               any(keyword in description for keyword in ['node.js', 'nodejs', 'node js']) or \
               any(topic in topics_lower for topic in ['nodejs', 'node']):
                detected['Node.js'] = True
                
            if any(keyword in repo_name for keyword in ['firebase']) or \
               any(keyword in description for keyword in ['firebase']) or \
               'firebase' in topics_lower:
                detected['Firebase'] = True
                
            if any(keyword in repo_name for keyword in ['mysql']) or \
               any(keyword in description for keyword in ['mysql']) or \
               'mysql' in topics_lower:
                detected['MySQL'] = True
                
            if any(keyword in repo_name for keyword in ['android']) or \
               any(keyword in description for keyword in ['android']) or \
               'android' in topics_lower:
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
            logo = self.logo_slugs.get(language, language.lower())
            # URL encode the language name for the badge
            encoded_lang = language.replace('+', '%2B').replace('#', '%23').replace(' ', '%20')
            badge = f'  <img src="https://img.shields.io/badge/{encoded_lang}-{color}?style=for-the-badge&logo={logo}&logoColor=white" alt="{language}"/>'
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
            
            # URL encode the language name and percentage for the badge
            encoded_lang = language.replace('+', '%2B').replace('#', '%23').replace(' ', '%20')
            encoded_percentage = percentage_str.replace('%', '%25')
            
            # Create badge with appropriate label color
            if language == 'JavaScript':
                badge = f"![{language}](https://img.shields.io/badge/{encoded_lang}-{encoded_percentage}-{color}?style=flat-square&labelColor=black)"
            else:
                badge = f"![{language}](https://img.shields.io/badge/{encoded_lang}-{encoded_percentage}-{color}?style=flat-square)"
            
            table_lines.append(f"| {language:<10} | {percentage_str:<10} | {badge} |")
        
        return "\n".join(table_lines)
    
    def update_readme(self, language_stats: Dict[str, float], repositories: List[Dict]) -> bool:
        """Update the README.md file with new language statistics and tools"""
        # Use portable path that works locally and in CI
        workspace = os.getenv('GITHUB_WORKSPACE', '.')
        readme_path = os.path.join(workspace, 'README.md')
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"README.md not found at {readme_path}")
            return False
        
        # Generate new content
        new_table = self.generate_language_table(language_stats)
        new_tools_section = self.generate_languages_and_tools_section(language_stats, repositories)
        
        if not new_table or not new_tools_section:
            print("No language statistics to update")
            return False
        
        # Find and replace the language statistics table using HTML markers
        table_pattern = r'(<!-- LANG-TABLE-START -->\s*\n\| Language\s+\| Percentage\s+\| Progress Bar \|\s*\n\|[^\n]+\|\s*\n)(.*?)(\n<!-- LANG-TABLE-END -->)'
        table_lines = new_table.split('\n')
        table_data_rows = '\n'.join(table_lines[2:])  # Skip header and separator
        
        if re.search(table_pattern, content, flags=re.MULTILINE | re.DOTALL):
            table_replacement = f"\\1{table_data_rows}\\3"
            new_content = re.sub(table_pattern, table_replacement, content, flags=re.MULTILINE | re.DOTALL)
            print("✅ Successfully updated language table")
        else:
            print("⚠️  Could not find language table section with markers")
            return False
        
        # Find and replace the Languages and Tools section using HTML markers
        tools_pattern = r'(<!-- LANG-TOOLS-START -->\s*\n)(.*?)(\n<!-- LANG-TOOLS-END -->)'
        
        if re.search(tools_pattern, new_content, flags=re.MULTILINE | re.DOTALL):
            tools_replacement = f"\\1{new_tools_section}\\3"
            new_content = re.sub(tools_pattern, tools_replacement, new_content, flags=re.MULTILINE | re.DOTALL)
            print("✅ Successfully updated languages and tools section")
        else:
            print("⚠️  Could not find languages and tools section with markers")
            return False
        
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
        try:
            print(f"🚀 Starting language statistics update for user: {self.username}")
            print("=" * 50)
            
            # Validate GitHub token first
            print("🔐 Validating GitHub token...")
            if not self.validate_github_token():
                print("⚠️  Continuing without valid authentication...")
            
            # Get repositories first
            repositories = self.get_user_repositories()
            
            if not repositories:
                print("❌ No repositories found")
                print("This could be due to:")
                print("  - Network connectivity issues")
                print("  - User has no public repositories")
                print("  - API rate limiting")
                print("  - Repository privacy settings")
                print("⚠️  Exiting gracefully...")
                return  # Exit gracefully instead of raising exception
            
            # Detect new repositories for immediate attention
            print("\n🔍 Checking for recently created repositories...")
            recent_repos = self.detect_new_repositories(repositories)
            
            # Calculate language statistics using all repositories
            print(f"\n📊 Calculating language statistics across {len(repositories)} repositories...")
            language_stats = self.calculate_language_statistics(repositories)
            
            if not language_stats:
                print("⚠️  No language statistics calculated - this might be due to:")
                print("   - All repositories are forks (excluded from stats)")
                print("   - API rate limiting")
                print("   - Network connectivity issues")
                print("   - Empty repositories with no detectable languages")
                return
            
            print(f"\n📈 Language Statistics (Top {min(len(language_stats), 10)} languages):")
            for i, (language, percentage) in enumerate(list(language_stats.items())[:10], 1):
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
            
        except Exception as e:
            print(f"❌ Fatal error during execution: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print("Full traceback:")
            traceback.print_exc()
            # Don't raise the exception, just exit gracefully
            print("⚠️  Exiting gracefully to prevent workflow failure")
            return

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
