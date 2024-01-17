bl_info = {
	"name": "DSC Marker Exporter Addon",
	"author": "Nuno-Jesus",
	"version": (1, 0, 0),
	"blender": (4, 0, 2),
	"location": "Dope Sheet",
	"description": "",
	"warning": "",
	"wiki_url": "",
	"category": "Animation",
}

import bpy
from bpy.props import StringProperty, IntProperty


def frame_to_dsctime(frame, fps=60):
	seconds = frame / fps
	time = seconds * 100000
	return int(time)

def stringify_marker(custom_time, i=1):
	return f"TIME({custom_time});\n" + \
		f"CHANGE_FIELD({i});\n" + \
		"MOVIE_DISP(1);\n" + \
		"MOVIE_PLAY(1);\n" + \
		"DATA_CAMERA(0, 1);\n" + \
		"SET_MOTION(0, 1, -1, 1000);\n" + \
		"SET_MOTION(1, 1, -1, 1000);\n" + \
		"SET_MOTION(2, 1, -1, 1000);\n"

###########################################################################################

class MyProperties(bpy.types.PropertyGroup):
	prefix: StringProperty()
	suffix: StringProperty()


###########################################################################################

class CopyOneMarkerOperator(bpy.types.Operator):
	bl_idname = "dsc_marker_exporter.copy_one_marker_to_clipboard"
	bl_label = "Copies the DSC time of 1 marker to the clipboard"
	
	dsc_time: StringProperty()

	def execute(self, context):
		context.window_manager.clipboard = self.dsc_time
		self.report({'INFO'}, "Copied the selected marker to the clipboard!")
		return {'FINISHED'}
	
###########################################################################################

class CopyAllMarkersOperator(bpy.types.Operator):
	bl_idname = "dsc_marker_exporter.copy_all_markers_to_clipboard"
	bl_label = "Copies the DSC time of all markers to the clipboard"

	fps: IntProperty()

	def execute(self, context):
		all_markers_time = ""

		sorted_frames = sorted(map(lambda marker: marker.frame, bpy.context.scene.timeline_markers))
		for i, frame in enumerate(sorted_frames):
			dsc_time = frame_to_dsctime(frame, fps=self.fps)
			all_markers_time += stringify_marker(dsc_time, i + 1)

		context.window_manager.clipboard = all_markers_time
		self.report({'INFO'}, "Copied all markers to the clipboard!")
		return {'FINISHED'}
	
###########################################################################################
	
class AddonMainPanel(bpy.types.Panel):
	bl_idname = "dsc_marker_exporter.addon_main_panel"
	bl_label = "DSC Marker Export"
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		addon_props = scene.addon_props

		layout.prop(addon_props, "prefix")

		# Check the scene's frame rate
		fps = int(scene.render.fps / scene.render.fps_base)
		if fps != 60:
			layout.label(text="Warning: Scene FPS is not set to 60", icon='ERROR')

		# Display the custom time for the current frame
		current_frame = scene.frame_current
		custom_time = frame_to_dsctime(current_frame, fps=fps)

		# Use a label to display the custom time
		layout.label(text=f"DSC Time: {custom_time}")

		# Add a button to copy the custom time to the clipboard
		copy_one_button = layout.operator(CopyOneMarkerOperator.bl_idname, text="Copy DSC Time to Clipboard")
		# copy_one_button.dsc_time = stringify_marker(custom_time)
		copy_one_button.dsc_time = addon_props.prefix

		copy_all_button = layout.operator(CopyAllMarkersOperator.bl_idname, text="Copy all markers to Clipboard")
		copy_all_button.fps = fps
		
###########################################################################################

classes = [MyProperties, CopyAllMarkersOperator, CopyOneMarkerOperator, AddonMainPanel]

def update_panel(scene, context):
	pass

def register():
	for temp in classes:
		bpy.utils.register_class(temp)
	
	bpy.app.handlers.frame_change_post.append(update_panel)
	bpy.types.Scene.addon_props = bpy.props.PointerProperty(type=MyProperties)

def unregister():
	for temp in classes:
		bpy.utils.unregister_class(temp)
	
	if update_panel in bpy.app.handlers.frame_change_post:
		bpy.app.handlers.frame_change_post.remove(update_panel)
	del bpy.types.Scene.addon_props

if __name__ == "__main__":
	register()
