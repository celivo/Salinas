import re
tests = ["I like food", 							#0
"I like all foods", 								#1
"I like food.", 									#2
"I like food very much.", 							#3
"This school has a class about foodways!", 			#4
"We're learning about food systems.", 	   			#5
"Look! In the sky! A food system!",					#6
"There are only two things I like: food and food."] #7

words = ["food", "foods", "food system", "food systems"]
for w in words:
	count = 0
	for test in tests:
		if re.search(w, test):
			print(w + ": " + "match in test " + str(count))
		count += 1

# Basic keyword without variations is good!
