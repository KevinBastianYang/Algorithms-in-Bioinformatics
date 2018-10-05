Algorithms in Bioinformatics Project
=======================
Mission
----------------
The goal of this project is to use the kth-order markov method to classify a set of short genomic
sequences. Each short sequence will be classified to one group, which is represented by a genome
in a reference genome data set. The file containing short genomic sequences can be found at
/share/home/ccwei/courses/2018/pab/proj1/reads.fa. The 10 genomes can be found under the
directory /share/home/ccwei/courses/2018/pab/proj1/genomes/. A test set has been created for
you: 20,000 short reads are given in /share/home/ccwei/courses/2018/pab/proj1/test/test.fa. The
mapping of aligned genomes and the short sequences listed in test.fa is given in a file called
seq_id.map file. You can use these files to test your own script.
You are expected to include in your report the implementation of your kth
-order markov method
together with the following results. Your scripts needs to be handed in as supplementary
materials.
1. the total number of short sequences in the file reads.fa;
2. (*) the number of reads that can be assigned to a genome in the genome dataset (with
whatever criteria you use);
3. (*) the number of reads that can’t be assigned to any genome in the genome dataset ;
4. the number of groups with at least j short sequences assigned, where j = 1, 5, 10 or 50. 
5. for those groups with at least 10 short sequences assigned, list the total numbers of short
sequences assigned to those groups. Then you can draw a pie chart to show the relative
frequency of each group. 

Solution
---------------
Because the k-th order markov model in which a state contains 1 sequence is equivalent to 1 order markov in which a state contains k sequences, I calculate the transition probability matrix (maximum likelihood) of different k sequences for each genome. Then for each read, I scan the k sequences and calculate the corresponding probability score for each genome matrix and select the maximum score and corresponding genome as the assignment( if the maximum score - the second / second score < 0.05, this read will not be assigned).

Test
---------------
I use the given 20000 reads as test to see the performance of my codes. I use different k(ranging from 3 to 11) and compare the assignment result with the seq map(golden standard).

```shell
python test.py
```
The assigned map for different k will be in test_result folder. Then run compare.py to see the accurary

```shell
python compare.py
```

* Note:1. test.py can take 5 minutes to process different k 2. I rename the original genome data file to 0.fna, 1.fna, 2.fna, … ,9.fna)
In the results We can see the bigger the k, the more accurate the results are. So I use k = 9, 10, 11 to demonstrate the final results.

Demo
-----------------
```shell
python demo.py
```
The detailed assignment results(seq_id_k.map) and the statistical results (count_k.txt) are in demo_result folder.

Results and Discussion
-----------------
Shown in proj1.pdf
