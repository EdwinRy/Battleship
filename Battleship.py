##Game graphics
from tkinter import *

##Screen properties
screenWidth, screenHeight = 500, 500

##Mathematical structures
##Vector consisting of 2 values
class vec2():
	def __init__(self,x,y):
		self.x = x
		self.y = y;

##Vector consisting of 3 values
class vec3():
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

##Return minimal value of 3 parameters
def min3(x,y,z):
	minimum = x
	if(y<minimum):
		minimum = y
	if(z<minimum):
		minimum = z
	return minimum

##Return maximal value of 3 parameters
def max3(x,y,z):
	maximum = x
	if(y>maximum):
		maximum = y
	if(z>maximum):
		maximum = z
	return maximum

##Models
##Model loader
def loadOBJModel(path,texture):
	m = Model()
	m.texture = PhotoImage(file=path)

	pass
##3d renderable model in the scene
class Model():
	##Object constructor
	def __init__(self):
		self.vertices = []
		self.indices = []
		self.textureCoords = []
		self.texture = None

	##Load screen coordinates of triangles
	def loadCoords(self,coords):
		self.vertices = coords
	
	##Load indices for the model
	def loadIndices(self,indices):
		self.indices = indices

##Flag attached to the cruise
class Flag():
	def __init__(self,position,model):
		self.position = position

##Ship along with the model
class Ship():
	def __init__(self,position,model):
		self.position = position


##Rasterizer
##convert to screen space
def convertCoord(coord):
	coord.x = (0.5 * screenWidth) - (-coord.x * 0.5 * screenWidth)
	coord.y = (0.5 * screenHeight) - (coord.y * 0.5 * screenHeight)
	return coord

class Renderer():
	##Rasterizer constructor
	def __init__(self):
		self.models = []
	
	def setPixel(self,x,y,r,g,b)
	{
		self.img.put("#%02x%02x%02x" % (r,g,b),(x,y))
	}

	##Rasterize a single triangle
	def drawTriangle(self,v0,v1,v2):

		##Calculate bounding rectange
		minx = int(min3(v0.x,v1.x,v2.x))
		maxx = int(max3(v0.x,v1.x,v2.x))
		miny = int(min3(v0.y,v1.y,v2.y))
		maxy = int(max3(v0.y,v1.y,v2.y))

		##Assign X constants
		c1x = v1.x - v0.x
		c2x = v2.x - v1.x
		c3x = v0.x - v2.x

		##Assign Y constants
		c1y = v1.y - v0.y
		c2y = v2.y - v1.y
		c3y = v0.y - v2.y

		##Prepare the space in memory to be used
		cy1 = 0
		cy2 = 0
		cy3 = 0

		cx1 = 0
		cx2 = 0
		cx3 = 0

		##Prepare the space in memory for baryocentric coordinates
		##used to compute the z buffer
		zArea = ((v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x))
		z0 = 0
		z1 = 0
		z2 = 0

		##Iterate through the bounding rectangle
		for y in range(miny,maxy):
			cy1 = c1x * (y - v0.y)
			cy2 = c2x * (y - v1.y)
			cy3 = c3x * (y - v2.y)

			for x in range(minx,maxx):
				cx1 = c1y * (x - v0.x)
				cx2 = c2y * (x - v1.x)
				cx3 = c3y * (x - v2.x)

			
				##Check whether the point is within the triangle
				if((cy1 <= cx1)and(cy2 <= cx2)and(cy3 <= cx3)):
					##Calculate baryocentric coordinates
					cx1 /= -zArea
					cx2 /= -zArea
					cx3 /= -zArea

					##Calculate the Z buffer
					z = 1 / ((cx1 * v0.z) + (cx2 * v1.z) + (cx3 * v2.z))

					##colour in a pixel
					self.setPixel(x,y,255,255,255)


	##Add a model to the renderer list
	def loadModel(self,model):
		self.models.append(model)
	
	##Set current rendering buffer
	def setBuffer(self,img):
		self.img = img

	##Add multiple models at once
	def loadModels(self,models):
		for i in range(0,len(models)):
			self.models.append(models[i])

	##Render the model using its indices
	def renderIndices(self,model):
		i = 0
		while i < len(model.indices):
			self.drawTriangle(model.vertices[model.indices[i]],model.vertices[model.indices[i+1]],model.vertices[model.indices[i+2]])
			i += 3
		pass

	##Render the model using bare triangles
	##(the coordinates have to be in order)
	def renderVectors(self,model):
		i = 0
		while i < len(model.vertices): 
			self.drawTriangle(self.img,model.vertices[i],model.vertices[i+1],model.vertices[i+2])
			i += 3

	def renderModels(self):
		pass


##Actual Game
import time
##Enemy logic 
##(because you're SURELY going to play with friends)
class Enemy():
	def __init__(self):
		pass

##Player logic
class Player():
	def __init__(self):
		pass


class Game():
	##Call at startup
	def __init__(self,main):
		
		##Create canvas
		self.canvas = Canvas(main, width=screenWidth, height=screenHeight, bg="#000000")		
		self.canvas.pack()
		self.main = main

		##Set up buffers
		self.buffers = []
		self.currentBuffer = 0
		self.buffers.append(PhotoImage(width=screenWidth, height=screenHeight))
		self.buffers.append(PhotoImage(width=screenWidth, height=screenHeight))
		self.currentBuffer = self.canvas.create_image(0,0,anchor=NW,image=self.buffers[self.currentBuffer])

		self.renderer = Renderer()

		##TESTING
		v0 = vec3(-0.5,0.5,0)
		v1 = vec3(-0.5,-0.5,0)
		v2 = vec3(0.5,-0.5,0)
		v3 = vec3(0.5,0.5,0)
		v0 = convertCoord(v0)
		v1 = convertCoord(v1)
		v2 = convertCoord(v2)
		v3 = convertCoord(v3)

		self.verts = [v0,v1,v2,v3]
		self.indices = [0,1,2,0,2,3]
		self.m = Model()
		self.m.loadCoords(self.verts)
		self.m.loadIndices(self.indices)
		##todo:add textures
		##/TESTING

		##start the main loop
		self.onUpdate()

	##Call every frame
	def onUpdate(self):

		start = time.time()
		##render image
		self.onRender()
		##change buffers
		self.canvas.itemconfig(self.currentBuffer, image = self.buffers[self.currentBuffer])
		if self.currentBuffer == 0:
			self.curentBuffer = 1;

		else:
			self.currentBuffer = 0;

		print(time.time()-start)
		self.main.after(1,self.onUpdate)
	def onRender(self):
		self.renderer.setBuffer(self.buffers[self.currentBuffer])
		self.renderer.renderIndices(self.m)
		pass

root = Tk()
Game(root)
root.mainloop()
