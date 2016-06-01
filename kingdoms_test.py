# kingdoms test 

from opensimplex import OpenSimplex
import Image


class Kingdom:
	def __init__(self, name, ruler, capitol, counties):
		self.name = name
		self.ruler = ruler
		self.capitol = capitol
		self.counties = counties
	def Claim_County(self, county):
		self.counties.append(county)
	
	
	
class County:
	def __init__(self, ruler, x, y, kingdom):
		self.name = str(x) + NumberToLetter(y)
		self.ruler = ruler
		self.location = (x,y)
		self.kingdom = kingdom
	def NameCounty(self, name):
		self.name = name
	def Join_Kingdom(self, kingdom):
		self.kingdom = kingdom
		

def NumberToLetter(number):
	return chr(number+65)



#############################################
#	SIMPLEX BROWNIAN NOISE					#
#	FOR GENERATING LAND PRODUCTIVITY MAP	#
#############################################

# for further reading/reference:
# http://www.redblobgames.com/maps/terrain-from-noise/
# https://cmaher.github.io/posts/working-with-simplex-noise/

#specify dimensions of map
dim = 256
height = dim
width = dim
map=[]

#create an empty map (i.e. full of value 0)
for y in range(height):
	holder = []
	for x in range(width):
		holder.append(0)
	map.append(holder)

#returns simplex noise
def snoise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    #print nx, ny
    return gen.noise2d(nx, ny) / 2.0 + 0.5
	
#creates summed simplex noise
def sumOctave(num_iterations, x, y, persistence, scale, low, high):
    maxAmp = 0
    amp = 1
    freq = scale
    noise = 0
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
    noise = noise * (high - low) / 2 + (high + low) / 2
    return noise

#create image to output map in
img = Image.new( 'RGB', (height,width), "black") # create a new black image
pixels = img.load() # create the pixel map

gen = OpenSimplex()


scale = .03	 #make larger for finer granularity
	
for y in range(height):
    for x in range(width):
        n_val = sumOctave(16, x, y, .5, scale, 0, 255)
        map[y][x] = n_val
        noise_int = int(n_val)
        pixels[x, y] = (noise_int,noise_int,noise_int)

img.save("noisemap.bmp")

#map will have a value between 0 and 255 for the productivity
