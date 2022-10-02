"""
#######################################
Desktop Fountain Base Generator
#######################################

Copyright (c) 2022: Theodor B.

This program is free software: you can redistribute it and/or modify
it under the terms of the Creative Commons (4.0 International License).
Following terms apply: Attribution: You must give appropriate credit,
provide a link to the license, and indicate if changes were made.
You may do so in any reasonable manner, but not in any way that
suggests the licensor endorses you or your use.
"""

import math
import Part

#some arrangements with cheesy names
original = [[1,1],[1,1,1],[1,1]]
original_hole = [[1,1],[1,0,1],[1,1]]
butterfly = [[0,1,1],[1,1,1],[0,1,1]]
ant = [[0,1,0],[1,0,1],[1,1],[0,0,1,1],[0,1,0,1],[0,0,1]]
turtle = [[1,0,1],[0,1,1,0],[1,0,1]]
line2 = [[1],[0,1]]
line3 = [[1],[0,1],[0,1]]
line4 = [[1],[0,1],[0,1], [0,0,1]]
arrow = [[1,0,0,1],[0,1,0,1],[0,1,1], [0,0,1]]
triangle_hole = [[1,1,1,1],[0,1,0,1],[0,1,1], [0,0,1]]
triangle = [[1,1,1,1],[0,1,1,1],[0,1,1], [0,0,1]]
#already existing remixes
mediumbase = [[1,1,1],[0,1,1]]
large_rectengular = [[1,1,1],[1,1,1,1],[1,1,1]]
large_triangle = [[1,1,1,1],[0,1,1,1],[0,1,1],[0,0,1]]
extra_large = [[1,1,1],[1,1,1,1],[1,1,1],[0,1,1]]


######################################################################
#parameters
######################################################################
##########################
#array which defines the final shape of the object
#	1	--> create hexagon in this position
#	0	--> no hexagon in this position --> use this to define a empty space
#use presets (line4) or specify your own arrangement
arrange = extra_large

##########################
#parameters of hexagon
r_i = 66.4/2 #disance from origin to one edge
			 #default: 66.4/2
r_u = (2*r_i)/math.sqrt(3)	#distance from origin to one corner
height = 41	#height of the base without rim
			#default original: 31
			#default fairy tale fountain: 31
			#default deep base: 41

##########################
#parameters of cutout from hexagon
w_thick = 2.4 	#wall thickness !!! Don't change if you want to use original baseplates!!!
#				#default: 2.4
#Attention: don't change w_thick if you want to use the original baseplates
b_thick = 1 #bottom thickness
			#default: 1

##########################
#parameters of cutout for baseplates
cutout_bp_w = 8/2 	#width/2 of cutout to hold baseplates
					#default: 8/2

distance_cutOutBottom_baseTop = 11	#distance between the bottom of the cutout to the top of the base
									#default: 11
cutout_bp_h = height-distance_cutOutBottom_baseTop #position of cutout in z-direction
cutout_bp_d = 1.2 	#depth of cutout
					#default: 1.2

##########################
#parameters of cutout for water channels
cutout_wc_w = 8/2	#width/2 of cutout
					#default:8/2
distance_wcTop_baseTop = 3 	#distance between top of waterchannel and top of base
							#default: 3
cutout_wc_h = height - distance_wcTop_baseTop 	#height of cutout

##########################
#parameters of rim
height_rim = 28 #default original:22
				#default fairy tale fountain and deep base: 28
overlap_rim = 13 #overlap between rim an base
				#default: 13
rim_thick = 2.4 #default: 2.4
######################################################################
#end of parameters
######################################################################

#delete current objects (uncomment for debugging)
for obj in FreeCAD.ActiveDocument.Objects:
		FreeCAD.ActiveDocument.removeObject(obj.Name)

#pad arrange array with zeros
#in every array a '0' has to be placed as first element if not, the cutouts won't work properly
for line in arrange:
	line.insert(0, 0)
	line.insert(len(line), 0)
arrange.insert(0,[0])
arrange.insert(len(arrange),[0])

