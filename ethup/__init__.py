import argparse
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from github import Github
from git import Repo, GitCommandError

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s[%(asctime)s] %(message)s',
    datefmt='%m-%d|%H:%M:%S',
)

# This should be an absolute path
REPO_PATH = '/path/to/your/local/repos'

# Generate on GitHub within Settings
#  -> Developer Settings
#  -> Personal Access Tokens
GITHUB_TOKEN = '<your_github_token>'

GITHUB_USER = '<your_user_name>'

# List of execution client repositories
FORKED_REPOS = [
    'besu',
    'erigon',
    'ethereumjs-monorepo',
    'evmone',
    'go-ethereum',
    'nethermind',
]


# Update Specified Repos
def update_repo(repo):
    logging.info(f'[{repo.name}] Starting processing')

    local_repo_path = os.path.join(CLIENTS_PATH, repo.name)

    if not os.path.exists(local_repo_path):
        logging.debug(f'[{repo.name}] Cloning into {local_repo_path}')
        Repo.clone_from(repo.clone_url, local_repo_path)

    local_repo = Repo(local_repo_path)
    git = local_repo.git

    # Check if the upstream remote already exists
    try:
        local_repo.remote('upstream')
    except ValueError:
        logging.info(
            f'[{repo.name}] Adding upstream remote: {repo.parent.clone_url}'
        )
        local_repo.create_remote('upstream', url=repo.parent.clone_url)

    logging.info(f'[{repo.name}] Fetching from upstream')
    git.fetch('upstream')

    logging.info(f'[{repo.name}] Checking out master/main/devel branch')
    merge_name = ''
    try:
        git.checkout('master')
        merge_name = 'master'
    except GitCommandError:
        try:
            git.checkout('main')
            merge_name = 'main'
        except GitCommandError:  # erigon
            git.checkout('devel')
            merge_name = 'devel'

    logging.info(f'[{repo.name}] Merging changes from upstream')
    git.merge(f'upstream/{merge_name}')

    logging.info(f'[{repo.name}] Pushing changes to origin')
    git.push('origin')

    logging.info(f'[{repo.name}] Finished processing')


def main():
    try:
        parser = argparse.ArgumentParser(
            description="Update Ethereum clients."
        )
        parser.add_argument(
            '--clients',
            nargs='+',
            default=FORKED_REPOS,
            help='Ethereum clients to update. Default updates all.')
        parser.add_argument(
            '--path',
            type=str,
            default=CLIENTS_PATH,
            help='Specify manual path to client repos.',
        )
        args = parser.parse_args()

        # Connect to Github
        g = Github(GITHUB_TOKEN)
        user = g.get_user(GITHUB_USER)

        # Update Specified Repos
        with ThreadPoolExecutor() as executor:
            repos_to_update = [
                repo for repo in user.get_repos() if repo.name in args.clients
            ]
            executor.map(update_repo, repos_to_update)
    except Exception as e:
        logging.error(f'Error: {e}')
