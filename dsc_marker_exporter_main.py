bl_info = {
	'name': 'DSC Marker Exporter Addon',
	'author': 'Nuno-Jesus',
	'version': (1, 0, 0),
	'blender': (4, 0, 2),
	'location': 'Dope Sheet',
	'description': '',
	'warning': '',
	'wiki_url': '',
	'category': 'Animation',
}

import bpy
from bpy.props import StringProperty, IntProperty

def frame_to_dsctime(frame, fps=60):
	seconds = frame / fps
	time = seconds * 100000
	return int(time)

def stringify_marker(dsc_time, i=1):
	return f'TIME({dsc_time});\n' + \
		f'CHANGE_FIELD({i});\n' + \
		'MOVIE_DISP(1);\n' + \
		'MOVIE_PLAY(1);\n' + \
		'DATA_CAMERA(0, 1);\n'


###########################################################################################

class NewLineProperty(bpy.types.PropertyGroup):
	value: StringProperty()

###########################################################################################

class ClearLinesOperator(bpy.types.Operator):
	bl_idname = 'dsc_marker_exporter.clear_lines'
	bl_label = 'Clear'
	bl_description = 'Deletes all the added lines.'

	def execute(self, context):
		context.scene.lines.clear()
		return {'FINISHED'}

###########################################################################################

class AddLineOperator(bpy.types.Operator):
	bl_idname = 'dsc_marker_exporter.add_line'
	bl_label = 'New Line'
	bl_description = 'Adds a new line to export alongside the marker time'

	def execute(self, context):
		lines = context.scene.lines
		lines.add()
		return {'FINISHED'}

###########################################################################################

class DeleteLineOperator(bpy.types.Operator):
	bl_idname = 'dsc_marker_exporter.delete_line'
	bl_label = ''
	bl_description = 'Deletes a line property that is bounded with this operator. The ' + \
		'deleted line will no longer be added to the clipboard.'

	i: IntProperty()

	def execute(self, context):
		lines = context.scene.lines
		lines.remove(self.i)
		return {'FINISHED'}
		
###########################################################################################

class CopyCurrentFrameOperator(bpy.types.Operator):
	bl_idname = 'dsc_marker_exporter.copy_one_marker_to_clipboard'
	bl_label = 'Copy Current DSC Time'
	bl_description = 'Copies the DSC time of the current frame to the clipboard. The generated ' + \
		'text comes like this:\n' + 'TIME({dsc_time});\n' + \
		'CHANGE_FIELD({i});\n' + \
		'MOVIE_DISP(1);\n' + \
		'MOVIE_PLAY(1);\n' + \
		'DATA_CAMERA(0, 1);\n'
	
	dsc_time: StringProperty()

	def execute(self, context):
		context.window_manager.clipboard = self.dsc_time
		self.report({'INFO'}, 'Copied the selected marker to the clipboard!')
		return {'FINISHED'}
	
###########################################################################################

class CopyAllMarkersOperator(bpy.types.Operator):
	bl_idname = 'dsc_marker_exporter.copy_all_markers_to_clipboard'
	bl_label = 'Copy All Markers DSC Time'
	bl_description = 'Converts all timeline markers to DSC Time and copies them to the clipboard.' + \
		'Every marker is bound to have the same default text, as stated in the operator above.'

	fps: IntProperty()

	def execute(self, context):
		lines = context.scene.lines
		all_markers_time = ''
		all_lines = ''.join([f'{line.value}\n' for line in lines])

		print(all_lines)

		sorted_frames = sorted(map(lambda marker: marker.frame, bpy.context.scene.timeline_markers))
		for i, frame in enumerate(sorted_frames):
			dsc_time = frame_to_dsctime(frame, fps=self.fps)
			all_markers_time += stringify_marker(dsc_time, i + 1) + all_lines

		context.window_manager.clipboard = all_markers_time
		self.report({'INFO'}, 'Copied all markers to the clipboard!')

		return {'FINISHED'}
	
###########################################################################################
	
class AddonMainPanel(bpy.types.Panel):
	bl_idname = 'dsc_marker_exporter.addon_main_panel'
	bl_label = 'DSC Time Converter'
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'

	def calculate(self, scene):
		self.fps = int(scene.render.fps / scene.render.fps_base)
		self.dsc_current = frame_to_dsctime(scene.frame_current, fps=self.fps)

	def draw_info(self, scene):
		self.layout.label(text=f'Current DSC Time: {self.dsc_current}')

	def draw(self, context):
		scene = context.scene

		self.calculate(scene)
		self.draw_info(scene)
		
###########################################################################################
		
class AddonSecondPanel(bpy.types.Panel):
	bl_idname = 'dsc_marker_exporter.addon_second_panel'
	bl_label = 'Extra Text'
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'
	bl_options = {'DEFAULT_CLOSED'}
	bl_parent_id = 'dsc_marker_exporter.addon_main_panel'

	def draw(self, context):
		scene = context.scene
		lines = scene.lines

		for i, line in enumerate(lines):
			split = self.layout.split(factor=0.9)
			
			split.prop(line, 'value')
			button = split.operator(DeleteLineOperator.bl_idname, icon='CANCEL')
			button.i = i

		row = self.layout.row()
		row.operator(AddLineOperator.bl_idname, text='New line', icon='ADD')
		row.operator(ClearLinesOperator.bl_idname, text='Clear', icon='TRASH')

###########################################################################################
		
class AddonThirdPanel(bpy.types.Panel):
	bl_idname = 'dsc_marker_exporter.addon_third_panel'
	bl_label = 'Export'
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'
	bl_parent_id = 'dsc_marker_exporter.addon_main_panel'

	def calculate(self, scene):
		self.fps = int(scene.render.fps / scene.render.fps_base)
		if self.fps != 60:
			self.layout.label(text='Warning: Scene FPS is not set to 60', icon='ERROR')
		self.dsc_current = frame_to_dsctime(scene.frame_current, fps=self.fps)

	def draw_buttons_area(self, lines):
		all_lines = ''.join([f'{line.value}\n' for line in lines])

		copy_one_button = self.layout.operator(CopyCurrentFrameOperator.bl_idname, text='Copy Current DSC Time')
		copy_one_button.dsc_time = stringify_marker(self.dsc_current) + all_lines

		copy_all_button = self.layout.operator(CopyAllMarkersOperator.bl_idname, text='Copy All Markers DSC Time')
		copy_all_button.fps = self.fps

	def draw(self, context):
		scene = context.scene
		lines = scene.lines

		self.calculate(scene)
		self.draw_buttons_area(lines)

###########################################################################################

classes = [ 
	NewLineProperty, AddLineOperator, ClearLinesOperator, DeleteLineOperator,
	CopyAllMarkersOperator, CopyCurrentFrameOperator, AddonMainPanel, AddonSecondPanel, 
	AddonThirdPanel
]

def update_panel(scene, context):
	pass

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	bpy.app.handlers.frame_change_post.append(update_panel)
	bpy.types.Scene.lines = bpy.props.CollectionProperty(type=NewLineProperty)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
	
	if update_panel in bpy.app.handlers.frame_change_post:
		bpy.app.handlers.frame_change_post.remove(update_panel)
	del bpy.types.Scene.lines

if __name__ == '__main__':
	register()
