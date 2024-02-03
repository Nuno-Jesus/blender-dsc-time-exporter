# **DSC Time Exporter**
A Blender 4.0.2 add-on. Provides the ability to convert the Blender frames to [Project Diva](https://store.steampowered.com/app/1761390/Hatsune_Miku_Project_DIVA_Mega_Mix/) timestamps.

<!-- ## 📝 **Authorship** -->

## 📒 **About**
This repo houses a Blender add-on designed to help a friend of mine. The add-on automatically calculates the Project Diva time on a given frame. This time is used in some files to coordinate in-game animations, switch stages, add 2D/3D effects, etc. You can then export that time depending 

<!-- ## 🚨 **Disclaimer** -->
<!-- You're free  -->

## 🕹️ **Features**
The current section will explain what the add-on is for. Carefully read through the next sections.

- ### **Display the current DSC Time**
Depending on the frame you're on, the main panel will display the current DSC time. This conversion is done, depending on the frame rate selected for the scene.

<!-- GIF -->

- ### **Export the current DSC Time**
The second subpanel has 2 buttons. Click on the `Copy Current DSC Time` button to copy the current frame DSC time.

<!-- GIF -->

You'll notice the output is not quite what you expected. It comes with a lot of DSC commands, but the time is there. If don't feel like having all these commands when copying the time, you need to change the source code. More info [here](#👨🏻‍💻-changing-source-code)

- ### **Export all timeline markers DSC Time**
Need to export several frames? Using timeline markers, you can select multiple frames. Then, click on `Copy All Markers DSC Time` button to export them all, sorted by ascending order of time.

<!-- GIF -->

- ### **Append extra lines to the output**
If you are in dire need of appending further lines to each marker, you can explore the `Extra Text` subpanel. From there, you can add as many lines as you need. You can also remove some or all lines if not needed anymore.

<!-- GIF -->

## 👨🏻‍💻 **Changing Source Code**
If you're not feeling comfortable with the add-on output, you can change it and it's not that hard! On the `dsc_time_exporter_main.py`, look for this function:

```py
def stringify_marker(dsc_time, i=1):
	return f'TIME({dsc_time});\n' + \
		f'CHANGE_FIELD({i});\n' + \
		'MOVIE_DISP(1);\n' + \
		'MOVIE_PLAY(1);\n' + \
		'DATA_CAMERA(0, 1);\n'
```

The `dsc_time` parameter is what you're looking for. Supposing you only want this, the new code should look like this:

```py
def stringify_marker(dsc_time, i=1):
	return f'{dsc_time}\n'
```

Please, **keep the `\n` so line breaks are applied**!
## 📚 **Resources**

- [Blender API](https://docs.blender.org/api/current/index.html)