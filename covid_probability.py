import numpy as np
import pdb
import math

###################
### Assumptions ###
###################
FP = 0.01  # False Positive Rate. Just said 'rare' online.
FN = 0.20  # False Negative Rate. People quote 20% ofen. P

# Prior on likelihood a random person in Alameda County 
# has covid and is contagious.
A_POS = 0.0065  # 10887 / 1,671,329
# According to [1] there have been 10887 new cases in
# the last 14 days, which is about the number of people that are contagious.
# Popluation of Alameda is 1,671,329.

# [1] https://www.sfchronicle.com/projects/coronavirus-map/

# For testing this code.
# A_POS = 0.5  

# Known from assumptions because these are binary events.
TP = 1 - FN  # True Positive Rate. e.g. 1 - 0.2 = 0.8
TN = 1 - FP  # True Negative Rate. 1 - 0.99 = 0.1
A_NEG = 1 - A_POS  # Probabily you think he didn't have it.



############
### Math ###
############
# Want to know what's the probability andrew is sick given the test results.
# A=1 -> Andrew Contagious. T=1 - Test is positive.
# FP = P(T=1|A=0)
# FN = P(T=0|A=1)

def get_p(t, a):
  # P(T=t | A=a)
  if t == 0 and a == 0:
    return TN
  elif t == 0 and a == 1:
    return FN
  elif t == 1 and a == 0:
    return FP
  elif t == 1 and a == 1:
    return TP
  raise Exception ("Doggie no! No Doggie!", t, a)

def probability_a_equals_given_results(test_results, a):
  numerator = 1
  denominators = [A_NEG, A_POS]  # For a=0, a=1
  for t in test_results:
    numerator *= get_p(t, a)
    denominators[0] *= get_p(t, 0)
    denominators[1] *= get_p(t, 1)
  denominator = np.sum(denominators)
  
  if a == 1:
    numerator *= A_POS
  elif a == 0:
    numerator *= A_NEG
  else:
    raise Exception("Doggie, c'mon.")

  return numerator / denominator


####################
### Test Results ###
####################
# test_results = [1, 0, 0]  # Positive Friday, Negative Monday, Negative Monday.
# test_results = [1]
test_results = [1, 0] # Positive Friday, Negative Monday, 


p_pos = probability_a_equals_given_results(test_results, 1)
p_neg = probability_a_equals_given_results(test_results, 0)
assert np.allclose(p_pos + p_neg, 1.0)  # Testing this code.

print ("Probability has the virus: %.2f%%" % (p_pos * 100))
print ("Probability does not have the virus: %.2f%%" % (p_neg * 100))
