# program to create random counties from a map

import random
import math
import PIL
import Image
import ImageFont, ImageDraw
import os
import pickle
import obot

class Ruler:
	def __init__(self, username):
		self.username = username
		self.holdings = []
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		gold = 0
	def Claim_County(self,id,c_list):
		c = County_From_clist(ID, c_list)
		if c != -1:
			self.holdings.append(c)
			c.Claim_County(self)

class County:
	def __init__(self,id,capitol,color,ruler):
		self.id = id
		self.name = self.id
		self.capitol = capitol
		self.territory = []
		self.territory.append(capitol)
		self.edge_territory = []
		self.edge_territory.append(capitol)
		self.adj_counties = []
		self.color=color
		self.ruler = ruler
		self.motto = ""
		self.productivity = random.randint(0,255)
	#add another square to claimed territory
	def Add_Territory(self, square, counties_map, pixels):
		self.territory.append(square)
		self.edge_territory.append(square)
		counties_map[square[1]][square[0]] = self.id
		pixels[square[0], square[1]] = self.color
	#grow one more square by randomly choosing an adjacent, unoccupied square
	def Grow(self,counties_map,pixels):
		possible = self.Get_Adjacent_Empty(counties_map)
		if(len(possible)>0):
			pick = random.choice(possible)
			self.Add_Territory(pick,counties_map, pixels)
	#get a list of all adjacent squares
	def Get_Adjacent_Empty(self,counties_map):
		possible = []
		adjacent = []
		for square in self.edge_territory:
			if square[0]>0:
				adjacent.append((square[0]-1,square[1]))
			if square[0]<height-1:
				adjacent.append((square[0]+1,square[1]))
			if square[1]>0:
				adjacent.append((square[0],square[1]-1))
			if square[1]<width-1:
				adjacent.append((square[0],square[1]+1))
			edge=0
			for adj in adjacent:
				if counties_map[adj[1]][adj[0]] == 0:
					edge+=1
					possible.append(adj)
				elif counties_map[adj[1]][adj[0]] != self.id:
					if counties_map[adj[1]][adj[0]] not in self.adj_counties:
						self.adj_counties.append(counties_map[adj[1]][adj[0]])
#			if a square on the list is proven to be surrounded by claimed territory, remove it from the list
			if edge==0:
				self.edge_territory.remove(square)
		return possible
#	DO NOT CHECK IF THE SQUARES ON THE INTERIOR CAN EXPAND
#		If they weren't next to an empty square last round, they never will be
#	Keep a list of 'edge' territory (in addition to the total territory list)
#		New territory is automatically added to the list
#		if a square on the list is proven to be surrounded by claimed territory, remove it from the list

	#Find center of territory
	def Get_Center(self):
		x_total=0
		y_total=0
		count = 0
		for item in self.territory:
			x_total+=item[0]
			y_total+=item[1]
			count+=1
		center = (x_total/count,y_total/count)
		if center in self.territory:
			return center
		#if center of territory not in territory (i.e. donut) then find nearest point
		else:
			nearest = (0,0)
			near_dist = 9999
			for square in self.territory:
				dist = math.sqrt((center[1]-square[1])**2+(center[0]-square[0])**2)
				if dist < near_dist:
					nearest = square
					near_dist = dist
			return nearest
			
	def Claim_County(self,ruler):
		self.ruler = ruler
	def Set_Motto(self, motto):
		self.motto = motto

		
#check and see if the map is full
def Map_Full(counties_map):
	for y in range(len(counties_map)):
		for x in range(len(counties_map[y])):
			if counties_map[y][x]==0:
#				print "FOUND 0 AT ", x, " ", y
				return False
	return True
		
#count the number of empty (unclaimed) squares on the map
def Count_Empty(counties_map):
	count=0
	for y in range(len(counties_map)):
		for x in range(len(counties_map[y])):
			if counties_map[y][x]==0:
				count+=1
	return count

#God is the default ruler of all counties
#before anyone claims them
def Create_God():
	return Ruler("God")

