import csv

class Itemset:
    '''The class to represent itemsets
    It is comparable and also hashable
    '''
    def __init__(self, ar, count = 0):
        self.items = ar;
        self.count = count;
    def __hash__(self):
        return self.items.__hash__();
    def __eq__(self, other):
        return (self.items == other.items);
    def __str__(self):
        return '{' + str(self.items) + ', count: ' + str(self.count) + '}';
    def __repr__(self):
        return str(self);

def contains_in(a, b):
    '''check whether tuple a is in tuple b'''
    return set(a).issubset(set(b));

def gen_candidate_itemsets_for_group(group):
    '''generate candidate itemsets for a group of itemsets whose items only differ in the last item'''
    k = len(group[0].items) + 1;
    candidate_itemsets = list();
    for itemset_a in group:
        for itemset_b in group:
            if itemset_a.items[k - 2] < itemset_b.items[k - 2]:
                candidate_itemsets.append(Itemset(itemset_a.items[:k - 1] + (itemset_b.items[k - 2],)));
    return candidate_itemsets;

def gen_candidate_itemsets(itemsets):
    '''generate candidate itemsets
    This function actually doing the "SELECT" in the paper 2.1.1
    '''
    if len(itemsets) == 0:
        return list();
    #use sorting to group itemsets that has the same prefix items together
    itemsets = sorted(itemsets, key=lambda x:x.items);
    candidate_itemsets = list();
    group = list();
    previous = None;
    k = len(itemsets[0].items);
    for itemset in itemsets:
        if previous is None or previous.items[:k - 1] == itemset.items[:k - 1]:
            #if this one and previous one's items are the same except the last item, they are in the same group
            group.append(itemset);
        else:
            #now we have found all members of the group whose items only differ in the last item
            #generate all candate itemsets based on that group
            candidate_itemsets.extend(gen_candidate_itemsets_for_group(group));
            #start a new group
            group = [itemset];
        previous = itemset;
    if len(group):
        #still one group left
        candidate_itemsets.extend(gen_candidate_itemsets_for_group(group));
    itemsets = set(itemsets);
    def check(candidate_itemset):
        '''pruning function, False if need to be pruned'''
        for i in range(len(candidate_itemset.items)):
            subset = Itemset(candidate_itemset.items[0:i] + candidate_itemset.items[i + 1:]);
            if subset not in itemsets:
                return False;
        return True;
    #pruning
    candidate_itemsets = filter(check, candidate_itemsets);
    return candidate_itemsets;

def main(csv_file_name, min_sup, min_conf):
    '''The main function for a-priori algorithm'''
    output_file_name = 'output.txt';
    output_file = open(output_file_name, 'w');

    #Read the file and make sure each transitions are sorted
    rows = list();
    with open(csv_file_name, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(list(row));
    rows = [sorted(set(row)) for row in rows];
    transitions = tuple(rows);

    #now, find the frequent iterms
    n = len(transitions);
    import collections
    counter = collections.Counter();
    for transition in transitions:
        counter.update(transition);
    init_itemsets = list();
    for item, count in counter.iteritems():
        if count >= n * min_sup:
            init_itemsets.append(Itemset((item,), count));

    L = list();
    L.append(init_itemsets);
    k = 1;
    done = False;
    while not done:
        # get candidate itemsets
        candidate_itemsets = gen_candidate_itemsets(L[k - 1]);
        # counting the appearance of each candidate_itemsets
        for transition in transitions:
            for candidate_itemset in candidate_itemsets:
                if contains_in(candidate_itemset.items, transition):
                    candidate_itemset.count += 1;

        # find out all the candidate_itemsets that are frequent
        new_frequent_itemsets = list();
        for candidate_itemset in candidate_itemsets:
            if candidate_itemset.count >= min_sup * n:
                new_frequent_itemsets.append(candidate_itemset);
        if len(new_frequent_itemsets) == 0:
            # There is no new frequent_items, done.
            done = True;
        else:
            L.append(new_frequent_itemsets);
        k += 1;

    frequent_itemsets = [frequent_itemset for itemsets in L for frequent_itemset in itemsets];

    #Sort the frequent itemsets based on the decreasing order of the frequency.
    frequent_itemsets = sorted(frequent_itemsets, key=lambda x:(-x.count, x.items));

    #Output frequent itemsets.
    print '==Frequent itemsets (min_sup=%d%%)'%(min_sup * 100);
    print >>output_file, '==Frequent itemsets (min_sup=%d%%)'%(min_sup * 100);
    for frequent_itemset in frequent_itemsets:
        print '[' + ','.join(frequent_itemset.items) + ']' + ', %d%%'%(frequent_itemset.count * 100 / n);
        print >> output_file, '[' + ','.join(frequent_itemset.items) + ']' + ', %d%%'%(frequent_itemset.count * 100 / n);

    #Calculate association rules
    rules = list();
    for frequent_itemset in frequent_itemsets:
        if len(frequent_itemset.items) > 1:
            for position, right in enumerate(frequent_itemset.items):
                #Get the left part of the rules
                left_set = list(frequent_itemset.items);
                del left_set[position];

                #Get the count of the left part
                left_count = sum((contains_in(left_set, transition) for transition in transitions));

                #calculate the confidence
                conf = float(frequent_itemset.count) / left_count;
                #check if it satisfies the condition
                if conf >= min_conf:
                    rules.append((left_set, right, conf, float(frequent_itemset.count) / n));
    # output the association rules
    rules = sorted(rules, key=lambda x:(-x[2]))
    print
    print >> output_file;
    print '==High-confidence association rules (min_conf=%d%%)'%(min_conf * 100);
    print >> output_file, '==High-confidence association rules (min_conf=%d%%)'%(min_conf * 100);
    for rule in rules:
        print '[%s] => [%s] (Conf: %.1f%%, Supp: %d%%)'%(','.join(rule[0]), rule[1], rule[2] * 100, rule[3] * 100);
        print >> output_file, '[%s] => [%s] (Conf: %.1f%%, Supp: %d%%)'%(','.join(rule[0]), rule[1], rule[2] * 100, rule[3] * 100)

if __name__ == '__main__':
    import sys
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]));
