"""biased_coin.py    515111910078   yangjunchen"""
import sys
import numpy as np
import math
"""model_construction(): define the parameters of a hmm"""
def model_construction():
	A = ['H','T']
	S = [0,1,2,'end']   
	Eje_prob = {1:{'H':0.5,'T':0.5},2:{'H':0.8,'T':0.2}}
	Tra_prob = {0:{1:1,2:0,'end':0},1:{1:0.99,2:0.01,'end':0},2:{1:0,2:0.95,'end':0.05}}
	return A,S,Eje_prob,Tra_prob
"""readin(): readin the parameters"""
def readin():
	parameters = sys.argv
	if len(parameters) == 1:
		return -1 
	elif len(parameters) != 2:
		return -2 
	else :
		file = open(parameters[1],'r')
		content = file.readlines()
		file.close()
		return content
"""viterbi(seqs,A,S,ejec_prob,tran_prob): calculate the optimal path"""
def viterbi(seqs,A,S,ejec_prob,tran_prob):
	
    all_path = []
    for seq in seqs:
        seq = seq.strip()
        """path: save the path"""
        path = (len(seq)+1)*[S[0]]
        """prev: use to retrace the path"""
        prev = np.zeros((len(S[0:-1]),len(seq)),dtype = int)
        v = {}

        #initializing
        for state in S:
            v[state] = {}
        for state in S:
            if state == 0:
                v[state][0] = 1
            else:
                v[state][0] = 0
        #circle
        for pos in range(1,len(seq)+1):
            for sta in S[1:-1]:
                max_pro = 0
                if pos == 1:
                    begin = 0
                else :
                    begin = 1
                """find the max_pro"""
                for pre_sta in S[begin:-1]:
                    tmp = float(v[pre_sta][pos-1]*tran_prob[pre_sta][sta])
                    if tmp > max_pro:                       
                        max_pro = tmp
                        prev[sta][pos-1] = pre_sta
                v[sta][pos] = float(ejec_prob[sta][seq[pos-1]]*max_pro)
        #ending
        max_pro = 0
        for pre_sta in S[1:-1]:
            tmp = float(v[pre_sta][pos]*tran_prob[pre_sta][S[-1]])
            if tmp > max_pro:
                P_viterbi = tmp
                ending_state = pre_sta
        #retrace path
        path[len(seq)] = ending_state
        current_state = ending_state
        for i in range(len(seq)-1,-1,-1):
            path[i] = prev[current_state][i] 
            current_state = path[i]

        all_path.append(path)

    return all_path
"""forward_back_post(seqs,A,S,ejec_prob,tran_prob): calculate the forward, backward, and posterior probability"""
def forward_back_post(seqs,A,S,ejec_prob,tran_prob):
    Top5_set = []
    for seq in seqs:        
        seq = seq.strip()
        """forward algorithm"""
        f = {}

        #initializing
        for state in S:
            f[state] ={}
        for state in S:
            if state == 0:
                f[state][0] = 1
            else:
                f[state][0] = 0
        #circle
        for pos in range(1,len(seq)+1):
            for sta in S[1:-1]:
                if pos == 1:
                    begin = 0
                else :
                    begin = 1
                f[sta][pos] = ejec_prob[sta][seq[pos-1]]*sum(f[pre_sta][pos-1]*tran_prob[pre_sta][sta]for pre_sta in S[begin:-1])
                #if f[sta][pos ] == 0:
                    #print "0!",sta,pos
        #ending
        P_x = sum(f[pre_sta][len(seq)]* tran_prob[pre_sta][S[-1]]for pre_sta in S[1:-1])
        
        """backward algorithm"""
        b = {}

        #initializing
        for state in S[1:-1]:
            b[state] = {}
            b[state][len(seq)] = tran_prob[state][S[-1]]
        #circle
        for pos in range(len(seq)-1,0,-1):
            for sta in S[1:-1]:
                b[sta][pos] = sum(tran_prob[sta][post_sta]*ejec_prob[post_sta][seq[pos]]*b[post_sta][pos+1] for post_sta in S[1:-1])
        
        """posterior prob"""
        """P_first2 keeps the probability of the first biased coin of every position"""
        P_first2 = len(seq) * [0]
        for pos in range(2,len(seq)+1):
            P_first2[pos-1] = float(f[S[1]][pos-1]*tran_prob[S[1]][S[2]]*ejec_prob[S[2]][seq[pos-1]]*b[S[2]][pos]) / P_x
        P_first2 = np.array(P_first2)
        
        """find the max 5 probs in P_first2"""
        new_top5 = np.argpartition(P_first2,-5)[-5:]
        top5_result = {}
        for i in new_top5:
            top5_result[i+1] = P_first2[i]
        Top5_set.append(top5_result)


    return Top5_set


def main():
    seqs = readin()
    if seqs == -1:
        print "Usage:python biased_coins.py filename"
        return 
    elif seqs == -2:
        "Error: Too many or too less parameters"
        return
    else:

        A,S,E,T = model_construction()       
####viterbi
        paths = viterbi(seqs,A,S,E,T)
        first_pos = []
        
        file0 = open("viterbi_results.txt",'w')
        print "-----------viterbi_results----------"
        file0.write("viterbi_results\n")
        for i,path in enumerate(paths):
            first_pos.append(path.index(2))
            print "Sequence:",i,"Position:", path.index(2)
            file0.write("Sequence:")
            file0.write(str(i))
            file0.write('\t')
            file0.write("Position:")
            file0.write(str(path.index(2)))
            file0.write('\n')
        file0.close()
        
           
###forward
        bayes_results= forward_back_post(seqs,A,S,E,T) 
        
        count = 0
        match = 0
        
        file = open("posterior_results.txt",'w')
        print "-------posterior results----------"
        file.write("-------posterior results----------\n")
        for result in bayes_results:
            print "Sequence:", count+1
            file.write("Sequence:")
            file.write(str(count+1))
            temp = sorted(zip(result.values(),result.keys()),reverse=True)
            if temp[0][1] == first_pos[count]:
                    match += 1
            pros = 0
            for item in temp:
                pros += item[0]
                print "Position" ,"probability"
                file.write("Position\t")
                file.write("probability\n")
                print item[1],'\t',item[0]
                file.write(str(item[1]))
                file.write('\t')
                file.write(str(item[0]))
                file.write('\n')
            print "summed probability"
            print pros
            print "------------------"
            file.write("summed probability\n")
            file.write(str(pros))
            file.write("\n------------------\n")
            count += 1

        """hit_percentage: the probability of the same biased coin result between viterbi and posterior """
        print "hit_percentage: ", float(match)/len(paths)
        file.write("hit_percentage: ")
        file.write(str(float(match)/len(paths)))
        file.write('\n')
        file.close()
       
        
if __name__ == '__main__':
	main()



