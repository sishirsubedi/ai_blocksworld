# ai_blocksworld

This is a course project for AI course at TAMU.

Implement search algorithms for blocksworld problem.

A written description of how your heuristic works, or what it is based on, or the logic behind it. Briefly address whether it is admissible
or not (an informal argument will suffice).

Heuristics is calculated using the following formula:
	f(n) = g(n) + h(n)
		f(n) is the cheapest solution through n
		g(n) is the cost of getting from current state to state n
		h(n) is the cost of getting to goal state from state n

The main idea - the cost of getting from parent to child is calculated using a mismatch score w.r.t
goal state taken into consideration and  the cost of getting from child to goal state is calculated
using height of each stack and pair wise neighbor analysis.

g(n) is calculated using MD (mismatch difference ) rule:

1. calculate mismatch score of both parent and all children:

This rule checks the first stack and counts how many blocks are not in correct position.
The main idea is that if first stack has blocks already in place as in goal state then state
will get bonus of 2 steps as it will not be necessary to take this block out of stack and then
later put block  back in the correct location. Similarly, if block is not in correct position then
penalty of two steps is given, and depending of number of mismatch, penalty will be multiplied by the mismatch number.

for each block in first stack
	if block is in final position in order then bonus of 2 steps
     else count mismatch and give penalty twice the number of 	mismatch

2. Calculate the difference of the parent child mismatch scores and substract it by child's score:

Calculate parent mismatch score and child mismatch score and then subtract child's mismatch score by
the difference between parents and child's score. The idea is that if you want to describe all your
children based on by how much they are alike goal state when passing through that particular parent.


h(n) is calculated using HN (height neighbor) rule :

Height rule:

Case 1: stack is empty
	Irrespective of position of stack, starting out as empty will be given small bonus of 1 step.

Case 2: goal stack height is one:
	if it already has 'A' in this position then bonus of 2 steps
            if it does not have 'A' in this position then penalty of 2 steps

Case 3: non-goal stack height is one:
	Irrespective of block, starting out as small height in non goal stacks  given small bonus of 1 	step.

Case 4: goal stack height is more than one and in order
          For each block in order- bonus of 2 points

Case 5: goal and non goal stack height is more than one and out of order
	From top of the stack take two pair of blocks. Check the order of blocks and comapre it to how it should be in the final state.
	If blocks are in order(top block will be on top in goal state) in first stack then 2 steps penalty.
	Similarly, if blocks are out of order then penalty will increase to 4 steps because of additional cost of 2 steps
	for flipping it to correct order in goal state.


Neighbor rule:

	When checking if a pair of block is in order, calculate the number of neighbor that must be present between them.
	Add missing number of neighbor to the penalty calculated from height rule because more missing neighbors then more
	number of steps required to search those missing neighbors and bring it to first stack to reach goal state.

So,

g(n) = score from MD rule
h(n) = score from HN rule

and final →   f(n) = score from MD rule + score from HN rule

Conditions for optimality: Admissibility

The heuristic tries to be admissible when considering a single block but it is not admissible when considering groups of blocks in stacks.
At one block level, if the block is not present in first stack in order then minimum step necessary to put it in right position
is one step- pick up the block from wrong position and put it in right position as in goal state.
So, the penalty for this misplaced block will be 1 step. So in cases when the height of stack is one and
correct position is empty then it will calculate only 1 step. However, when we consider more than one block
then we need to consider that we need to move other blocks to create empty position for a block to put it in correct position.
In this case, heuristic algorithm will not be admissible because it overestimates number of steps to consider to arrange blocks
by a factor of 2-3. For example, if a pair of blocks are out of order then optimal step would be 2 steps, but algorithm will
calculate 4 steps 2 for each block to take it out of current location and put it in different temporary position and then later
on put it in correct position. This will be overestimation by a factor of 2 and then depending on neighbors and mismatch rule
there will be additonal pentaly given. Therefore, heuristic algorithm is not admissible and overestimates by a factor of 2 to 3.