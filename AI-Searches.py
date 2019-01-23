
import time

import math

import random

from copy import deepcopy 

class Wizzo:

	# initialize all variables
	def __init__(self, nursery,no_of_rows, no_of_lizards):

		self.nursery = nursery

		self.no_of_rows = no_of_rows

		self.no_of_lizards = no_of_lizards

		# this will store all possible valid states
		self.possible_state  = set()

		# this is dictionary representaion of valid states
		self.dict_of_state = {}

		for i in range(self.no_of_rows):

			for j in range(self.no_of_rows):

				# if cell contains 2 then its not valid cell
				if self.nursery[i][j] == 2:

					self.dict_of_state[(i,j)] = 0

				else:

					# all other cells are added to possible state set and corresponding 
					# dictionary entry is marked 1
					self.possible_state.add((i,j))

					self.dict_of_state[(i,j)] = 1

		self.tree_count = self.find_tree_count()





	def find_tree_count(self):

		tree_count = [0] * self.no_of_rows

		for col in range(self.no_of_rows):

			count = 0

			for row in range(self.no_of_rows):

				if self.nursery[row][col] == 2 : count += 1

			tree_count[col] = count

		return tree_count





	# given a state and a cell, this function will find all invalid states
	def mark_invalid(self, current_state, i,j):

		invalid_set = set()

		# return if row or col exceeds no_of_rows 
		if i >= self.no_of_rows or j >= self.no_of_rows : return 

		# if cell has 2 then none of the cell is marked invalid
		if  current_state[i][j] == 2 : return 

		# In column j, mark all cells as invalid from ith row till the last row (going downward)
		# unless 2 is found, in which case break from loop
		for row in range(i, self.no_of_rows):

			if self.dict_of_state[(row,j)] : invalid_set.add((row, j))

			if current_state[row][j] == 2 : break
		
		# In column j, mark all cells as invalid from i-1 row till the top row (going upward)
		# unless 2 is found, in which case break from loop
		for row in range(i - 1, -1 , -1 ):

			if self.dict_of_state[(row,j)] : invalid_set.add((row, j))

			if current_state[row][j] == 2 : break

		# In row i, mark all cells as invalid from jth column till the right most column (going right)
		# unless 2 is found, in which case break from loop
		for col in range(j, self.no_of_rows):

			if self.dict_of_state[(i,col)] : invalid_set.add((i, col))

			if current_state[i][col] == 2 : break

		# In row i, mark all cells as invalid from j-1 column till the left most column (going left)
		# unless 2 is found, in which case break from loop
		for col in range(j -1, -1, -1):

			if self.dict_of_state[(i,col)] : invalid_set.add((i, col))	

			if current_state[i][col] == 2 : break

		# mark all invalid cells in both the diagonals
		for d_row, d_col in zip(range(i, -1, -1), range(j, -1, -1)):

			if self.dict_of_state[(d_row,d_col)] : invalid_set.add((d_row, d_col))	

			if current_state[d_row][d_col] == 2 : break

		for d_row, d_col in zip(range(i, -1, -1), range(j, self.no_of_rows, 1)):

			if self.dict_of_state[(d_row,d_col)] :invalid_set.add((d_row, d_col))

			if current_state[d_row][d_col] == 2 : break

		for d_row, d_col in zip(range(i, self.no_of_rows, 1), range(j, -1, -1)):

			if self.dict_of_state[(d_row,d_col)] :invalid_set.add((d_row, d_col))

			if current_state[d_row][d_col] == 2 : break

		for d_row, d_col in zip(range(i, self.no_of_rows, 1), range(j, self.no_of_rows, 1)):

			if self.dict_of_state[(d_row,d_col)] :invalid_set.add((d_row, d_col))

			if current_state[d_row][d_col] == 2 : break

		# return invalid set
		return invalid_set

	

	# this function will delete all invalid cells and return a new set of possible states
	# and corresponding dictionary
	def delete_invalid(self, invalid_set, possible_state_values, dict_states):

		# copy inital set and dictionary
		new_possible_set = possible_state_values.copy()

		new_dict_of_state = dict_states.copy()

		# delete all states that are also in invalid set 
		for s in invalid_set:

			if new_dict_of_state[s]:

				new_possible_set.remove(s)

				new_dict_of_state[s] = 0

		# return the new state set and dictionary
		return new_possible_set, new_dict_of_state



	# create state in matrix form
	def create_state(self, lizard_location):

		#print lizard_location[0], lizard_location[1]

		temp_state = deepcopy(self.nursery)

		for lizards in lizard_location:

			#print lizards[0], lizard_location

			temp_state[lizards[0]][lizards[1]] = 1

		return temp_state


	def add_states_to_queue(self, liz_count,liz_loc ,possible_state_set, dict_state ):

		temp_queue= []

		for state in possible_state_set:

			lizard_location = deepcopy(liz_loc)

			lizard_location.append(state)

			lizard_count = liz_count + 1

			if lizard_count == self.no_of_lizards : return "Yes" , lizard_location

			temp_state = self.create_state(lizard_location)

			# find cells that will now be invalid
			invalid_set = self.mark_invalid(temp_state, state[0], state[1])

			# find new valid states set and dictionary
			new_state_set, new_dict_state = self.delete_invalid(invalid_set, possible_state_set, dict_state)
			
			if len(new_state_set) < self.no_of_lizards - lizard_count : continue

			temp_queue.append([lizard_count, lizard_location, new_state_set, new_dict_state])

			#print lizard_count, lizard_location, new_state_set

		return "No", temp_queue

	
	def create_initial_state(self):

		initial_state_nursery = deepcopy(self.nursery)

		initial_state_set = set()

		valid_set = set()

		lizard_count = 0

		for row in range(self.no_of_rows):

			for col in range(self.no_of_rows):

				if initial_state_nursery[row][col] == 0:

					valid_set.add((row,col))
	
		if len(valid_set) < self.no_of_lizards  : return [],()

		while lizard_count < self.no_of_lizards:
		
			new_lizard_loc = random.sample(valid_set, 1)

			row = new_lizard_loc[0][0]

			col = new_lizard_loc[0][1]

			initial_state_nursery[row][col] = 1

			initial_state_set.add((row, col))

			lizard_count += 1

			valid_set.remove(new_lizard_loc[0])


		return initial_state_nursery, initial_state_set


	def calculate_attack(self, state, liz_position):

		attack_count = 0

		for lizards in liz_position:

			row = lizards[0]

			col = lizards[1]

			invalid_set = self.mark_invalid(state, row, col)

			for liz in liz_position:

				if liz in invalid_set and liz != lizards :

					attack_count += 1

		return attack_count



	def find_neighbour(self, current_state_nursery, current_state_set):

		new_state_nursery = deepcopy(current_state_nursery)

		new_state_set = deepcopy(current_state_set)

		valid_set = set()

		for row in range(self.no_of_rows):

			for col in range(self.no_of_rows):

				if new_state_nursery[row][col] == 0:

					valid_set.add((row,col))

		if len(valid_set) < 1 : return [],()
		
		new_lizard = random.sample(valid_set, 1)

		delete_this_lizard = random.sample(new_state_set, 1)

		new_state_nursery[delete_this_lizard[0][0]][delete_this_lizard[0][1]] = 0

		new_state_set.remove(delete_this_lizard[0])

		new_state_nursery[new_lizard[0][0]][new_lizard[0][1]] = 1

		new_state_set.add(new_lizard[0])

		return new_state_nursery, new_state_set




	def is_valid(self, delta, T):

		if delta < 0 : return True

		current_probability = math.exp( -abs(delta / T))

		if random.random() < current_probability :

			 return True

		return False




	def schedule(self, temp, count):

		return  temp / (math.log(self.no_of_rows + count))



	def SA(self):

		timeout = time.time() + (60 * 5) - 20 

		if self.no_of_rows == 0 and self.no_of_lizards == 0 : return "OK" , []

		if sum(self.tree_count) + self.no_of_rows < self.no_of_lizards :

			return "FAIL" , []

		current_state_nursery, current_state_set = self.create_initial_state()

		if current_state_nursery == [] : return "FAIL" ,  []

		current_attack = self.calculate_attack(current_state_nursery, current_state_set)

		T0 = 5

		iteration = 5

		count = 1

		Temp = self.schedule(T0, count)

		while   Temp > 0 and time.time() <= timeout:

			if Temp == 0 or current_attack == 0 : return "OK", current_state_nursery

			count +=1 

			for _ in range(iteration):

				new_state_nursery, new_state_set = self.find_neighbour(current_state_nursery, current_state_set)

				if new_state_nursery == [] : return "FAIL" ,  []

				new_attack = self.calculate_attack(new_state_nursery, new_state_set)

				if new_attack == 0 :

					return "OK", new_state_nursery

				if self.is_valid(new_attack - current_attack, Temp):

					current_state_nursery = deepcopy(new_state_nursery)

					current_state_set = deepcopy(new_state_set)

					current_attack = new_attack
			
			Temp = self.schedule(T0, count)
			
		return "FAIL" ,  []



	# main bfs function
	def bfs(self):

		timeout = time.time() + (60 * 5) - 20 

		if self.no_of_rows == 0 and self.no_of_lizards == 0 : return "OK" , []

		if self.no_of_lizards == 0 : return "OK" , self.nursery

		if sum(self.tree_count) + self.no_of_rows < self.no_of_lizards :

			return "FAIL" , []

		# create queue to store states
		is_answer, queue = self.add_states_to_queue( 0, [], self.possible_state, self.dict_of_state )

		if is_answer == "Yes" : 

				temp_state = self.create_state( queue)

				#print lizard_count, lizard_location

				return "OK", temp_state 

		while queue and time.time() <= timeout:

			lizard_count,lizard_location, new_state_set, new_dict_state = queue.pop(0)

			if lizard_count == self.no_of_lizards : 

				temp_state = self.create_state( lizard_location)

				return "OK", temp_state

			if len(new_state_set) < self.no_of_lizards - lizard_count : continue

			is_answer, queue_with_new_element = self.add_states_to_queue(lizard_count, lizard_location, new_state_set,new_dict_state )

			if is_answer == "Yes" : 

				temp_state = self.create_state( queue_with_new_element)

				return "OK", temp_state

			queue.extend(queue_with_new_element)

		return "FAIL" ,  []





	# this function is recursively called to perform DFS
	def dfs_sub(self, state, col, lizard_count, possible_state_values, dict_states, timeout):

		# if possible states are less than number of lizards to be placed then return False
		if len(possible_state_values) < self.no_of_lizards - lizard_count : return False

		# if lizard count matches total lizards that were to be placed then return True
		if lizard_count == self.no_of_lizards : return True

		if sum(self.tree_count[col:]) + self.no_of_rows - col + 1 < self.no_of_lizards - lizard_count : return False

		if time.time() >= timeout : return False

		# for each col, iterate each row one by one
		for row in range(self.no_of_rows):

			# if valid state is found, then place lizard in that cell
			if dict_states[(row,col)]:

				# set value of that cell as 1
				state[row][col] = 1

				# increment lizard count
				lizard_count += 1

				# find cells that will now be invalid
				invalid_set = self.mark_invalid(state, row, col)

				# find new valid states set and dictionary
				new_state_set, new_dict_state = self.delete_invalid(invalid_set, possible_state_values, dict_states)

				# call dfs_sub on same column with new valid states
				for next_col in range(col, self.no_of_rows):

					if  self.dfs_sub(state, next_col, lizard_count, new_state_set, new_dict_state, timeout):

						# return True if a solution is found
						return True

				# if current row,col could not find the final solution then revert
				# mark state[row][col] as 0
				state[row][col] = 0

				# decrease lizard count
				lizard_count -= 1

				# now (row,col) state would never give a solution so remove it from
				# possible states set
				possible_state_values.remove((row, col))
				
				dict_states[(row,col)] = 0
	
		return False	



	# main DFS function
	def dfs(self):

		timeout = time.time() + (60 * 5) - 20 

		if self.no_of_rows == 0 and self.no_of_lizards == 0 : return "OK" , []

		if sum(self.tree_count) + self.no_of_rows < self.no_of_lizards :

			return "FAIL" , []

		# make a copy of nursery so that original state remains unaffected
		state = deepcopy(self.nursery)

		# set current lizard count
		lizard_count = 0

		# for each column call DFS_sub till a solution is found, If no solution , return "FAIL"	
		for col in range(self.no_of_rows):

			if self.dfs_sub(state, col, lizard_count, self.possible_state, self.dict_of_state, timeout):

				return "OK", state	

			if time.time() >= timeout : break	

		return "FAIL", []



