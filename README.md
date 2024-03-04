# Summary

To help get up to speed with DeepReach, I am creating this repo to assist anyone in understanding the concept of reachability, the HJ PDE, and DeepReaches NN PDE solution. 

This will all be done on a pendulum to allow for nice visualisations. The steps are as follows:

1. Pendulum dynamics
2. Grid search from starting cndoitions with no onctrol to find the largest region of attraction
3. Add a small bounded control action
4. Calculate the optimal control to return you to the region of attraction from outside
5. Grid search to find the set of points that can be returned to the region of attraction from outside of it
6. plot it - this is the reachable set
7. Implement a formal HJ PDE solution to the problem and look at your optimal control vs its control action
8. Implement DeepReach itself on the same problem and compare its solutions with yours and the analytical HJ PDE solution