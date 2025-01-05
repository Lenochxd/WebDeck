# Contributing to WebDeck

Thank you for considering contributing to WebDeck! Here are some guidelines to help you get started.


## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Languages](#languages)
- [Python](#python)
- [Jinja Templates/HTML/JS](#jinja-templateshtmljs)
- [Website](#website)
- [Reporting Issues](#reporting-issues)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Discord Community](#discord-community)

## Code of Conduct

Please adhere to the [Code of Conduct](https://github.com/Lenochxd/WebDeck/blob/master/.github/CODE_OF_CONDUCT.md) in all your interactions with the project.


## Development Setup

To set up the development environment, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Lenochxd/WebDeck.git
    cd webdeck
    ```

1. Set up your environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    python3 run.py
    ```


## Languages

- Translation files are in `webdeck/translations/*`.
- To add or update a translation:
  1. Copy `en_US.lang` to a new file named with your language code (e.g., `fr_FR.lang`).
  2. Follow the instructions in the file to translate only the necessary text.

> **Note**:
> - Only translate the `.lang` files. Do not translate other files like `webdeck/version.json`.
> - Translating `README.md` files is optional but not recommended as it increases maintenance work.


## Python

- Write clean, readable, and maintainable code.
- Write descriptive docstrings and comments for complex logic.
- Avoid using deprecated functions and libraries.


## Jinja Templates/HTML/JS

- The current codebase is messy and will be rewritten.
- Contributions are welcome but be aware that the code is temporary and will be replaced.
- Focus on fixing immediate issues or improving layout consistency.


## Website

- The website repository is not public yet. Contributions will be welcome once it is made available.


## Reporting Issues

If you find a bug, have a feature suggestion, or notice a documentation gap:
1. Check if the issue already exists in [Issues](https://github.com/Lenochxd/WebDeck/issues).
2. If not, create a new issue with:
   - A clear description.
   - Steps to reproduce (if it's a bug).
   - Relevant screenshots or logs (if applicable).


## Submitting a Pull Request

To submit a pull request, follow these steps:

1. **Fork the repository**:
    - Navigate to the [WebDeck repository](https://github.com/Lenochxd/WebDeck) on GitHub.
    - Click the "Fork" button in the top-right corner of the page to create a copy of the repository under your GitHub account.

2. **Clone your fork**:
    - Open your terminal or command prompt.
    - Clone your forked repository to your local machine:
        ```bash
        git clone https://github.com/<your-username>/WebDeck.git
        cd WebDeck
        ```

3. **Create a new branch**:
    - Create a new branch for your feature or bugfix:
        ```bash
        git checkout -b feature/your-feature-name
        ```

4. **Make your changes**:
    - Implement your feature or bugfix in the codebase.
    - Ensure your code follows the project's coding standards and guidelines.

5. **Commit your changes**:
    - Stage your changes:
        ```bash
        git add .
        ```
    - Commit your changes with a clear and concise commit message:
        ```bash
        git commit -m "Description of your changes"
        ```

6. **Push your branch**:
    - Push your branch to your forked repository on GitHub:
        ```bash
        git push origin feature/your-feature-name
        ```

7. **Open a pull request**:
    - Navigate to your forked repository on GitHub.
    - Click the "Compare & pull request" button next to your branch.
    - Provide a detailed description of your changes in the pull request, including the purpose and any relevant information.
    - Submit the pull request.

8. **Address feedback**:
    - Be responsive to any feedback or requests for changes from the project maintainers.
    - Make necessary updates to your pull request as requested.

> **Tip**: If your branch has multiple commits for a single feature, consider squashing them before submitting your PR.


## Discord Community

Join our [Discord community](https://discord.gg/tUPsYHAGfm) to discuss anything related to WebDeck. Contributors can also help users and collaborate on new features or bug fixes.

---

Thank you for your contribution!
