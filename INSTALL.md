# **Installation**

## 🧬 **1 - Cloning**

Clone the repository into your machine:

```shell
git clone https://github.com/Nuno-Jesus/blender-dsc-time-exporter.git
```

> [!NOTE]
> If you want to give a name into the folder, you can specify the name as an extra parameter, like so: `git clone https://github.com/Nuno-Jesus/blender-dsc-time-exporter.git name_of_the_folder`

## ⚙️ **2 - Uploading to Blender**

**2.1.** Open Blender, navigate to the `Edit` tab and select the `Preferences` option:

![Blender Edit Tab](blender_edit_tab.png)

A window like this should be rendered:

![Blender Preferences Window](blender_preferences_window.png)

**2.2** Navigate to the `Add-ons` tab and click on `Install`

![Blender Add-ons Tab](blender_addons_tab.png)

You should now search for the folder that has this repository cloned and select the `dsc_time_exporter_main.py` file. Click on `Install Add-on` and the module will be imported.

**2.3** If you search for "dsc", you should now see a new entry on the add-on list. Make sure you toggle the checkbox to activate the plugin.

![Blender Addon Uploaded](blender_addon_uploaded.png)

## ✅ **3 - Final checks**

If all went smoothly, you should now see a new panel on the right side of the timeline. Proceed to click on the small arrow on the right, just under the scroll bar:

![Blender Timeline Arrow](blender_timeline_arrow.png)

The new panel, called `DSC Time Converter` should now be visible.

![Blender New Addon](blender_new_addon.png)