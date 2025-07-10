# Openpass

<!-- Badges Section - FILL IN YOUR ACTUAL VALUES -->
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-V2.0.0-green.svg)](https://github.com/[YOUR_USERNAME]/[REPO_NAME]/releases)

<!-- FILL IN: Brief description of what OpenPass does -->
Harmona is an opensource platform for Edge to Cloud AI-Driven Applications for Field Studies

![](docs/images/architecture.jpg)

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

### Prerequisites

<!-- FILL IN: List all requirements -->
- Ubuntu (22.01 or higher)
- Libraries using apt-get: bash, curl, python3, git, and docker.
- Hardware: at least (1) 4 1.2 Ghz CPU cores, (2) 8 GB Ram, and (3) 256 GB storage.
- Parrot Anafi Drones
- K3s (Lightweight Kubernetes)


## Quick Start

```bash
# Download the install.sh file first
curl -O https://raw.githubusercontent.com/ICICLE-ai/Harmona/main/install.sh

# Check if pods are READ and in RUNNING state
kubecmd get pods

#Once all pods are in READY state run 
bash /scripts/setup/startWebsite.sh
```
Below is the dashboard images which will apprear after performing above task.
![](/docs/images/dashboard.png)

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Code Standards
- Write tests for new features
- Update documentation for each implementation
- Use conventional commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`

## Support

<!-- FILL IN: Support information -->
- 📧 **Email:** cstewart@cse.ohio-state.edu
- 🐛 **Bug Reports:** [Create an issue](https://github.com/vedantpatil2021/Harmona/issues)
- 💡 **Feature Requests:** [Create an issue](https://github.com/vedantpatil2021/Harmona/issues)
- 📖 **Documentation:** [LINK](https://icicle-ai.github.io/training-catalog/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE)- [OAC 2112606](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2112606)

---

**⭐ If you find this project helpful, please consider giving it a star!**

**🤝 Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) before submitting a PR.**