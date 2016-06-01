# reddit bot
# to handle requests



import obot
import string
import counties_maker_2
import time

#process

def Process_Comments(r):
	input = list(r.get_comments('thefifthhorse',limit=50))
	for i in input:
		if '!thefifthhorse' in string.lower(i.body):
			replied = 0
			j = r.get_submission(i.permalink).comments[0]
			for reply in j.replies:
				if string.lower(reply.author.name) == 'thefifthhorse':
					replied = 1
			if not(replied):
				print "	Parsing request from ", i.author.name
				Parse_Command(i)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
			
def Parse_Command(comment):
	text = string.split(comment.body)
	m = text.index('!thefifthhorse')
	if len(text) >= m+1:
		if string.lower(text[m+1])=='join':
			print "		JOIN"
			if counties_maker_2.Ruler_From_rlist(comment.author.name, r_list) == -1:
				r_list.append(counties_maker_2.Create_Ruler(comment.author.name))
				comment.reply("Success!  You are now registered!  Please check [this page](https://www.reddit.com/r/TheFifthHorse/wiki/players) to see your standing!")
			else:
				comment.reply("You are already registered!")
		elif len(text) >= m+2:
			if string.lower(text[m+1])=='claim':
				claim_id = text[m+2]				
				print "		CLAIM ", claim_id
				k = Submit_Claim(comment.author.name, claim_id)
				comment.reply(k)
			elif len(text) >= m+3:	
				if string.lower(text[m+1])=='sell':
					if RepresentsInt(text[m+3]):
						claim_id = text[m+2]
						sell_price = int(text[m+3])						
						print "		SELL ", claim_id, " FOR ", sell_price
						k = Sell_County(comment.author.name, claim_id, sell_price)
						comment.reply(k)
					else:
						comment.reply("Error: not an int")
				else:
					comment.reply("Error: unrecognized command")
			else:
				comment.reply("Error: unrecognized command")
		else:
			comment.reply("Error: unrecognized command")
	else:
		comment.reply("Error: unrecognized command")

		
		# VVV this has been superseded, expect problems
def New_Ruler(user):
	ruler = Ruler(user)
	ruler.gold = 100
	r_list.append(ruler)

def Payday(r_list):	
	for ruler in r_list:
		ruler.Revenue_From_Holdings()
		ruler.gold += 10
		print "		PAYING ", ruler.username
	
def Submit_Claim(user, id):
	if RepresentsInt(id):
		id_int = int(id)
		c = counties_maker_2.County_From_clist(id_int, c_list)
		ruler = counties_maker_2.Ruler_From_rlist(user, r_list)		
		#if county exists and ruler exists
		if c != -1:
			if ruler != -1:
				#if ruler has no counties or county is adjacent to existing county
				adj = 0
				for county in ruler.holdings:
					for a in county.adj_counties:
						if a == id_int:
							adj = 1
				if len(ruler.holdings)==0 or adj:
					#check if forsale
					if c.forsale:
						#check if enough money
						if ruler.gold > c.price:
							ruler.Claim_County(int(id_int),c_list)
							return "Success: you are now the proud owner of county"+str(id_int)+ "!"
						else:
							return "Error: not enough gold for purchase"
					else:
						return "Error: county not for sale"
				elif not(adj):
					return "Error: claimed county must be adjacent to one of your existing counties!"
				
			else:
				return "Error: no ruler "+ user+ ", please JOIN to be able to claim counties."
		else:
			return "Error: no claim "+ str(id_int)
	else:
		return "Error: claim not a number"

def Sell_County(user,id,price):	
	if RepresentsInt(id) and RepresentsInt(price):
		id_int = int(id)
		c = counties_maker_2.County_From_clist(id_int, c_list)
		ruler = counties_maker_2.Ruler_From_rlist(user, r_list)
		#if county exists and ruler exists
		if c != -1:
			if ruler != -1:
				#if ruler owns county 
				if ruler == c.ruler:
					c.Put_Up_For_Sale(int(price))
					return "Success: you have put up property "+id+" for sale for "+str(price)
				else:
					return "Error: you do not own this property!"
			else:
				return "Error: no ruler "+ user+ ", please JOIN to be able to sell counties."
		else:
			return "Error: no claim "+ str(id_int)
	else:
		return "Error: not integer"
		
def Update_Ruler_List(r_list):
	content = "Name | No. Holdings | Gold | Income Rate\n"
	content+="---|---|----|----\n"
	for ruler in r_list:
		line =ruler.username + " | " 
		line += str(len(ruler.holdings)) + " | "
		line += str(ruler.gold) + " | "
		income = 0
		for h in ruler.holdings:
			income+=h.productivity*ruler.stewardship
		line += str(income) + "\n"
		content += line
		
	r.edit_wiki_page('thefifthhorse', 'players', content, reason=u'Updating Ruler List')

		
def Update_Polimap():
	r.delete_image('thefifthhorse','polimap')
	r.upload_image('thefifthhorse','polimap_text.png','polimap')
	
def Update_Rulermap():
	r.delete_image('thefifthhorse','rulers')
	r.upload_image('thefifthhorse','rulers.png','polimap')
	
def Update_Image(file, imagename):
	r.delete_image('thefifthhorse',imagename)
	r.upload_image('thefifthhorse',file,imagename)
	

#use this bit to generate a new map
#CAREFUL THIS WILL OVERWRITE THE OLD MAP AND GAME STATE INFORMATION
'''
dim = 256
height = dim
width = dim
counties_map=[]
#create list of county names
num_counties=200
#list of county objects
c_list=[]
r_list=[]

counties_maker_2.Generate_Map(height,width,counties_map,num_counties,c_list)
counties_maker_2.Save_Map(c_list, counties_map, r_list)
'''

	
	
r = obot.login()
	
print
print	
	
#loads in save file
data = counties_maker_2.Load_Map()
c_list=data[0]
counties_map=data[1]
r_list = data[2]

print

#The main loop 
while 1:
	print "processing"
	#Take commands
	print " beginning comment processing:"
	Process_Comments(r)
	print " comments processed"
	#create updated maps
	img = counties_maker_2.Create_Ruler_Image(counties_map,c_list)
	img.save("rulers.png")
	img = counties_maker_2.Create_County_Price_Image(counties_map,c_list)
	img.save("price.png")
	print " maps updated"
	#Update things
	Update_Image('rulers.png','rulers')
	Update_Image('price.png','price')
	Update_Image('polimap_text.png','polimap')
	print " maps uploaded"
	#pay rulers
	Payday(r_list)
	print " rulers paid"
	#Save Game State	
	Update_Ruler_List(r_list)
	counties_maker_2.Save_Map(c_list, counties_map, r_list)
	print " game saved"
	#sleep for x seconds
	print "__"
	time.sleep(30)


#to do:

# write a purge command which removes a ruler from r_list