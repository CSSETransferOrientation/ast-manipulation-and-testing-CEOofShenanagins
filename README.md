# Binary Operator Simplifier 

1. Completed the arithmatic and multiplicative identities, testbench file i/o, and the unit test class

2. I enjoyed the moment this assignment clicked, I liked breaking down the identities and putting the two reductions together, and the file navigation was fun

3. I didn't particularly enjoy navigating between folders and trying to keep all the test cases straight. I've also been getting a serious headache trying to fix a bug that came up after trying the mult_by_zero reduction. It occured by running the following test, and I'm still not sure what caused it.

# ;;> Your testing setup is a little too busted for me to easily find the bug
# ;;> feel free to stop by sometime and we can track it down together if you'd like
input:           * 8 + * * 2 3 4 * 0 4
expected output: * 8 * * 2 3 4 
actual output:   * 8 * * 2 3 3


# ;;> Tests look pretty good, but the idea was to have one test per file. 
