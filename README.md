# ESRS Group 9
### Bingle - A book lending app built using Django, Python, HTML, and JavaScript. Deployed on Kubernetes and Docker.

### Objectives
Bingle originated from the minds of University of Sussex students, initially as a modest academic project. Yet, it quickly evolved into a beacon of sustainability and community for book lovers. Beyond assessment criteria, it now promotes healthy book exchange, fostering connections and saving budgets.

### Website
Portal can be accessed from [Bingle](http://bingle.amanthapa.com.np)

### Documentation
- [Project Plan](./Documents/Project-Plan-Grp-6.pdf)
- [Reflective Essay](./Documents/947G5_Group_6_Reflective_Essay.pdf)
- [Technical Documentation](./portal/portal_app/static/portal_app/doc/technical.pdf)

### Code Docstrings
- Code docstrings have been generated using Sphinx that describes all our function and can be found [here](Bingle/docs).

All the tickets opened for bugs and issues can be found [Here](https://github.com/thepercyj/esrs-group-9/issues?q=is%3Aissue+is%3Aclosed).

Follow us for more exciting future projects below:
- [Rohan Kadam](https://github.com/Rez27)
- [Tom Naccarato](https://github.com/tnaccarato)
- [Jawad Nasar Shah](https://github.com/jawadnasar)
- [Mya Lwin](https://github.com/Mya2328)
- [Moldir Zhumakhazhi](https://github.com/Moka364mz)
- [Rob Ryan](https://github.com/RobRyan1122)

# Local Installation Guide

Install Visual Studio Code (VSCode):

### Step 1  
Go to the official VSCode [Website](https://code.visualstudio.com/download)
Download the installer for your operating system (Windows, macOS, or Linux).
Run the installer and follow the installation prompts.
Install PyCharm (Optional):

**OR**

If you also want to install PyCharm Community Version, go to the official PyCharm [Website](https://code.visualstudio.com/download)
Download the installer for your operating system.
Run the installer and follow the installation prompts.

### Step 2
Download our project and Extract the Zip Source Folder :
Locate the source folder you want to extract.
Right-click on the folder and choose "Extract" or use a zip utility program to extract the contents.
Open the Project Folder in VSCode:

### Step 3
Install Python Packages from requirements.txt:
Open a terminal or command prompt.
Navigate to the project directory where requirements.txt is located.
Run the following command to install the required packages:
```markdown
pip install -r requirements.txt
```

### Step 4  
Launch VSCode.
Click on "File" in the menu and select "Open Folder".
Navigate to the location where you extracted the source folder, select it, and click "Open".

### Step 5  
Open a terminal within VSCode (click on "Terminal" in the menu, then "New Terminal").
Navigate to the project directory (where manage.py is located).
Run the following command to start the Django server:
```markdown
cd Bingle ; python manage.py runserver
```
**OR**
```markdown
cd Bingle ; python manage.py runserver 0.0.0.0: xxxx ( Replace xxxx with any port you want to use to run the server on aside from default 8000)
```

Now open a web browser and browse the following address:
```markdown
http://localhost:8000 or http://127.0.0.1:8000
```
The server should now be running, That's it!!. Enjoy playing !!

