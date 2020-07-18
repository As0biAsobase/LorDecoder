import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

class Calculator:
    def __init__(self):
        # self.population = 0
        # self.desired = 0
        # self.draws = 0
        # self.desired_in_draws = 0
        pass
    def hypergeom_pmf(self, N, A, n, x):

        '''
        Probability Mass Function for Hypergeometric Distribution
        :param N: population size
        :param A: total number of desired items in N
        :param n: number of draws made from N
        :param x: number of desired items in our draw of n items
        :returns: PMF computed at x
        '''
        Achoosex = comb(A,x)
        NAchoosenx = comb(N-A, n-x)
        Nchoosen = comb(N,n)

        return (Achoosex)*NAchoosenx/Nchoosen

    def hypergeom_cdf(self, N, A, n, t, min_value=None):

        '''
        Cumulative Density Funtion for Hypergeometric Distribution
        :param N: population size
        :param A: total number of desired items in N
        :param n: number of draws made from N
        :param t: number of desired items in our draw of n items up to t
        :returns: CDF computed up to t
        '''
        if min_value:
            return np.sum([self.hypergeom_pmf(N, A, n, x) for x in range(min_value, t+1)])

        return np.sum([self.hypergeom_pmf(N, A, n, x) for x in range(t+1)])

    def hypergeom_plot(self, N, A, n):

        '''
        Visualization of Hypergeometric Distribution for given parameters
        :param N: population size
        :param A: total number of desired items in N
        :param n: number of draws made from N
        :returns: Plot of Hypergeometric Distribution for given parameters
        '''

        x = np.arange(0, n+1)
        y = [self.hypergeom_pmf(N, A, n, x) for x in range(n+1)]
        plt.plot(x, y, 'bo')
        plt.vlines(x, 0, y, lw=2)
        plt.xlabel('# of desired items in our draw')
        plt.ylabel('Probablities')
        plt.title('Hypergeometric Distribution Plot')
        plt.show()

# f = Calculator()
# print(f.hypergeom_pmf(40, 3, 7, 1))
# f.hypergeom_plot(40, 3, 20 )
