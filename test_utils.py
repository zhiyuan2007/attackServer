import string
from random import randint
def _rand_num_by_ratio(low, high, scope = 6, ratio = 0.9):
     val = randint(low, high)
     if (val < high * ratio):
         val %= scope
         val += 1 # val can not be 0
     else:
         newRan = randint(1 , high + 1)
         val = val % newRan
         if (val <= scope):
             val += (scope + 1)
     return val
 
def gen_rand_prefix_domain(prefix_len = 253):
     namestr = string.digits
     namestr += string.lowercase
     #namestr += '-'
     strLen = _rand_num_by_ratio(1, prefix_len, 10)
     domain = ''
     label_len = _rand_num_by_ratio(1, 63)
     count = 0
     for j in range(0, strLen):
         if (len(domain) >= prefix_len - 1):
             break
         domain += namestr[randint(0, len(namestr) - 1)]
         count += 1
         if (count == label_len):
             domain += '.'
             label_len = _rand_num_by_ratio(1, 63)
             count = 0
     if (domain[len(domain) - 1] != '.'):
         domain += "."
     return domain