# this will parse the given input file
def parse_input():

	# open input file
	input_file = "input.txt"

	with open(input_file,'r') as inp: 

		# get all the contents of the file in variable content
		contents = [x.strip('\n') for x in inp.readlines()]

		nursery = []

		# get value of algo
		algo = contents[0]

		# get no of rows 
		no_of_rows = int(contents[1])

		# get number of lizards
		no_of_lizards = int(contents[2])

		# remaining content is matrix for nursery
		for line in contents[3 :]:

			row = map(int,list(line.strip()))

			nursery.append(row)

	# return all values to main function
	return algo, no_of_rows, no_of_lizards, nursery



# write the output in output file
def write_ouput(pass_status, new_nursery):

	# open output file
	out_file =  "output.txt"

	with open(out_file, 'w') as out: 

		# write pass or fail status
		out.write(pass_status + "\n")

		# if new nursery matrix is present then add that to output file
		if new_nursery:

			for line in new_nursery:

				line = map(str, line)

				l = "".join(line)

				out.write(l + "\n")



# main function
def main():


		# parse input file to get the input variables
		algo, no_of_rows, no_of_lizards, nursery = parse_input()

		if algo == "DFS":

			# call DFS Algo
			pass_status, new_nursery = Wizzo(nursery, no_of_rows, no_of_lizards).dfs()

			# write the output in output file
			write_ouput(pass_status, new_nursery)

		if algo == "BFS":

			# call BFS Algo
			pass_status, new_nursery = Wizzo(nursery, no_of_rows, no_of_lizards).bfs()

			# write the output in output file
			write_ouput(pass_status, new_nursery)


		if algo == "SA":

			# call SA Algo
			pass_status, new_nursery = Wizzo(nursery, no_of_rows, no_of_lizards).SA()

			# write the output in output file
			write_ouput(pass_status, new_nursery)

			


if __name__ == '__main__':
 
	main()
	
