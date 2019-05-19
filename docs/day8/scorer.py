import re 
import os, sys

def read_timex_from_file(fpath):
    with open(fpath, 'r') as f:
        return re.findall('<TIMEX>([^<]+)</TIMEX>', f.read())

def update_scores(gold_timex, subm_timex):
    global true_positive, false_positive, false_negative
    tp = len([s for s in subm_timex if s in gold_timex])
    fp = len(subm_timex) - tp
    fn = len(gold_timex) - tp
    true_positive  += tp
    false_positive += fp
    false_negative += fn
    return (tp, fp, fn)


def print_file_result(d, output, gold_timex, subm_timex, scores):
    with open(output, 'a') as out:
        out.write("Gold file: %s, submitted file: %s \n" %(d, d.replace('ann','sub')))
        out.write("\nGold annotations: \n")
        for g in gold_timex:
            out.write(g+"\n")
        out.write("\nSubmitted annotations: \n")
        for s in subm_timex:
            out.write(s+"\n")
        out.write("\n-------- \n")
        out.write("True positive: %d, False positive: %d, False negative: %d \n" %scores)
        out.write("\n=========================================================================\n\n")

		
if __name__ == "__main__":
    gold_dir  = os.path.abspath(sys.argv[1])
    submitted_dir = os.path.abspath(sys.argv[2])
    try:
        output = os.path.abspath(sys.argv[3])
    except IndexError:
        output = os.path.join(submitted_dir, "../scorer_output.txt")

    if os.path.exists(output):
        os.remove(output)

    true_positive  = 0.0
    false_positive = 0.0
    false_negative = 0.0
					  
    for d in os.listdir(gold_dir):
        gold_timex = read_timex_from_file(os.path.join(gold_dir,d))
        subm_timex = read_timex_from_file(os.path.join(submitted_dir,d.replace('ann','sub')))
        scores = update_scores(gold_timex, subm_timex)
        print_file_result(d, output, gold_timex, subm_timex, scores)
		
    if true_positive == 0:
        recall = precision = f_measure = 0.0
    else:
        recall     = true_positive/(true_positive + false_negative)
        precision  = true_positive/(true_positive + false_positive)
        f_measure  = 2*recall*precision/(recall+precision)

    with open(output, 'a') as out:
        out.write("True positive:  %2.2f \n" %true_positive)
        out.write("False positive: %2.2f \n" %false_positive)
        out.write("False negative: %2.2f \n" %false_negative)
        out.write("-------- \n")
        out.write("Recall:    %2.2f \n"	%(100*recall   ))
        out.write("Precision: %2.2f \n"	%(100*precision))
        out.write("F1-score:  %2.2f \n"	%(100*f_measure))

    print ("recall: %2.2f, precision %2.2f, f1-score %2.2f"
           %(100*recall, 100*precision, 100*f_measure))
    print ("Scorer output: \n%s" % os.path.abspath(output))
