Pattern Scanner
================
Mission
----------
Search a protein sequence database with a PROSITE pattern. Your scripts should take two arguments: a PROSITE pattern string, a filename for a fasta format sequence database. The example database is ws_215.protein.fa. A full definition of PROSITE syntax is in pattern_syntax_rules.
Output: For every match, your script should print out the name and description of the target sequence and the start/end point of the pattern match. Your script should be able to deal with multiple hits per target sequence.

Solution
----------
First of all, I separate the input pattern into many small ones by ‘-’ . Then I check the correctness of each small one and convert them into corresponding regular expression. Lastly, I use the regular expression to search the pre-processed file to dig out the match.

Run Demo
----------
```shell
python prosite.py "[RK]-G-{EDRKHPCG}-[AGSCI]-[FY]-[LIYA]-x(2,4)-[FYLM]." ws_215.protein.fa
```



The Rosencrantz and Guildenstern inference problem (Hidden Markov Model Application)
======================
Mission
-----------
For some people, this may be a nontrivial problem. Leave time to do it properly. I think it’ll be worth your time… you should learn how HMM algorithms work.

In the Tom Stoppard play Rosencrantz and Guildenstern Are Dead, the play opens with Guildenstern flipping coins that always come up heads, against all odds, leading to a discussion of probabilities that sets the tone for the play. In the play, Rosencrantz has no 
doubt about what the next flip will produce, and he complains that the flipping game is
boring. Consider the following more complicated problem, in which Guildenstern’s flips are a
hidden Markov process, and Rosencrantz must use HMM theory to figure out what’s going
on. Stoppard, I’m sure, would approve. 

Here are the rules to a game that our more interesting Guildenstern plays every day.
Guildenstern has two coins. The first coin is fair, and the second coin is biased. He starts with
the first coin. After each flip, there is a small probability that he will secretly switch to the
second coin. Then after each flip of the second coin, there is a small probability that he will
stop flipping coin for the day. (He never switches back 2016to the fair coin.) He asks
Rosencrantz to guess when he switched to the second coin, based solely on the observed
sequence of heads and tails. 

Clearly Rosencrantz can model this as a hidden Markov process. The two coins behave as two
HMM states, emitting H and T with some probability; the small switching probability behaves
as a transition probability from the first to the second state, and the small ending probability
behaves as a transition probability to the usual HMM special end state. 

An example of a string that Rosencrantz might see:
THHHHTTHTTHTTHHTTTTHHTHTHTHTTTTTTHHHHHHTTHTHTHTHHHH
Rosencrantz’s problem: he can’t tell for sure just from looking at a string like this when
Guildenstern switched to the biased coin. But, if he learns HMM theory, he can make a really
good guess (or, as we say to make it sounds less like guesswork, a statistical inference). 

Rosencrantz sees a different sequence of heads and tails every day that they play the game.
A file of the sequences for 100 days of the game is the example file
/share/home/ccwei/courses/2018/pab/hw4/example; the format is one sequence per line,
and some of the lines can be fairly long. Have a look at the file. Do you think you could guess
where the switch happens in each sequence? It’s pretty hard to do by eye (I can’t do it). 

Part a. The HMM architecture.
Draw the HMM architecture (states, emissions and state transitions) that corresponds to
Guildenstern’s game. You don’t need to turn this picture in; but you need it for your own use
for the next parts of the question, and we’ll see its structure anyway in the two Perl scripts
you write. (You might include a description of the architecture in the comments of your Perl
script, though – it’ll help us understand what you’re doing, if you do something we don’t
expect!). 

Part b. Viterbi HMM alignment
Let’s make it a bit easy on Rosencrantz: let’s assume he’s played the game so much that he
knows Guildenstern’s parameters. The first (fair) coin has emission probabilities
p(H)=p(T)=0.5. The second (biased) coin has emission probabilities p(H) = 0.8, p(T) = 0.2. The
probability of switching from the first to the second coin is 0.01; the probability of ending the
sequence after flipping the second coin is 0.05.
Implement a Viterbi dynamic programming alignment procedure in Perl for the HMM you
drew above, using these parameters. Have your script read a file such as the example data
file ```example``` and, for each sequence, find the
maximum likelihood state path. For each sequence, have your Perl script print out the 
maximum likelihood guess for which position was the first flip of the biased coin (e.g. a
number from 2..N for a sequence of length N).
Part c. Forward-Backward HMM alignment and posterior decoding
Of course, the maximum likelihood position is still just a guess; its count can easily be wrong.
We can use Forward-Backward and posterior decoding to get an even more detailed
inference for Rosencrantz.
Implement Forward and Backward dynamic programming procedures in Perl for the HMM,
using the same parameters as above. Have your Perl script read a file such as the example
data file ```example```, and then, for each sequence
in the file, use the Forward and Backward variables to calculate the posterior probability
distribution over positions of the first flip of the biased coin, e.g. for a given position, what is
the probability that this position is the correct guess? For each sequence, have your Perl
script print out the best (most probable) five positions, followed by the summed posterior
probability of all five (e.g. is the probability that one of the five is right).

Solution
-------------
(1)Viterbi: The maximum likelihood guess for which position was the first flip of the biased coin.

(2)Posterior probability:
To calculate the first position of the biased coin, I use the following equation to calculate this probability.
```P(𝛱𝑖−1=1,𝛱𝑖=2 |𝑥,𝜃)=𝑓1(𝑖−1)∗𝑎12∗𝑒2(𝑥𝑖)∗𝑏2(𝑖)/𝑃(𝑥)```
Where
```𝛱𝑖−1=1``` means the previous state is 1 (fair coin)
```𝛱𝑖=2``` means the present state is 2 (biased coin)
```𝑓1(𝑖−1)``` is the forward probability of state 1 at position i-1
```a12``` is the transition probability from 1 to 2
```𝑒2(𝑥𝑖)``` is the ejection probability of sequence Xi at state 2
```𝑏2(𝑖)``` is the backward probability of state 2 at position i
```P(x)``` is the summed probability of sequence x.
Thereafter, I firstly calculate the corresponding forward and backward probability separately, then I use the results to calculate the posterior probability of every position for each sequence.

(3)Verification:
I verify the first position of biased coin in Viterbi with the results in posterior algorithm.
The result is 100% match, which means that Viterbi and posterior algorithm demonstrate the same position.

Run
---------
```shell
python biased_coin.py example
```
