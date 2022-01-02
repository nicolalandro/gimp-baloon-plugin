# Add baloon plugin
This is a gimp plugin to create manga balloon easy.

## How to install

### For Gimp 2.99.* and 3.*
1) download the folder add_baloon
2) Inside GIMP program, go to Edit -> Preferences -> Folders -> Plug-Ins and see the folder/path listed.
3) Copy/Move the add_balloon folder from step 1 to one of one of those folders.
4) If you're on Linux, you'll have to browse to the file and right click on it, the Properties, Permissions Tab, Allow Execute as Program (to make it executable). Ex. chmod +x add_balloon/add_balloon.py
5) Restart GIMP.
6) And now plug-in is active for use.

Linux steps example
```
cd ~/.var/app/org.gimp.GIMP/config/GIMP/2.99/plug-ins
mkdir add_balloon
cd add_balloon
wget https://raw.githubusercontent.com/nicolalandro/gimp-baloon-plugin/master/add_balloon/add_balloon.py
chmod +x new_baloon_text.py
# run gimp
```

### For Other Gimp version
1) Download new_baloon_text.py file
2) Inside GIMP program, go to Edit -> Preferences -> Folders -> Plug-Ins and see the folder/path listed.
3) Copy/Move the .py file from step 1 to one of one of those folders.
4) If you're on Linux, you'll have to browse to the file and right click on it, the Properties, Permissions Tab, Allow Execute as Program (to make it executable). Ex. chmod +x new_baloon_text.py
5) Restart GIMP.
6) And now plug-in is active for use.


Linux steps (For GIMP 2.10):
```
cd ~/.config/GIMP/2.10/plug-ins
wget https://raw.githubusercontent.com/nicolalandro/gimp-baloon-plugin/master/new_baloon_text.py 
chmod +x new_baloon_text.py  
# run gimp
```

## How to use

## Python3 version
* select an area
![select area](imgs/python3/demo1.png)

* go to select Add baloon...
![add baloon](imgs/python3/demo2.png)

* insert text and specify font and font size
![insert text](imgs/python3/demo3.png)

* here the results
![result](imgs/python3/demo4.png)

## Python2 version
* select an area
![select area](imgs/python2/demo1.png)

* go to select Add baloon...
![add baloon](imgs/python2/demo2.png)

* insert text and specify font and font size
![insert text](imgs/python2/demo3.png)

* here the results
![result](imgs/python2/demo4.png)

## Development references
Here I put some reference to study how to develop a plugin like this
* GTK: UI framework
  * [Glade](https://glade.gnome.org/): UI tool to create .glade xml ui
GIMP python plugin:
  * [Gimp Doc Python2](https://www.gimp.org/docs/python/index.html): Old gimp documentation obout python2 (it is used for the first version of the plugin)
  * [Create Python3 Plugin for GIMP: The basics](https://z-uo.medium.com/create-python3-plugin-for-gimp-the-basics-94ede94e9d1f): how to develop python3 plugin (GIMP 2.99.*)
  * [Forum - Develop Python3 plugin for GIMP](https://www.gimp-forum.net/Thread-Learn-to-create-Python3-plugins): discussion thread