#Generates county map from scratch
def Generate_Map(height,width,counties_map,num_counties,c_list):
	#create empty map image
	img = Image.new( 'RGB', (height,width), "white") # create a new white image
	pixels = img.load() # create the pixel map
	
	#create an empty map (i.e. full of value 0)
	for y in range(height):
		holder = []
		for x in range(width):
			holder.append(0)
		counties_map.append(holder)	

	counties=range(1,num_counties)

	#initialize all counties with a starting location and name
	for c in counties:
		x = random.randrange(0,255)
		y = random.randrange(0,255)
		color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
		c_list.append(County(c,(x,y),color,Create_God()))
		counties_map[y][x]=c
		pixels[x, y] = color
		
	#while there still exists empty territory on the map	
	#grow each county	
	counter=0
	while(not(Map_Full(counties_map))):
		for c in c_list:
			c.Grow(counties_map,pixels)
		print Count_Empty(counties_map)
		if counter%10==0:
			print "exported"
			img.save("polimap"+'{0:04d}'.format(counter)+".png")
		counter+=1
	#save final map state	
	img.save("polimap"+'{0:04d}'.format(counter)+".png")
	
	resize_factor = 4
	#resize image to be large enough to write names on it
	img2 = img.resize((resize_factor*width,resize_factor*height))
	draw = ImageDraw.Draw(img2)
	for c in c_list:
		center = c.Get_Center()
		draw.text((center[0]*resize_factor-8,center[1]*resize_factor-3), str(c.name))

	img2.save("polimap_text.png")

#takes in a county ID and returns the county object
def County_From_clist(ID, c_list):
	for c in c_list:
		if ID == c.id:
			return c
	#if not found return -1
	return -1
	
#takes in counties map and returns an img of that map
def Create_County_Image(counties_map):
	h=len(counties_map)
	w=len(counties_map[0])
	img = Image.new( 'RGB', (h,w), "white") # create a new white image
	pixels = img.load() # create the pixel map
	for y in range(len(counties_map)):
		for x in range(len(counties_map[y])):
			c = County_From_clist(counties_map[y][x],c_list)
			pixels[x, y] = c.color
	return img
	
#Generate map of counties, showing their productivity
def Create_County_Productivity_Image(counties_map):
	h=len(counties_map)
	w=len(counties_map[0])
	img = Image.new( 'RGB', (h,w), "white") # create a new white image
	pixels = img.load() # create the pixel map
	for y in range(len(counties_map)):
		for x in range(len(counties_map[y])):
			c = County_From_clist(counties_map[y][x],c_list)
			pixels[x, y] = (c.productivity,c.productivity,c.productivity)
	return img
	
#Generate large map of counties, showing who rules them
def Create_Ruler_Image(counties_map):
	h=len(counties_map)
	w=len(counties_map[0])
	resize_factor = 4
	img = Image.new( 'RGB', (h,w), "white") # create a new white image
	pixels = img.load() # create the pixel map
	for y in range(len(counties_map)):
		for x in range(len(counties_map[y])):
			c = County_From_clist(counties_map[y][x],c_list)
			pixels[x, y] = c.ruler.color
	
	img2 = img.resize((resize_factor*width,resize_factor*height))
	draw = ImageDraw.Draw(img2)
	for c in c_list:
		center = c.Get_Center()
		draw.text((center[0]*resize_factor-(5*len(c.ruler.username)),center[1]*resize_factor-3), str(c.ruler.username))

	return img2
	
	
#characters are 7 high and 5 wide
# so height -3
# width - 5*len(c.ruler.username)/2
	
#saves map in a 
def Save_Map(c_list, counties_map):
	if not os.path.exists("./save"):
		os.makedirs("./save")
	os.chdir("./save")
	data = (c_list, counties_map)
	pickle.dump( data, open( "save.p", "wb" ) )
	os.chdir("..")

def Load_Map():
	if os.path.exists("./save"):
		os.chdir("./save")
		data = pickle.load( open( "save.p", "rb" ) )
		os.chdir("..")
		return data
	else:
		print "No Save File"
		return -1

dim = 256
height = dim
width = dim
counties_map=[]
#create list of county names
num_counties=200
#list of county objects
c_list=[]

'''
data = Load_Map()
c_list=data[0]
counties_map=data[1]
'''
Generate_Map(height,width,counties_map,num_counties,c_list)
Save_Map(c_list, counties_map)

print
print
print Count_Empty(counties_map)
print len(c_list)
img = Create_County_Image(counties_map)
img.save("test.png")
img = Create_County_Productivity_Image(counties_map)
img.save("productivity.png")

img2 = Create_Ruler_Image(counties_map)
img2.save("rulers.png")

#to do:

# reddit api stuff
# be able to interact with users
#	allow for commands to be given
#	imgur api to update map
#	moderator stuff to update map link

#	Ability to declare war and take territory
#	Scheduling things to happen once a day, etc.  

#Look into hosting options

#backburner
# use the productivity map to influence how a county expands?
# somehow stop the "smear race" that happens when a bunch of counties expand in the same direction, forming a bunch of parallel lines