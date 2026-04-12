from github import Github, GithubException


def commit_article(
    repo_name: str,
    path: str,
    content: str,
    commit_message: str,
    token: str,
) -> dict:
    """Create or update a file in the GitHub repo and return status + URL."""
    g = Github(token)
    repo = g.get_repo(repo_name)

    try:
        existing = repo.get_contents(path)
        repo.update_file(
            path=path,
            message=commit_message,
            content=content,
            sha=existing.sha,
        )
        return {
            "status": "updated",
            "path": path,
            "url": f"https://github.com/{repo_name}/blob/main/{path}",
        }
    except GithubException as exc:
        if exc.status == 404:
            repo.create_file(
                path=path,
                message=commit_message,
                content=content,
            )
            return {
                "status": "created",
                "path": path,
                "url": f"https://github.com/{repo_name}/blob/main/{path}",
            }
        raise


def get_article_content(repo_name: str, path: str, token: str) -> str:
    """Read a file from the GitHub repo. Returns its UTF-8 text or an error note."""
    g = Github(token)
    repo = g.get_repo(repo_name)

    try:
        file = repo.get_contents(path)
        return file.decoded_content.decode("utf-8")
    except GithubException as exc:
        if exc.status == 404:
            return "文件不存在。"
        raise
