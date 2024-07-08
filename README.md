# Diacare App

Welcome to the Diacare App project! Follow these instructions to set up your development environment and start coding.

## Setup Instructions

### Step 1: Install recommended extensions

1. While waiting for the GitHub Codespace to finish setting up, install the recommended Visual Studio Code extensions by clicking on the Extensions icon in the Activity Bar on the left then the small cloud icon to install all recommended extensions.

### Step 2: Open the Terminal in VS Code

1. Open the Command Palette by pressing `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac).
1. Type "Terminal: Create New Terminal" and select it. This will open a terminal window at the bottom of VS Code.

### Step 3: Navigate to the Project Directory

In the terminal, navigate to the project directory by running:

```sh
cd /workspaces/diacare-project
```

Replace /workspaces/diacare-project with the path to your project directory if it's different.

### Step 4: Set Up a New Virtual Environment

Create a new virtual environment named venv by running:

```sh
python -m venv venv
```

### Step 5: Activate the Virtual Environment

Activate the virtual environment:

- On Windows:
  ```sh
  .\venv\Scripts\activate
  ```
- On macOS and Linux:
  ```sh
  source venv/bin/activate
  ```

### Step 6: Install Dependencies

> **IMPORTANT**: Make sure you have the virutal environment activated!

Install the project dependencies from the requirements.txt file by running:

```sh
pip install -r requirements.txt
```

This should install streamlit as well as pandas, numpy, and scikit-learn for you. Feel free to pip install any other dependencies.

## Writing and Running Your First Python Script

Let's write a simple Python script that prints "Hello, World!" and run it from the IDE.

1. Create a New File:
   - In VS Code, click on the Explorer icon in the Activity Bar on the left.
   - Click on the New File icon and name the file hello_world.py.
1. Write the Script:

   - Open hello_world.py and add the following code:

   ```py
   print("Hello, World!")
   ```

1. Run the Script:

   - Right-click on the hello_world.py file in the Explorer and select Run Python File in Terminal.
   - Alternatively, you can run the script from the terminal by ensuring the virtual environment is activated and then running:

   ```sh
   python hello_world.py
   ```

You should see the output Hello, World! printed in the terminal.

Congratulations! You've successfully set up your development environment, installed the necessary dependencies, and run your first Python script.

For more information on using Streamlit and developing this project, refer to the [Streamlit documentation](https://docs.streamlit.io/develop/tutorials).

Happy coding!
