bl_info = {
	'name': 'DSC Time Exporter Addon',
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

#! YOU CAN CHANGE THE DEFAULT TEXT HERE
def stringify_marker(dsc_time, i=1):
	return f'TIME({dsc_time});\n' + \
		f'CHANGE_FIELD({i});\n' + \
		'MOVIE_DISP(1);\n' + \
		'MOVIE_PLAY(1);\n' + \
		'DATA_CAMERA(0, 1);\n'

def calculate(scene):
	fps = scene.render.fps / scene.render.fps_base
	dsc_current = frame_to_dsctime(scene.frame_current, fps=fps)

	return fps, dsc_current

###########################################################################################

class NewLineProp(bpy.types.PropertyGroup):
	value: StringProperty()

###########################################################################################

class DSC_TIME_CONVERTER_OT_clear_lines(bpy.types.Operator):
	bl_idname = 'dsc_time_converter.clear_lines_button'
	bl_label = 'Clear'
	bl_description = 'Deletes all the added lines'

	def execute(self, context):
		context.scene.lines.clear()
		return {'FINISHED'}

###########################################################################################

class DSC_TIME_CONVERTER_OT_add_line(bpy.types.Operator):
	bl_idname = 'dsc_time_converter.add_line_button'
	bl_label = 'New Line'
	bl_description = 'Adds a new line to export alongside the marker time'

	def execute(self, context):
		lines = context.scene.lines
		lines.add()
		return {'FINISHED'}

###########################################################################################

class DSC_TIME_CONVERTER_OT_delete_line(bpy.types.Operator):
	bl_idname = 'dsc_time_converter.delete_line_button'
	bl_label = ''
	bl_description = 'Deletes a line property that is bounded with this operator. The ' + \
		'deleted line will no longer be added to the clipboard'

	i: IntProperty()

	def execute(self, context):
		lines = context.scene.lines
		lines.remove(self.i)
		return {'FINISHED'}
		
###########################################################################################

class DSC_TIME_CONVERTER_OT_copy_current_frame(bpy.types.Operator):
	bl_idname = 'dsc_time_converter.copy_current_frame_button'
	bl_label = 'Copy Current DSC Time'
	bl_description = 'Copies the DSC time of the current frame to the clipboard. The generated ' + \
		'text comes like this:\n' + 'TIME({dsc_time});\n' + \
		'CHANGE_FIELD({field_num});\n' + \
		'MOVIE_DISP(1);\n' + \
		'MOVIE_PLAY(1);\n' + \
		'DATA_CAMERA(0, 1);\n'
	
	dsc_time: StringProperty()

	def execute(self, context):
		context.window_manager.clipboard = self.dsc_time
		self.report({'INFO'}, 'Copied the selected marker to the clipboard!')
		return {'FINISHED'}
	
###########################################################################################

class DSC_TIME_CONVERTER_OT_copy_all_markers(bpy.types.Operator):
	bl_idname = 'dsc_time_converter.copy_all_markers_button'
	bl_label = 'Copy All Markers DSC Time'
	bl_description = 'Converts all timeline markers to DSC Time and copies them to the clipboard.'

	fps: IntProperty()

	def execute(self, context):
		lines = context.scene.lines
		all_new_lines = ''.join([f'{line.value}\n' for line in lines])
		buffer = ''

		sorted_frames = sorted(map(lambda marker: marker.frame, bpy.context.scene.timeline_markers))
		for i, frame in enumerate(sorted_frames):
			dsc_time = frame_to_dsctime(frame, fps=self.fps)
			buffer += stringify_marker(dsc_time, i + 1) + all_new_lines

		context.window_manager.clipboard = buffer
		self.report({'INFO'}, 'Copied all markers to the clipboard!')

		return {'FINISHED'}
	
###########################################################################################
	
class DSC_TIME_CONVERTER_PT_main(bpy.types.Panel):
	bl_idname = 'dsc_time_converter.main_panel'
	bl_label = 'DSC Time Converter'
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'

	def draw(self, context):
		scene = context.scene

		self.fps, self.dsc_current = calculate(scene)
		self.layout.label(text=f'Current DSC Time: {self.dsc_current}')
		
###########################################################################################
		
class DSC_TIME_CONVERTER_PT_sub_1(bpy.types.Panel):
	bl_idname = 'dsc_time_converter.subpanel_1'
	bl_label = 'Extra Text'
	bl_description = 'If you need, you can add more lines to be copied alongside the default' + \
		'text. Every marker is bound to have the default text and the new lines you add to it'
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'
	bl_options = {'DEFAULT_CLOSED'}
	bl_parent_id = DSC_TIME_CONVERTER_PT_main.bl_idname

	def draw(self, context):
		scene = context.scene
		lines = scene.lines

		row = self.layout.row()
		row.operator(DSC_TIME_CONVERTER_OT_add_line.bl_idname, text='New line', icon='ADD')
		row.operator(DSC_TIME_CONVERTER_OT_clear_lines.bl_idname, text='Clear', icon='TRASH')

		for i, line in enumerate(lines):
			split = self.layout.split(factor=0.9)
			
			split.prop(line, 'value')
			button = split.operator(DSC_TIME_CONVERTER_OT_delete_line.bl_idname, icon='CANCEL')
			button.i = i

###########################################################################################
		
class DSC_TIME_CONVERTER_PT_sub_2(bpy.types.Panel):
	bl_idname = 'dsc_time_converter.subpanel_2'
	bl_label = 'Export'
	bl_description = 'Export your markers'
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'
	bl_parent_id = DSC_TIME_CONVERTER_PT_main.bl_idname

	def draw_buttons_area(self, lines):
		if self.fps != 60:
			self.layout.label(text=f"Scene FPS should be 60 (current is {round(self.fps, 2)})", icon='ERROR')
		
		all_new_lines = ''.join([f'{line.value}\n' for line in lines])

		copy_marker_button = self.layout.operator(DSC_TIME_CONVERTER_OT_copy_current_frame.bl_idname, text='Copy Current DSC Time')
		copy_marker_button.dsc_time = stringify_marker(self.dsc_current) + all_new_lines

		copy_all_button = self.layout.operator(DSC_TIME_CONVERTER_OT_copy_all_markers.bl_idname, text='Copy All Markers DSC Time')
		copy_all_button.fps = self.fps

	def draw(self, context):
		scene = context.scene
		lines = scene.lines

		self.fps, self.dsc_current = calculate(scene)
		self.draw_buttons_area(lines)

###########################################################################################

classes = [ 
	NewLineProp, DSC_TIME_CONVERTER_OT_add_line, DSC_TIME_CONVERTER_OT_clear_lines, DSC_TIME_CONVERTER_OT_delete_line,
	DSC_TIME_CONVERTER_OT_copy_all_markers, DSC_TIME_CONVERTER_OT_copy_current_frame, DSC_TIME_CONVERTER_PT_main, 
	DSC_TIME_CONVERTER_PT_sub_1, DSC_TIME_CONVERTER_PT_sub_2
]

def update_panel(scene, context):
	pass

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	bpy.app.handlers.frame_change_post.append(update_panel)
	bpy.types.Scene.lines = bpy.props.CollectionProperty(type=NewLineProp)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
	
	if update_panel in bpy.app.handlers.frame_change_post:
		bpy.app.handlers.frame_change_post.remove(update_panel)
	del bpy.types.Scene.lines

if __name__ == '__main__':
	register()
