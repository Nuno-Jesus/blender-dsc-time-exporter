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
		"DATA_CAMERA(0, 1);\n"


###########################################################################################

class NewLineItem(bpy.types.PropertyGroup):
	value: StringProperty()

###########################################################################################

class ClearLinesOperator(bpy.types.Operator):
	bl_idname = "dsc_marker_exporter.clear_lines"
	bl_label = "Deletes all added lines"

	def execute(self, context):
		context.scene.lines.clear()
		return {'FINISHED'}

###########################################################################################

class AddNewLineOperator(bpy.types.Operator):
	bl_idname = "dsc_marker_exporter.add_new_line"
	bl_label = "Adds a new line to export alongside the marker time"

	def execute(self, context):
		lines = context.scene.lines
		new_line = lines.add()
		return {'FINISHED'}
		
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
		lines = context.scene.lines
		all_markers_time = ""
		all_lines = ''.join([f"{line.value}\n" for line in lines])

		print(all_lines)

		sorted_frames = sorted(map(lambda marker: marker.frame, bpy.context.scene.timeline_markers))
		for i, frame in enumerate(sorted_frames):
			dsc_time = frame_to_dsctime(frame, fps=self.fps)
			all_markers_time += stringify_marker(dsc_time, i + 1) + all_lines

		context.window_manager.clipboard = all_markers_time
		self.report({'INFO'}, "Copied all markers to the clipboard!")

		return {'FINISHED'}
	
###########################################################################################
	
class AddonMainPanel(bpy.types.Panel):
	bl_idname = "dsc_marker_exporter.addon_main_panel"
	bl_label = "DSC Marker Export"
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'
	bl_options = {'DEFAULT_CLOSED'}

	def calculate(self, scene):
		self.fps = int(scene.render.fps / scene.render.fps_base)
		if self.fps != 60:
			self.layout.label(text="Warning: Scene FPS is not set to 60", icon='ERROR')
		self.dsc_current = frame_to_dsctime(scene.frame_current, fps=self.fps)

	def draw_info(self, scene):
		self.layout.label(text=f"Current Frame: {scene.frame_current}")
		self.layout.label(text=f"Current Frame DSC Time: {self.dsc_current}")

	def draw_buttons_area(self, lines):
		all_lines = ''.join([f"{line.value}\n" for line in lines])

		copy_one_button = self.layout.operator(CopyOneMarkerOperator.bl_idname, text="Copy DSC Time to Clipboard")
		copy_one_button.dsc_time = stringify_marker(self.dsc_current) + all_lines

		copy_all_button = self.layout.operator(CopyAllMarkersOperator.bl_idname, text="Copy all markers to Clipboard")
		copy_all_button.fps = self.fps

	def draw(self, context):
		scene = context.scene
		lines = scene.lines

		self.calculate(scene)
		self.draw_info(scene)
		self.draw_buttons_area(lines)
		
###########################################################################################
		
class AddonSecondPanel(bpy.types.Panel):
	bl_idname = "dsc_marker_exporter.addon_second_panel"
	bl_label = "Advanced"
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'
	bl_options = {'DEFAULT_CLOSED'}
	bl_parent_id = 'dsc_marker_exporter.addon_main_panel'

	def draw(self, context):
		scene = context.scene
		lines = scene.lines

		for line in lines:
			self.layout.prop(line, "value")
		row = self.layout.row()
		row.operator(AddNewLineOperator.bl_idname, text="New line")
		row.operator(ClearLinesOperator.bl_idname, text="Clear")

###########################################################################################

classes = [NewLineItem, AddNewLineOperator, ClearLinesOperator, \
		CopyAllMarkersOperator, CopyOneMarkerOperator, AddonMainPanel, AddonSecondPanel]

def update_panel(scene, context):
	pass

def register():
	for temp in classes:
		bpy.utils.register_class(temp)
	
	bpy.app.handlers.frame_change_post.append(update_panel)
	bpy.types.Scene.lines = bpy.props.CollectionProperty(type=NewLineItem)

def unregister():
	for temp in classes:
		bpy.utils.unregister_class(temp)
	
	if update_panel in bpy.app.handlers.frame_change_post:
		bpy.app.handlers.frame_change_post.remove(update_panel)
	del bpy.types.Scene.lines

if __name__ == "__main__":
	register()