####################
#calculate offsets in order to fit the individual hexagons together
##offset in x-direction (gets applied every single time)
dx = 2*r_u \
	-(r_i - w_thick/2)*math.tan(30*math.pi/180) \
	- w_thick/math.cos(30*math.pi/180)
#offset for every second line of hexagons
d_y = r_u * math.sin(60 * math.pi/180) - w_thick/2

#########################################
#Functions
#########################################
def getIndexOffset(n_angle, i):
	i_x = 0
	j_x = 0

	if i%2 != 0:
		if n_angle == 0:
			j_x = 1
		elif n_angle == 1:
			i_x = 1
			j_x = 1
		elif n_angle == 2:
			i_x = 1
		elif n_angle == 3:
			j_x = -1
		elif n_angle == 4:
			i_x = -1
		elif n_angle == 5:
			i_x = -1
			j_x = 1
	else:
		if n_angle == 0:
			j_x = 1
		elif n_angle == 1:
			i_x = 1
		elif n_angle == 2:
			i_x = 1
			j_x = -1
		elif n_angle == 3:
			j_x = -1
		elif n_angle == 4:
			i_x = -1
			j_x = -1
		elif n_angle == 5:
			i_x = -1


	return i_x, j_x

#############################
#Functions to create shapes
def create_hexagon_shape(r_i, height, pos):
	points = []
	lines = []
	edges = []
	r_u = (2*r_i)/math.sqrt(3)

	#compute the points of hexagon
	for i in range(0,6):
		x_cord = r_u * math.cos(i*60*math.pi/180)
		y_cord = r_u * math.sin(i*60*math.pi/180)
		points.append(FreeCAD.Vector(x_cord, y_cord,0))
	#connect first and last point to line
	lines.append(Part.LineSegment(points[-1], points[0]))
	#connect points to lines
	for i in range(0,len(points)-1):
		lines.append(Part.LineSegment(points[i], points[i+1]))
	#convert lines to edges
	for line in lines:
		edges.append(line.toShape())
	#Create Wire
	wire = Part.Wire(edges)
	#Create Face
	face = Part.Face(wire)
	#Change Placement of face
	face.Placement.Base = FreeCAD.Vector(pos)
	#extrude face
	hexagon_shape = face.extrude(FreeCAD.Vector(0,0,height))
	return hexagon_shape #this is not yet an object which is visible in FreeCAD

def create_cutout_bp_shape():
	points = []
	lines = []
	edges = []

	points.append(FreeCAD.Vector(-cutout_bp_w, 0, 0))
	points.append(FreeCAD.Vector(cutout_bp_w, 0, 0))
	points.append(FreeCAD.Vector(cutout_bp_w, 0, 2*cutout_bp_w))
	points.append(FreeCAD.Vector(-cutout_bp_w, 0, 2*cutout_bp_w))
	#connect points to lines
	for i in range(0,len(points)-1):
		lines.append(Part.LineSegment(points[i], points[i+1]))
	#connect first and last point to line
	lines.append(Part.LineSegment(points[-1], points[0]))

	#convert lines to edges
	for line in lines:
		edges.append(line.toShape())
	#Create Wire
	wire = Part.Wire(edges)

	#Create Face
	face = Part.Face(wire)

	#Change Placement of face
	face.Placement.Base = FreeCAD.Vector((0,0,cutout_bp_h))

	#extrude face
	cut_out_shape = face.extrude(FreeCAD.Vector(0,cutout_bp_d,0))

	return cut_out_shape

def create_cutout_wc_shape():
	points = []
	lines = []
	edges = []

	#compute the points for basic shell
	points.append(FreeCAD.Vector(-cutout_wc_w, 0, 0))
	points.append(FreeCAD.Vector(cutout_wc_w, 0, 0))
	points.append(FreeCAD.Vector(cutout_wc_w, 0, cutout_wc_h))
	points.append(FreeCAD.Vector(-cutout_wc_w, 0, cutout_wc_h))
	#connect points to lines
	for i in range(0,len(points)-1):
		lines.append(Part.LineSegment(points[i], points[i+1]))
	#connect first and last point to line
	lines.append(Part.LineSegment(points[-1], points[0]))
	#convert lines to edges
	for line in lines:
		edges.append(line.toShape())
	#Create Wire
	wire = Part.Wire(edges)
	#Create Face
	face = Part.Face(wire)
	#Change Placement of face
	face.Placement.Base = FreeCAD.Vector((0,0,b_thick))
	#extrude face
	cut_out_shape = face.extrude(FreeCAD.Vector(0, w_thick, 0))
	return cut_out_shape

