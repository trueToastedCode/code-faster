import requests
from urllib.parse import urljoin


def parse_repository_str(repository_str):
    repository_str = repository_str.strip()
    if repository_str.startswith('https://github.com/'):
        return repository_str[19:]
    return repository_str


def parse_repositories_str(repositories_str):
    return [parse_repository_str(x) for x in repositories_str.split('\n') if x.strip()]


def fetch_branches(repository):
    response = requests.get(urljoin('https://api.github.com/repos/', repository + '/branches'))
    assert response.status_code == 200
    return [x['name'] for x in response.json()]


def main():
    repositories_str = """
    https://github.com/trueToastedCode/amqp
    https://github.com/trueToastedCode/common
    https://github.com/trueToastedCode/redis
    https://github.com/trueToastedCode/mongodb
    """

    out_file = 'result.txt'

    submodule_dst = 'src/submodules/%s'

    with open(out_file, 'w') as f:
        repositories = parse_repositories_str(repositories_str)

        for repository in repositories:
            f.write(f'[ {repository} ]\n')

            branches_url = urljoin('https://api.github.com/repos/', repository + '/branches')
            requests.get(branches_url)

            branches = fetch_branches(repository)
            git_url = urljoin('https://github.com/', repository + '.git')

            for branch in branches:
                f.write(f'git submodule add -b {branch} {git_url} {submodule_dst % branch}\n')

            f.write('\n')


if __name__ == '__main__':
    main()
