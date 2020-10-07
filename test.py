# a={'a','c','f','z'}
# b={'a','c','3','ds','2','w'}
# print(list(b-a))

# a=['d','s','d','w','f','c','g','r','e','t','u']
# b=[x+'1' for x in a if [1,x+'a'] ]
# print(b) 

d={"VillageLocation":(1,1)}
player1_location=(1,1)
player2_location=(2,2)
#check by values
reachedVillage = player1_location in d.values() #returns True #method for checking by values
if (reachedVillage == True):
    goToSleep("player1")