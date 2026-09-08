# Template for DTU bioengineering

This template is designed for bioengineering data science projects at [DTU Bioengineering](https://www.bioengineering.dtu.dk/). It follows best practices for project organization, ensuring consistency and efficiency in data handling, analysis, and modeling.

---

**DISCLAIMER: This introduction and template is built from [Cookiecutter](https://github.com/drivendata/cookiecutter-data-science). If you are an experienced programmer and know GitHub, I recommend you check the link**

---

### Assumptions for this guide

- You are relatively new to Python
- You have a strong cup of coffee
- Words like Git, GitHub and datascience scare you.

### First things first

This README.md is your project’s welcome page; it introduces your work at and guides newcomers on how to dive in. Keep it updated with your project's goals and instructions, ensuring it's a clear, for collaborators (and yourself). Below you will find a best practices for how to make a good readme file.

![DTU_BIOENGINEERING_SYNBIO_PIC](references/syn_biopic.png)

## Why spend 5 minutes on reading this guide?

- Invest just 5 minutes with this guide to master the essentials of data science project structure. You'll learn what files are important, and how they fit together. It's time well spent for skills that will last.

## Why organize you project in a standardized way?

- **Enhances collaboration:** Clearly defined directories and naming conventions facilitate teamwork and code reviews.
- **Increases efficiency:** Reduces the time taken to understand different parts of the project and how they connect.
- **Improves reproducibility:** Standardized folders and file names make it easier to reproduce analysis and results.
- **Facilitates automation:** Standard structures allow for the automation of data processing, testing, and deployment.

**Small tip:** One of my favorite programmers on Youtube, called Arjan, talks about this in this [video](https://www.youtube.com/watch?v=xVuqDBCQAYc&t=386s). His channel is a great resource to learn more about python programming.

## Project Organization

Below is a description/guide of a typical project folder structure and its contents:

- **README.md**

  - Think of this document as the welcome sign at the front door of your project. It's here to say hello to anyone who stops by and to give them a quick tour. Inside, you'll typically find:

    - **Project Overview**: A clear, concise introduction explaining the what, why, and how of your project. It sets the stage for understanding the purpose and value of your work.

    - **Installation Instructions**: Step-by-step guidance on getting your project up and running on a local machine. This part is crucial for onboarding new contributors quickly and effectively.

    - **How to Run your code**: Detailed commands and scripts to execute your project, whether it’s a simple: `python3 script.py`.

    - **Folder Structure Explanation**: An outline of the organizational layout of your project, detailing what each directory contains and how the files and folders are related to each other. This helps users navigate your project and understand where to find specific pieces of code or data.

    - **Usage Examples**: If applicable, provide examples of how to use your code or application, which can range from code snippets to screenshots or video demonstrations.

    - **Contributing Guidelines**: A section inviting and guiding potential contributors on how they can help improve the project, what the contribution process looks like, and any coding standards or tests they should be aware of.

  - Remember, the `README.md` is not just a manual; it’s the welcoming committee, the first impression, and the starting block for anyone who interacts with your project. Make it comprehensive, but also make it inviting!

- **LICENSE**

  - The LICENSE file contains the terms under which the project can be used, modified, or distributed. The most common is MIT license but BSD license is also widely usd.
  - In all your scripts you should have a copy of the LICENSE file see example script in src folder.

- **notebooks/**

  - Contains Jupyter notebooks for experiments and data exploration. The naming convention includes an ordering number, the creator's initials, and a description (e.g., `1.0-jqp-initial-data-exploration`).
  - This folder is super important and is probably where you will spend most of your time so remember to keep it tight with good naming conventions.

- **data/**

  - Organized subdirectories for various stages of data processing:
    - **external/**: Data from third-party sources that are often immutable and must be kept separate from internal modifications.
    - **interim/**: Intermediate data which might have gone through some transformations and are in the process towards the final dataset.
    - **processed/**: The final, cleaned data sets that are ready for analysis and modeling.
    - **raw/**: The original, unaltered data as it was obtained.

- **docs/**

  - Generated documentation for the project, possibly using tools like Sphinx, which helps in maintaining comprehensive and up-to-date documentation.
  - Sphinx is super cool since it can take the docstrings from you code and make a website from it. For example check out the documentation: https://teemi.readthedocs.io/en/latest/
  - In the docs folder you can setup the structure through the index.rst file.

- **models/**

  - This directory stores the trained models, their predictions, and summaries. Serialized model objects go here so that they can be loaded and used without retraining.

- **references/**

  - Includes additional reference materials such as data dictionaries, manuals, and any other instructional material that helps understand the data and the models.

- **reports/**

  - Stores generated analysis reports, which may include HTML, PDF, or LaTeX files. Subdirectories like **figures/** hold the graphics and plots used or generated by the reports.

- **requirements.txt**

  - Lists all the dependencies required to recreate the analysis environment, typically generated by `pip freeze > requirements.txt`.

- **setup.py**

  - Allows the project directory to be installed as a package, making it easier to import modules within `src`.

- **src/**

  - The source code used in the project is divided into subdirectories for organization:
    - **data/**: Scripts to fetch or generate data.
    - **features/**: Scripts to convert raw data into features suitable for modeling.
    - **models/**: Scripts for training predictive models and applying these models to make predictions.
    - **visualization/**: Scripts to generate visualizations for exploratory analysis and to showcase results.

- **Makefile**

  - Contains commands for common tasks such as `make data` or `make train`, simplifying complex sequences of commands into reusable scripts.

- **tox.ini**

  - Configuration file for tox, a tool for running tests in isolated environments. It ensures that the codebase works across multiple environments and Python versions.

- **.gitignore**
  - This file is the keeper of secrets for your project. It tells Git to ignore things like backup files, personal settings, and system files that don't help anyone else—like those annoying .DS_Store files Macs create. This way, your project stays clean and only shares what's truly useful.

Each component of the project structure plays a role in ensuring that the workflow from data acquisition to modeling is as smooth and error-free as possible. By adhering to this structure, DTU Bioengineering researchers and collaborators can focus more on the research.

## **Virtual environments with uv - avoiding dependency hell**

Think of a virtual environment like having a separate workspace for each of your projects. Each project gets its own Python version and package set, so tools for one project do not accidentally break another one.

This matters because of "dependency hell": one package needs one version of a library, another package needs a different version, and suddenly your setup stops working. A virtual environment gives each project its own isolated "kitchen", so the ingredients stay separate and reproducible.

**Metaphor for dependency hell:** imagine you are baking a cake and a pie at the same time, but you only have one oven. The cake needs one temperature, the pie needs another, and now both recipes are fighting over the same setup. Python packages can behave like that too: two projects may need different versions of the same tool, and they can clash if they share the same environment. A virtual environment gives each project its own "kitchen", so things stop getting mixed up.

We used to recommend **Anaconda/Conda** for this template, and it still works as the older approach. Today, the recommended option is **[`uv`](https://github.com/astral-sh/uv)** because it is much faster, simpler to install, and easy to use for creating environments and installing packages.

### What is uv?

`uv` is a modern Python package and environment manager. You can use it to:

- install Python versions
- create virtual environments
- install packages from `requirements.txt`
- work with `pyproject.toml`
- run Python commands inside the project environment

Compared with older workflows, `uv` is usually much faster and requires fewer steps.

### What is `pyproject.toml`?

`pyproject.toml` is the modern configuration file for Python projects. Think of it as a single place where a project can describe:

- its name and version
- which Python version it expects
- which packages it depends on
- how the project should be built

Older Python projects often use `setup.py` and `requirements.txt` instead. Those files still work, but `pyproject.toml` is the newer and cleaner standard, and tools like `uv` work especially well with it.

This template now includes both approaches so beginners can learn the old style and the modern style side by side.

### Approach 1: quick start with `requirements.txt`

This is the easiest way to get started if you just want to install the packages listed in `requirements.txt`.

1. Install `uv`

   Follow the official installation guide here: [astral.sh/uv](https://docs.astral.sh/uv/).

2. Create a virtual environment in the project folder

   ```bash
   uv venv
   ```

   This creates a `.venv` folder for the project.

3. Activate the environment

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install the project dependencies

   ```bash
   uv pip install -r requirements.txt
   ```

5. Test that Python is set up correctly

   ```bash
   python test_environment.py
   ```

This approach matches many older Python projects and is easy to understand: create an environment, install from a package list, and run your code.

### Approach 2: modern `uv` workflow with `pyproject.toml`

This repository now also includes a `pyproject.toml` file. That lets `uv` understand the project metadata and dependencies directly.

1. Create the environment and install the project

   ```bash
   uv sync
   ```

   This reads `pyproject.toml`, creates or updates `.venv`, and installs the dependencies.

2. Run commands inside that environment

   ```bash
   uv run python test_environment.py
   ```

This is the more modern workflow and is usually the best option once you are comfortable with Python projects.

### Running code with uv

Once the environment is activated, you can run scripts as usual:

```bash
python src/data/make_dataset.py data/raw data/processed
```

You can also run commands through `uv` directly without manually activating the environment:

```bash
uv run python test_environment.py
```

If you are using the `pyproject.toml` workflow, `uv run ...` is often the cleanest option because it uses the project environment automatically.

### Legacy option: Anaconda/Conda

If you already use Anaconda or Conda, that is still fine. Some older parts of this template, such as the `Makefile`, still reference Conda-based setup. But for new users, `uv` is the recommended starting point because it is fast and easy to use.

## **How to use GitHub (through VS code)**

Check out this [introductory video](https://www.youtube.com/watch?v=wpISo9TNjfU) for a quick intro to Git and GitHub.

If you want to get going quickly check out [this video](https://www.youtube.com/watch?v=i_23KUAEtUM) to use GitHub and VS code.

## **Contributions**

Contributions are welcome! Please fork the project, make your changes, and submit a pull request. For major changes, open an issue first to discuss what you'd like to change.

## **Credits**

Cookiecutter Data Science was used to make the file structure of this project. You can find a guide on how to use it [here](https://drivendata.github.io/cookiecutter-data-science/).

## **QUESTIONS**

If you have any questions about how to organize your research please reach out to Lucas (GitHub user: hiyama341) at luclev@dtu.dk.
