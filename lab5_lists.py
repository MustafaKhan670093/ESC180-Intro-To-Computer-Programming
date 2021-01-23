# Learning goal: process lists of lists using nested loops: https://www.cs.toronto.edu/~guerzhoy/180/labs/lab05.py
#

#From the last lab
def lists_are_the_same(list1, list2):
    '''Return True iff list1 and list2 have the same elements in the same order

    Arguments:
    list1, list2 -- lists

    '''
    if len(list1) != len(list2):   #Take care of the easy case first
        return False

    i = 0
    while i < len(list1):
        if list1[i] != list2[i]:
            return False          #If even one pair differs, we can return
                                  #False right away
        i += 1

    return True                   #Checked all the pairs, didn't return False
                                  #so therefore must return True

################################################################################
def list1_starts_with_list2(list1, list2):
    '''Return True iff the first len(list2) elements of list1 are the same,
    and are in the same order as, list2

    Arguments:
    list1, list2 -- lists
    '''
    #Almost the same idea as in lists_are_the_same
    if len(list1) < len(list2):
        return False

    i = 0
    while i < len(list2):
        if list1[i] != list2[i]:
            return False

        i += 1


    return True



def list1_starts_with_list2_noloops(list1, list2):
    '''Return True iff the first len(list2) elements of list1 are the same,
    and are in the same order as, list2

    Arguments:
    list1, list2 -- lists
    '''

    return list1[:len(list2)] == list2

    #Note: we didn't have to check the whether  list1 is longer than
    #list2, since list1[:len(list2)] happens to work even for large
    #len(list2) (if n > len(list1), list1[:n] is simply list1[:]

    #Longer (and worse) version that does the same thing:
    #if list1[:len(list2)] == list2
    #  return True
    #else:
    #  return False

################################################################################

def match_pattern(list1, list2):
    '''Return True iff list2 appears as a sublist of list1

    Arguments:
    list1, list2 -- lists
    '''
    #Same idea as above
    #Note: len(n) for n < 1 is just [], so we don't need to explicitly consider
    #the case that len(list2) > len(list1)
    for i in range(len(list1)-len(list2)+1):
        if list1[i:(i+len(list2))] == list2:
            return True

    return False

################################################################################
def duplicates(list1):
    '''Return True iff list1 has two equal adjacent elements
    Arguments:
    list1 -- a list
    '''

    for i in range(len(list1)-1):
        if list1[i] == list1[i+1]:
            return True

    return False


################################################################################

def print_matrix_dim(M):
    '''Print the dimensions of matrix M, represented as a
    list of lists

    Arguments:
    M -- a matrix, represented as a list of lists
    '''
    print(str(len(M)) + "x" + str(len(M[0])))



def dot_product(a, b):
    '''Return the dot product of the vectors a and b

    Arguments:
    a, b -- vectors represented as lists, which must be of the same length
    '''

    s = 0
    for i in range(len(a)):
        s += a[i]*b[i]

    return s


def mult_M_v(M, v):
    '''Return the product Mv of the matrix M and the vector v.

    Arguments:
    M -- a matrix, represented as a list of lists, of size nxm
    v -- a vector, represented as a list, of size m
    '''

    prod = []
    for i in range(len(M)):
        prod.append(dot_product(M[i], v))

    return prod

###############################################################################

#Slicing for "extending in the middle"
# We can use the following in order to "insert" several elements at once in the middle of a list.
L = [42, 43, 45]
M = [51, 52]
L[1:1] = M
#print(L) would result in [42, 51, 52, 43, 45]

###############################################################################

#list.sort() and sorted()
#Here is how we can sort lists in ascending order.
Q = [5, 2, 10, 20, 1]
sorted(Q)
#Q.sort() does the same thing.

#You can sort lists of strings as well. 
# #Those are sorted in alphabetical (called, lexicographical) order:
X = ["CSC", "CIV", "PRA", "ESC"]
sorted(X)

###############################################################################