# Name: Riya Dev
# Date: 12/12/2020
# test state: .OO.X.X..

def successors(state, turn):
   sli = [i for i in range(len(state)) if state[i] == '.']
   ret = [(state, state[0:i] + turn + state[i+1:]) for i in sli]
   return ret  # [(previous state, new state), ...]

def terminal_test(state, tc):
   if state.find('.') < 0: return True    # check empty spot
   for li in tc:
      check_li = [state[x] for x in li]
      if len(set(check_li)) == 1 and check_li[0] != '.':
         return True
   return False
      
def utility(turn, tc, state):
   # return 1 (turn wins), -1 (turn loses), or 0 (tie)
   # tc: [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
   for li in tc:
      for x in li:
         if state[li[0]] == turn and state[li[1]] == turn and state[li[2]] == turn:
            return 1
         elif state[li[0]] != turn and state[li[1]] != turn and state[li[2]] != turn:
            return -1
   return 0

def minimax(state, turn, tc):
   return max_value(state, turn, tc)[1]   # returns state

def max_value(state, turn, tc):
   # return value and state: (val, state)
   if terminal_test(state, tc):
      return utility(turn, tc, state), state  # from max's view
   value = -1000000000 # float('-inf') -> -1000000
   if turn == 'X':
         otherturn = 'O'
   else: otherturn = 'X'
   for a, s in successors(state, turn):
      prevval = value
      value = max(value, min_value(s, otherturn, tc)[0])
      if (prevval != value):
         state = s 
   return value, state
   
def min_value(state, turn, tc):
   # return value and state: (val, state)
   if terminal_test(state, tc): # from max's view
      if utility(turn, tc, state) == 1:
         return -1, state
      elif utility(turn, tc, state) == -1:
         return 1, state
      else: return 0, state
   value = 1000000000 # float('inf') -> 1000000
   if turn == 'X':
         otherturn = 'O'
   else: otherturn = 'X'
   for a, s in successors(state, turn):
      prevval = value
      value = min(value, max_value(s, otherturn, tc)[0])
      if (prevval != value):
         state = s
   return value, state

def get_turn(state):
   count = {'X': 0, 'O': 0, '.':9}
   for s in state: count[s] += 1
   return 'O' if count['O'] < count['X'] else 'X' 

def conditions_table(n=3, n2=9):
   ret = [[] for i in range(n*2+2)]
   for i in range(n2):
      ret[i//n].append(i)     # rows: [0, 1, 2], [3, 4, 5], [6, 7, 8]
      ret[n+i%n].append(i)    # cols: [0, 3, 6], [1, 4, 7], [2, 5, 8]
      if i//n == i % n: ret[n+n].append(i)   # diagonal \: [0, 4, 8]
      if i // n == n - i%n - 1: ret[n+n+1].append(i)  # diagonal /: [2, 4, 6]
   return ret

def display(state, n=3, n2=9):
   str = ""
   for i in range(n2):
      str += state[i] + ' '
      if i % n == n-1: str += '\n'
   return str

def human_play(s, n, turn):
   index_li = [x for x in range(len(s)) if s[x] == '.']
   for i in index_li:
      print ('[%s] (%s, %s)' % (i, i//n, i%n))
   index = int(input("What's your input? (Type a number): "))
   while s[index] != '.':
      index = int(input("Invalid. What's your input? "))
   state = s[0:index] + turn + s[index+1:]
   return state
   
def main():
   X = input("X is human or AI? (h: human, a: AI) ")
   O = input("O is human or AI? (h: human, a: AI) ")
   state = input("input state (ENTER if it's an empty state): ")
   if len(state) == 0: state = '.........'
   turn = get_turn(state)
   tc = conditions_table(3, 9)
   #print(tc)
   print ("Game start!")
   print (display(state, 3, 9))
   while terminal_test(state, tc) == False:
      if turn == 'X':
         print ("{}'s turn:".format(turn))
         if X == 'a': state = minimax(state, turn, tc)
         else: state = human_play(state, 3, turn)
         print (display(state, 3, 9))
         turn = 'O'
      else:
         print ("{}'s turn:".format(turn))
         if O == 'a': state = minimax(state, turn, tc)
         else: state = human_play(state, 3, turn)
         print (display(state, 3, 9))
         turn = 'X'
         
   if utility(turn, tc, state) == 0:
      print ("Game over! Tie!")
   else: 
      turn = 'O' if turn == 'X' else 'X'
      print ('Game over! ' + turn + ' win!')

if __name__ =='__main__':
   main()