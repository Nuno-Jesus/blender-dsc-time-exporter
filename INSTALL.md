# **Installation**

> [!NOTE]
> At the moment, I'm using Blender 4.0.2.

## 🧬 **1 - Cloning**

Clone the repository into your machine:

```shell
git clone https://github.com/Nuno-Jesus/blender-dsc-time-exporter.git
```

> [!NOTE]
> If you want to give a name into the folder, you can specify the name as an extra parameter, like so: `git clone https://github.com/Nuno-Jesus/blender-dsc-time-exporter.git name_of_the_folder`

## ⚙️ **2 - Uploading to Blender**

**2.1.** Open Blender, navigate to the `Edit` tab and select the `Preferences` option:

<div align=center>
	<image src="images/blender_edit_tab.png" alt="Blender Edit Tab">
</div>

A window like this should be rendered:

<div align=center>
	<image src="images/blender_preferences_window.png" alt="Blender Preferences Window">
</div>

**2.2** Navigate to the `Add-ons` tab and click on `Install`

<div align=center>
	<image src="images/blender_addons_tab.png" alt="Blender Add-ons Tab">
</div>

You should now search for the folder that has this repository cloned and select the `dsc_time_exporter_main.py` file. Click on `Install Add-on` and the module will be imported.

**2.3** If you search for "dsc", you should now see a new entry on the add-on list. Make sure you toggle the checkbox to activate the plugin.

<div align=center>
	<image src="images/blender_addon_uploaded.png" alt="Blender Addon Uploaded">
</div>

## ✅ **3 - Final checks**

If all went smoothly, you should now see a new panel on the right side of the timeline. Proceed to click on the small arrow on the right, just under the scroll bar:

<div align=center>
	<image src="images/blender_timeline_arrow.png" alt="Blender Timeline Arrow">
</div>

The new panel should now be visible.

<div align=center>
	<image src="images/blender_new_addon.png" alt="Blender New Addon">
</div>