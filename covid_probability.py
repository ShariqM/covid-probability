import numpy as np
import pdb
import math

###################
### Assumptions ###
###################
FP = 0.01  # False Positive Rate. Just said 'rare' online.
FN = 0.20  # False Negative Rate. People quote 20% ofen. 

# Prior on likelihood a random person in Alameda County 
# has covid and is contagious.
S_POS = 0.0065  # 10887 / 1,671,329
# According to [1] there have been 10887 new cases in
# the last 14 days, which is about the number of people that are contagious.
# Popluation of Alameda is 1,671,329.

# [1] https://www.sfchronicle.com/projects/coronavirus-map/

# For testing this code.
# S_POS = 0.5  

# Known from assumptions because these are binary events.
TP = 1 - FN  # True Positive Rate. e.g. 1 - 0.2 = 0.8
TN = 1 - FP  # True Negative Rate. 1 - 0.99 = 0.1
S_NEG = 1 - S_POS  # Probabily you think he didn't have it.



############
### Math ###
############
# Want to know what's the probability andrew is sick given the test results.
# S=1 -> Subject has covid. T=1 - Test is positive.
# FP = P(T=1|S=0)
# FN = P(T=0|S=1)

def get_p(t, s):
  # P(T=t | S=s)
  if t == 0 and s == 0:
    return TN
  elif t == 0 and s == 1:
    return FN
  elif t == 1 and s == 0:
    return FP
  elif t == 1 and s == 1:
    return TP
  raise Exception ("Doggie no! No Doggie!", t, s)

def probability_s_equals_given_results(test_results, s):
  numerator = 1
  denominators = [S_NEG, S_POS]  # For s=0, s=1
  for t in test_results:
    numerator *= get_p(t, s)
    denominators[0] *= get_p(t, 0)
    denominators[1] *= get_p(t, 1)
  denominator = np.sum(denominators)
  
  if s == 1:
    numerator *= S_POS
  elif s == 0:
    numerator *= S_NEG
  else:
    raise Exception("Doggie, c'mon.")

  return numerator / denominator


####################
### Test Results ###
####################
# test_results = [1, 0, 0]  # Positive Friday, Negative Monday, Negative Monday.
# test_results = [1]
test_results = [1, 0] # Positive Friday, Negative Monday, 


p_pos = probability_s_equals_given_results(test_results, 1)
p_neg = probability_s_equals_given_results(test_results, 0)
assert np.allclose(p_pos + p_neg, 1.0)  # Testing this code.

print ("With test results: ", test_results)
print ("Probability subject has the virus: %.2f%%" % (p_pos * 100))
print ("Probability subject does not have the virus: %.2f%%" % (p_neg * 100))
