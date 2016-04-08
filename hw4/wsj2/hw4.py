import nltk, time, numpy


def main():
	
	input_file = input("Enter path of file to score (in 'quotes'): ")
	scorer(input_file)
	print('done')


def scorer(toTag):
	input_file = open('./WSJ_02-21.pos', 'r')
	output = open('./output_count.txt', 'w')

	# Start timer
	t = time.time()

	print "This program runs slowly with large files! Please be patient..."
	input_length = sum(1 for line in input_file if line.strip())


	# LIKELIHOOD

	rows = input_length
	columns = 3 

	# Initialize table as 0
	table = [[0 for x in range(columns)] for x in range(rows)] 
	table2 = [[0 for x in range(columns)] for x in range(rows)] 

	lastElem = 0

	for line in input_file:
		# Skip blank lines
		if not line.strip():
			continue 

		# If not blank
		s = line.split()
		token = s[0]
		pos = s[1]

		index = 0
		execute = False

		for i in range(rows): 
			# First, add all to the HMM table
			table2[i][0] = token
			table2[i][1] = pos
			#for j in range(columns):
			# If found in table, increment count and break out of loop
			if (table[i][0] == token and table[i][1] == pos):
				table[i][2] = table[i][2] + 1 # add to count
				break
			elif (table[i][0] == 0):
				index = i
				execute = True
				break
		
		# If not found in table, set next index to token
		if (execute):
			table[index][0]	= token
			table[index][1] = pos
			table[index][2] = 1	
			lastElem = index			

	# Cut off empty table and sort alphabetically
	del table[lastElem:]
	del table2[lastElem:]
	table = sorted(table,key=lambda l:l[0])

	length = len(table)

	# Write all results to output
	for i in range(length):
		outputstring = table[i][0] + " " + table[i][1] + " " + str(table[i][2]) + '\n'
		output.write(outputstring)

	input_count = open('./output_count.txt', 'r')
	output_count_length = sum(1 for line in input_count)

	output = open('./output_percentages.txt', 'w')

	# Here's where we calculate POS likelihood
	counter = 0

	for i in range(length):
		token = table[i][0]
		pos = table[i][1]
		count = table[i][2]
		
		# Avoid out of range error
		if (i < length-1):
			index = i
			indices = []
			indices.append(index) # Add index of number

			# Check if there are probabilities
			while (table[index+1][0] == token):
				count = count + table[index+1][2]
				index = index+1
				indices.append(index) # Add index of same word

			# When no more, calculate percentages
			num_same = len(indices)
			percentages = [num_same]
			for i in range(num_same): 
				x = float(table[indices[i]][2])
				y = float(count)
				percentage = x / y
				output_string = table[indices[i]][0] + ' ' + table[indices[i]][1] + ' ' + str(percentage)  + '\n'
				output.write(output_string)
		
		# If last element
		else:
			x = float(table[i][2])
			y = float(count)
			percentage = x / y
			output_string = table[i][0] + ' ' + table[i][1] + ' ' + str(percentage)  + '\n'
			output.write(output_string)


	read_percentages = open('./output_percentages.txt', 'r')

	# Prior probabilities
	# Table2 is used for this :)

	pos_list = [[0 for x in range(2)] for x in range(len(table2))] 
	last_index = 0

	for i in range(len(table2)):
		pos = table2[i][1]

		index = -1
		for j in range(len(pos_list)):
			if (pos == pos_list[j][0]):
				index = j

		# index = pos_list.index(pos) if pos in pos_list[i] else -1

		if (index != -1):
			pos_list[index][1] = pos_list[index][1] + 1

		else:
			pos_list[last_index][0] = pos
			pos_list[last_index][1] = 1
			last_index = last_index + 1

	del pos_list[last_index:]

	# POS with smallest probability
        print pos_list
'''	if_not_in_corpus = pos_list[0][0]


	print "This took: ", time.time()-t, "seconds"
	calculate(toTag, if_not_in_corpus);
	input_file.close()
	output.close()


def calculate(input_fl, random):
	input_file = open(input_fl, 'r')
	output_hmm = open('./output_tagged.txt', 'w')
	read_percentages = open('./output_percentages.txt', 'r')


	percent_length = 0
	for line in read_percentages: 
		percent_length = percent_length + 1
	print('percent_length', percent_length)

	rows = percent_length
	columns = 3 

	# Initialize table as 0
	table = [[0 for x in range(columns)] for x in range(rows)]
	index = 0

	read_percentages = open('./output_percentages.txt', 'r')

	table = read_percentages.read().split('\n')
	# Read all percentages into table

	for line in input_file:
		# Skip blank lines
		if not line.strip():
			continue 

		# If not blank
		token = line
		print (token)
		
		pos = ''
		output_line = ''
		found = False
		i = 0
		while (i < range(len(table[0]))):
			print(i)
			print(token, table[i][0])
			if (token == table[i][0]):
				print("Matched!")
				found = True
				if (table[i][2] == 1.0):
					
					pos = table[i][1]
					output_line = s[0] + ' ' + pos + '\n'
					print_output = ''.join(output_line)
					output_hmm.write(print_output)
					break
				else:
					index_first = i
					index_last = i
					all_same = []

					while (table[index_last][0] == token):
						all_same.append(table[index_last])
						index_last = index_last + 1

					all_same = sorted(all_same,key=lambda l:l[2]) # sort by percentages
					pos = all_same[0][1]

					output_line = s[0] + ' ' + pos + '\n'
					print_output = ''.join(output_line)
					output_hmm.write(print_output)
					break
			i = i+1

		
		# Assign randomly based on earlier calculations
		if (found == False):
			pos = random
			output_line = s[0] + ' ' + pos + '\n'
			print_output = ''.join(output_line)
			output_hmm.write(print_output)

	print("Tagging output printed to: output_tagged.txt") 
	input_file.close()
	output_hmm.close()
	

'''
main()
