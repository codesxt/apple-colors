# Apple Server

virtualenv -p python3.5 venv --system-site-packages

pip install -r requirements.txt

Add this to venv/bin/activate
				TK_LIBRARY=/usr/lib/python3.5/tkinter/
				TK_PATH=/usr/lib/python3.5/tkinter/
				TCL_LIBRARY=/usr/lib
				export TCL_LIBRARY TK_LIBRARY TK_PATH

ref: http://www.australsounds.com/2014/04/virtualenvgit-how-to.html
