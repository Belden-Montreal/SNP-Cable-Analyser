import pylab
import skrf as rf

import numpy as np



'''cm = (1/np.sqrt(2)) * np.matrix([[1, -1, 0, 0],
                                   [1, 1, 0, 0],
                                   [0, 0, 1, -1],
                                   [0, 0, 1, 1]], dtype = float)'''


swap =  np.matrix([[0, 1, 0, 0],
                   [1, 0, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]], dtype = float)

print swap

cm = (1/np.sqrt(2)) * np.matrix([[1, -1, 0, 0],
                                   [1, 1, 0, 0],
                                   [0, 0, 1, -1],
                                   [0, 0, 1, 1]], dtype = float)



# create a Network type from a touchstone file
rs = [rf.Network('fci.s4p'), rf.Network('fci.s4p')]


'''

        Respresentation of the ports before mapping

        Example : rs.renumber([1,2], [2,1]) swaps pin 1 with pin 2
                        
                   111111111111111111  
 (0)   ------------1                1------------   (2)
                   1                1
                   1                1
                   1                1
 (1)   ------------1                1------------   (3)
                   111111111111111111
'''

rs[0].renumber([1,2], [2,1] )

#orderMatrix = (swap * (rs * np.linalg.inv(swap)))

#out = (cm*orderMatrix)*np.linalg.inv(cm)

#out.renumber([0,-1], [-1,0] )


#print out.s

#orderMatrix.se2gmm(2)


rs[0].se2gmm(2)

#print rs


#print rs.se2gmm()
#rs.plot_s_smith(label = "1")
#pylab.show()

rs[0].write_touchstone("testout_mm", form="ri")





print np.array( list(rs[0].s[i,:,:].diagonal() for i in range(len(rs[0].f))))[0,0]


#rs.se2gmm(p=2)
#rs.plot_s_smith(label = "1")
#pylab.show()

#rs.write_touchstone("testout_mm")

