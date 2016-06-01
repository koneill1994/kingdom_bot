# kingdoms test 

from opensimplex import OpenSimplex
import Image
import random


# biomes
#	water
#		e>sea level
#		produces fish resource based on distance to coast?
#	shore
#		e > sea level + a bit
#		produces clay?
#	forest
#		wet
#		produces wood
#	grassland
#		drier
#		Allows for farming, produces food
#	desert
#		driest
#		nuthin?

class Ocean:
	def __init__(self)
		self.name = "Ocean"
		#produces fish resource based on distance to coast?


class Tile:
	def __init__(self, x, y, seed):
		self.x = x
		self.y = y
		self.elevation = sumOctave(16, x, y, .5, 0.3, 0, 255, seed)
		self.moisture = sumOctave(16, x, y, .5, 0.3, 0, 255, seed+12345)
		
		
		
		
'''
	def Get_Biome(self):
		e = self.elevation
		m = self.moisture
		# normalize such that little is within .35 of the bounds
		if e<.4:
			#return "ocean"
			return (0,255,0)
		if e<.41:
			#return "beach"
			1
	
		if e>.9:
			if m < .1:
				return "scorched"
			if m < .2:
				return "bare"
			if m < .5:
				return "tundra"
			return snow
	
		if e > .8:
			if m < .33:
				return "temperate desert"
			if m < .66:
				return "shrubland"
	
		if e > .6:
			if m < .16:
				return "temperate desert"
			if m < 0.5:
				return "grassland"
			if m < .83:
				return "temperate deciduous forest"
			return "temperate_rain_forest"
		
		if m<.16:
			return "subtropical desert"
		if m<.33:
			return "grassland"
		if m<.66:
			return "tropical seasonal forest"
		return "tropical rain forest"
'''

#############################################
#	SIMPLEX BROWNIAN NOISE					#
#	FOR GENERATING LAND PRODUCTIVITY MAP	#
#############################################

# for further reading/reference:
# http://www.redblobgames.com/maps/terrain-from-noise/
# https://cmaher.github.io/posts/working-with-simplex-noise/

#returns simplex noise
def snoise(nx, ny):
	# Rescale from -1.0:+1.0 to 0.0:1.0
	#print nx, ny
	return gen.noise2d(nx, ny) / 2.0 + 0.5
	
#creates summed simplex noise
def sumOctave(num_iterations, x, y, persistence, scale, low, high, seed):
	maxAmp = 0
	amp = 1
	freq = scale
	noise = 0
	x+=width*seed
	#add successively smaller, higher-frequency terms
	i = 0
	while i < num_iterations:
		noise += snoise(x * freq, y * freq) * amp
		maxAmp += amp
		amp *= persistence
		freq *= 2
		i+=1
	#take the average value of the iterations
	noise /= maxAmp
	#normalize the result
	#noise = noise * (high - low) / 2 + (high + low) / 2
	return noise*255

def Octaves_New(x,y,height,width,scale,seed):
	x+=width*seed
	x=x*scale
	y=y*scale
	#x = x/width - 0.5
	#y = y/height -0.5
	#print "nx ", x
	#print "ny ", y
	output = 1 * snoise(1 * x, 1 * y)
	output+= 0.5 * snoise(2 * x, 2 * y)
	output+= 0.25 * snoise(4 * x, 4 * y)
	output = output/1.75
	output = output+1 /2
	return output
	
# given height, returns a color indicating the biome
def elevation_to_biome_color(height,sea_level):
	mountain_start = .8
	if height < sea_level:
		color = (0,0,255)
	elif height >= sea_level and height < mountain_start:
		color = (0,int(255*height),0)
	else:
		n = int(height*255)
		color = (n,n,n)
	#print height
	return color

def color_test(height):
	bounds = .4
	j = int(255*height)
	if height < bounds:
		return (j,0,0)
	elif height > 1.-bounds:
		return (0,j,0)
	return (j,j,j)
	
def Create_Elevation_Map(height, width, map, sea_level,seed):
	img = Image.new( 'RGB', (height,width), "black") # create a new black image
	pixels = img.load() # create the pixel map
	scale = .03	 #make larger for finer granularity
	for y in range(height):
		for x in range(width):
			#n_val = sumOctave(16, x, y, .5, scale, 0, 255,seed)
			n_val = Octaves_New(x,y,height,width,scale,seed)
			height_color = n_val * 255
			map[y][x] = n_val
			noise_int = int(height_color)
			#pixels[x, y] = (noise_int,noise_int,noise_int)
			#pixels[x, y] = elevation_to_biome_color(n_val,sea_level)
			pixels[x, y] = color_test(n_val)
	img.save("noisemap.bmp")
	return map

def Create_Blank_Map(dim):
	height = dim
	width = dim
	map=[]
	for y in range(height):
		holder = []
		for x in range(width):
			holder.append(0)
		map.append(holder)
	return map
	
	
#specify dimensions of map
gen = OpenSimplex()
dim = 256
height = dim
width = dim
map=Create_Blank_Map(dim)

seed = random.randrange(100)

#create an empty map (i.e. full of value 0)

sea_level = .2


		
		
Create_Elevation_Map(height, width, map, sea_level,seed+12345)


#map will have a value between 0 and 255 for the productivity
'''

voronoi = []

for y in range(height):
	holder = []
	for x in range(width):
		holder.append(0)
	voronoi.append(holder)

points = []
	

t = 0
while t<200:
	x = random.randrange(0,255)
	y = random.randrange(0,255)
	while(map[y][x] < sea_level):
		x = random.randrange(0,255)
		y = random.randrange(0,255)
	points.append((x,y))
	
#generate voronoi
#for y in voronoi:
#	for x in voronoi[y]:
#		nearest = 
'''
	
#do this with counties so you can keep track of the stuff
	
# to do
# do the "random 200 points" as in the other code
# 	if any are under water, reroll

# generate a voronoi diagram
# move each point to the centroid of its cell

# grow from there



