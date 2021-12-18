# Add baloon plugin
This is a gimp plugin to create manga baloon easy.

## How to install
1) Download file and unzip if it is zipped so that you get file with .py extension.
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
gimp
```

## How to use

* select an area
![select area](imgs/demo1.png)

* go to select Add baloon...
![add baloon](imgs/demo2.png)

* insert text and specify font and font size
![insert text](imgs/demo3.png)

* here the results
![result](imgs/demo4.png)