#############################
#Functions to create objects
def create_cut_single_hexagon(i):
	####################
	#create the hexagon to be cut
	baseObj = FreeCAD.ActiveDocument.addObject("Part::Feature","Base" + str(i))
	baseObj.Shape = create_hexagon_shape(r_i, height, (0,0,0))
	####################
	#create the hexagon to cut with
	cutObj = FreeCAD.ActiveDocument.addObject("Part::Feature","Cut" + str(i))
	cutObj.Shape = create_hexagon_shape(r_i-w_thick, height, (0,0,b_thick))
	####################
	#create the cutted hexagon
	cuttedObj = FreeCAD.ActiveDocument.addObject("Part::Cut","Cutted" + str(i))
	cuttedObj.Base = baseObj
	cuttedObj.Tool = cutObj
	return cuttedObj

def create_full_single_hexagon(i, r_i_full, height):
	####################
	#create the hexagon
	baseObj = FreeCAD.ActiveDocument.addObject("Part::Feature","Base" + str(i))
	baseObj.Shape = create_hexagon_shape(r_i_full, height, (0,0,0))

	return baseObj

def create_hexagon_array():
	arr = []
	arr_idx = 0
	for i, line in enumerate(arrange):
		for j, create_obj in enumerate(line):
			if create_obj == True:
				arr.append(create_cut_single_hexagon(arr_idx))
				#calculate x- and y-position
				x = dx * i
				if i % 2 == 0:
					y = (2*r_i - w_thick) * j
				else:
					y = (2*r_i - w_thick) * j + d_y
				#change x- and y- position
				arr[arr_idx].Placement.Base = FreeCAD.Vector(x, y, 0)
				arr_idx += 1

	#fuse single elements of array together
	fusion = FreeCAD.ActiveDocument.addObject("Part::MultiFuse","Fusion_of_Base")
	fusion.Shapes = arr
	return fusion

def create_hexagon_array_full(r_i_full, height_full):
	arr = []
	arr_idx = 0
	for i, line in enumerate(arrange):
		for j, create_obj in enumerate(line):
			if create_obj == True:
				arr.append(create_full_single_hexagon(arr_idx, r_i_full, height_full))
				#calculate x- and y-position
				x = dx * i
				if i % 2 == 0:
					y = (2*r_i - w_thick) * j
				else:
					y = (2*r_i - w_thick) * j + d_y
				#change x- and y- position
				arr[arr_idx].Placement.Base = FreeCAD.Vector(x, y, 0)
				arr_idx += 1

	#fuse single elements of array together
	fusion = FreeCAD.ActiveDocument.addObject("Part::MultiFuse","Fusion_of_Base")
	fusion.Shapes = arr
	return fusion

def create_cutouts_bp():
	cutout_shape = create_cutout_bp_shape()

	arr = []
	arr_idx = 0
	for i, line in enumerate(arrange):
		for j, create_obj in enumerate(line):
			if create_obj == True:
				#calculate center x- and y-position of individual hexagon
				x = dx * i
				if i % 2 == 0:
					y = (2*r_i - w_thick) * j
				else:
					y = (2*r_i - w_thick) * j + d_y
				#place cutouts in 60° steps around the center of the individual hexagon
				for n_angle in range(0,6):
					#create new cutout
					arr.append(FreeCAD.ActiveDocument.addObject("Part::Feature","Cutout" + str(arr_idx)))
					arr[arr_idx].Shape = cutout_shape
					#calculate absolute x- and y-position
					x_cord = x + (r_i - w_thick) * math.sin(n_angle*60*math.pi/180)
					y_cord = y + (r_i - w_thick) * math.cos(n_angle*60*math.pi/180)
					#change position and rotation of cutout
					arr[arr_idx].Placement.Base = FreeCAD.Vector(x_cord, y_cord, 0)
					arr[arr_idx].Placement.Rotation.Axis = FreeCAD.Vector(0,0,1)
					arr[arr_idx].Placement.Rotation.Angle = n_angle * (-60 * math.pi/180)

					arr_idx += 1
	##fuse single elements of array together
	fusion_cutouts = fusion_cut = FreeCAD.ActiveDocument.addObject("Part::MultiFuse","Fusion_of_Cutouts")
	fusion_cut.Shapes = arr
	return fusion_cutouts

