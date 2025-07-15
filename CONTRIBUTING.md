# Contributing

Thanks for your interest in contributing to **Harmona**. We're happy to have you here.

Please take a moment to review this document before submitting your first pull request. We also strongly recommend that you check for open issues and pull requests to see if someone else is working on something similar.

If you need any help, feel free to reach out to **cstewart@cse.ohio-state.edu**.

## About this repository

**This repository is mono repo of all the application which are developed under the platform Harmona**

## Structure

This repository is structured as follows:

```
Harmona
├─ services
│  ├─ openpass
│  ├─ website
│  ├─ aimissions
│  ├─ yolomissions
│  ├─ boundrymap
│  └─ sofwarepilot
├─ scripts
│  ├─ deployment
│  └─ setup
├─ docs
│  ├─ services
│  ├─ scripts
│  └─ helm-config
├─ helm-config
├─ public
└─ src
```

| Microservice                  | Description                              |
| --------------------- | ---------------------------------------- |
| **`Openpass`**     | **Service which contains all drone mission**                     |
| **`Softwarepilot`**     | **Service that let our Parot Anafi drone to communicate with our application**                     |
| **`Website`**     | **[Service that make sure there is a common point from where all the independent microservice can be accessed]**                     |
| **`AImission`**     | **Service that performs AI based missions by Parrot Anafi Drone.**                     |
| **`Boundrymap`**     | **Service which analyze, calculate and perform all GPS related to the missions**                     |
| **`YOLOmission`**     | **Service contains all the mission which are required to detect a particular object by drone**                     |


| Folder                  | Description                              |
| --------------------- | ---------------------------------------- |
| **`services`**     | **Contains all code of each microservices**                     |
| **`scripts/deployment`**     | **Contains all the files which are used to deploy a microservice**                     |
| **`scripts/setup`**     | **Contains all files which are used to run the whole Harmona plotform**                     |
| **`helm-config`**     | **This folder contains helm chart of Apache Bitnami which are futher used to deploy the microservices**                     |

## Development

### Fork this repo

You can fork this repo by clicking the fork button in the top right corner of this page.

### Clone on your local machine

```bash
git clone https://github.com/your-username/Harmona.git
```

### Navigate to project directory

```bash
cd Harmona
```

### Create a new Branch

```bash
git checkout -b my-new-branch
```


### Run a workspace

#### Examples

1. To run **Harmona**:

```bash
./scripts/setup/startMicroservice.sh
```

## Documentation

The documentation for this project is located in **`docs/`**. You can run the documentation locally by running the mdx file in any IDE.

Documentation is written using **Markdown**..


## Commit Convention

Before you create a Pull Request, please check whether your commits comply with
the commit conventions used in this repository.

When you create a commit we kindly ask you to follow the convention
`category(scope or module): message` in your commit message while using one of
the following categories:

- `feat / feature`: all changes that introduce completely new code or new
  features
- `fix`: changes that fix a bug (ideally you will additionally reference an
  issue if present)
- `refactor`: any code related change that is not a fix nor a feature
- `docs`: changing existing or creating new documentation (i.e. README, docs for
  usage of a lib or cli usage)
- `build`: all changes regarding the build of the software, changes to
  dependencies or the addition of new dependencies
- `test`: all changes regarding tests (adding new tests or changing existing
  ones)
- `ci`: all changes regarding the configuration of continuous integration (i.e.
  github actions, ci system)
- `chore`: all changes to the repository that do not fit into any of the above
  categories

  e.g. `feat(components): add new prop to the avatar component`

