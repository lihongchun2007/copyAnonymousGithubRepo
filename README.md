# Save a repository from anonymous.4open.science

Inspired by [clone-anonymous4open](https://github.com/ShoufaChen/clone-anonymous4open) project, which fails to work on current anonymous.4open.science website. Here `current` means 2021.10.

## Prerequisites
```
pip install requests
```

## Quick Start
```
git clone https://github.com/lihongchun2007/copyAnonymousGithubRepo.git
cd copyAnonymousGithubRepo
python clone.py /path/to/save  repository_name_on_anonymous
```

Example:
```
python clone.py  ../examples 840c8c57-3c32-451e-bf12-0e20be300389
```