def create_cutouts_wc():
	cutout_shape = create_cutout_wc_shape()

	arr = []
	arr_idx = 0
	for i, line in enumerate(arrange):
		for j, create_obj in enumerate(line):
			if create_obj == True:
				#calculate center x- and y-position of individual hexagon
				x = dx * i
				if i % 2 == 0:
					y = (2*r_i - w_thick) * j
				else:
					y = (2*r_i - w_thick) * j + d_y
				#place cutouts in 60° steps around the center of the individual hexagon
				for n_angle in range(0,6):
					i_x, j_x = getIndexOffset(n_angle, i)
					try:
						#look if a cutout is needed
						if arrange[i+i_x][j+j_x] == 1:
							#create new cutout
							arr.append(FreeCAD.ActiveDocument.addObject("Part::Feature","Cutout" + str(arr_idx)))
							arr[arr_idx].Shape = cutout_shape
							#calculate absolute x- and y-position
							x_cord = x + (r_i - w_thick) * math.sin(n_angle*60*math.pi/180)
							y_cord = y + (r_i - w_thick) * math.cos(n_angle*60*math.pi/180)
							#change position and rotation of cutout
							arr[arr_idx].Placement.Base = FreeCAD.Vector(x_cord, y_cord, 0)
							arr[arr_idx].Placement.Rotation.Axis = FreeCAD.Vector(0,0,1)
							arr[arr_idx].Placement.Rotation.Angle = n_angle * (-60 * math.pi/180)
							arr_idx += 1
					except Exception as e:
						pass
	##fuse single elements of array together
	fusion_cutouts = fusion_cut = FreeCAD.ActiveDocument.addObject("Part::MultiFuse","Fusion_of_Cutouts")
	fusion_cut.Shapes = arr
	return fusion_cutouts


#########################################
#Function calls
#########################################
############################
#create base with cutouts
base_with_bp_cutouts = FreeCAD.ActiveDocument.addObject("Part::Cut","Base_with_BP_Cutouts")
base_with_bp_cutouts.Base = create_hexagon_array()
cut_tool = FreeCAD.ActiveDocument.addObject("Part::MultiFuse","Cuttool")
cut_tool.Shapes = [create_cutouts_wc(), create_cutouts_bp()]
base_with_bp_cutouts.Tool = cut_tool
############################

############################
#create rim
base_full1 = create_hexagon_array_full(r_i, height_rim)
base_full2 = create_hexagon_array_full(r_i+rim_thick, height_rim)
rim = FreeCAD.ActiveDocument.addObject("Part::Cut","Rim")
rim.Base = base_full2
rim.Tool = base_full1
rim.Placement.Base = FreeCAD.Vector(0,0,height-overlap_rim)
############################

############################
#Fuse rim and base together
final_base = FreeCAD.ActiveDocument.addObject("Part::Fuse","FinalBase")
final_base.Base = base_with_bp_cutouts
final_base.Tool = rim
final_base.Visibility = False

############################
#Refine the fusion (without this, chamfer operations are almost impossible)
final_base_refined = FreeCAD.ActiveDocument.addObject('Part::Refine','FinalBase_Refined')
final_base_refined.Source = final_base

FreeCAD.ActiveDocument.recompute()
#Finished --> now manualy add a chamfer to the edges in the GUI of FreeCAD (Sorry, I have no idea how to implement this :D)
############################
