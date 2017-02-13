#!/usr/bin/python3
import logging
import sys

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

#You can't move from tuple[0] to tuple[1], unless you're the key or they key is in used.
valid = {2 : (1,3),
         5 : ((6,4),(9,1),(7,3),(2,8)),
         8 : (9,7),
         4 : (7,1),
         6 : (9,3)}
#If you're not the key, then these moves are actually invalid
invalidList = ((1,3),(6,4),(9,1),(7,3),(2,8),(9,7),(7,1),(9,3))

def determineComboValidity(pattern):
  used = []
  sentinel = len(pattern)-1
  count=0
  move = ()
  invalidPattern = False
  if min(pattern) < 1 or max(pattern) > 9:
    invalidPattern = True
  while count <= sentinel and invalidPattern == False:
    current = pattern[count]
    count +=1
    logger.debug("Trying %s, used list is %s" %  (current,used))  
  #Check if it's in the "used" index. If it is, break
    if current in used:
      logger.debug("Not a valid pattern, value repeated: %s" % (current))
      invalidPattern = True
      break
    else:
      used.append(current)
      logger.debug("added %s, used list is %s" % (current,used))
    if len(used) == 1:
      continue
   # Check used length. If more than 1, get move direction and do everything else, otherwise start over in the loop.
    else:
      #get da moves
      move = (used[count-2],current)
      logger.debug("Movement is {0}".format(move))
      accumulateOldMoves = []
      #get old moves made for comparison if they're valid
      for z in used:
        if z in valid:
          logger.debug("checking old value {0} in valid".format(z))
          accumulateOldMoves.append(valid[z])
          logger.debug("accumulated old list {0}".format(accumulateOldMoves)) 
      #is our current move "valid"?
      if current in valid:
        logger.debug("Is {0} equal to {1} (1st block)?".format(z,move))
        for z in (valid[current], valid[current]): #<-- ugly hack because I'm assuming we're getting tuples. Prevents a single tuple being iterated over.
          if ((z == move) or ((z[1],z[0]) == move)):
              logger.debug("yes.")
      else:
        # If not, let's check out old moves to see if they open up a path..
        finalTruthy = ()
        #First block to grab the edge case of len 1
        if len(accumulateOldMoves) == 1:
          j = tuple(accumulateOldMoves[0])
          logger.debug("Is move {0} equal to old move {1} (2nd block)?".format(move,j))
          if ((j == move) or ((j[1],j[0]) == move)):
            logger.debug("Yes, apparently")
            finalTruthy = True
            break
        else:
        # Is the old key value allowed for the current move?
          for j in accumulateOldMoves:
            logger.debug("Is move {0} equal to old move? {1} (3nd block)?".format(move,j))
            if ((j == move) or ((j[1],j[0]) == move)):
              logger.debug("Yes, apparently")
              finalTruthy = True
              break
        #If we've failed everythng, then we can assume it's not a special case. Valid values also double as invalid if it's not a special case.
        for z in invalidList:
            logger.debug("Is move {0} equal to {1} (FINAL)?".format(move, z))
            if ((z == move) or ((z[1],z[0]) == move)):
              logger.debug("FALSE!")
              finalTruthy = False
              break
        if finalTruthy == False:
            logger.debug("Invalid Pattern")
            invalidPattern = True
          
  #You made it to the end of this mess, congratulations!
  if invalidPattern == True:
    print("{0} is an INVALID pattern!".format(pattern))
  else:
    print("{0} is a valid pattern".format(pattern))
                                                              
patternTests = ((1,6,7,4), (2,1,3), (1,3,2), (1,9), (0,1,2,3,), (1,2,3,2,1))
extendedTests = ((1,9,5), (9,4,5), (2,1,4,5,7,6), (7,2,9,4,3,8,1,6), (7,2,9,4,3,8,1,6,5), (7,8,1), (4,2,6,9), (7,4,6,9,6,8,), (7,4,9,1))
pattern = patternTests + extendedTests

for i in pattern:
  determineComboValidity(i)
