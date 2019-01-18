# charred_cheetos
Johnson Li (PM), Kenny Li, Joyce Liao, Cheryl Qian

## Alphabet Goop

### Video Demo
[Part 1](https://youtu.be/vN_JRHyEJKk)

[Part 2](https://youtu.be/Xv5P73Mk14k)

### Project Overview
Our app is an in-browser word search game. Users can choose from a variety of categories or create their own puzzle with customizable size and category. For default categories, logged in users can view their personal best upon their first completion of a specific category.

App uses the Datamuse API, but no API key is needed to retrieve data.

### Launch Instructions
#### Running Flask App
1. Go to [root repository](https://github.com/JohnsonLi/charred_cheetos) and click "Clone or Download" button
2. Copy the ssh/https link and run `$ git clone <link>`
3. Make sure the latest version of Python (currently Python 3.7.1) is installed. If not, download it [here](https://www.python.org/downloads/).
4. Install virtualenv by running `$ pip install virtualenv`
   * Make a venv by running `$ python3 -m venv ENV_DIR`
   * Activate it by running `$ . /ENV_DIR/bin/activate`
   * Deactivate it by running `$ deactivate`
5. **With your virtual environment activated**, download all of the app's dependencies by running 
```
 (venv)$ pip install -r requirements.txt
```
6. Run `$ python app.py`
7. Launch the root route (http://127.0.0.1:5000/) in your browser to go to the login page.

#### API information
##### Datamuse
* Provide the words used to generate each word search puzzle
* No API key is required
