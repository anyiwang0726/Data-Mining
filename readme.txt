
Explanation of Datasets:

(a) 
    NYC Open Data set used: NYPD Motor Vehicle Collisions, which concludes the detailed information of vehicle collisions in New York City from 2012 to 2015 on daily basis. 
(b) 
    Data Analysis:
    ** Drop all NaN rows of the original file, skip cells with "NaN" values;
    ** Drop column names and unique keys from the original data file.
    ** Bucketize the hour/minute/second time into morning(before 12pm), afternoon(before 18pm) and evening(before 12am);
    ** Add descriptions to line values to make the market value readable. For example, change "1" in "NUMBER OF PERSONS INJURED" into "Num_injur=1";
    ** Skip the "0" value from the original csv files. This is because we are more interested in what happened during/before the car accident than what did not happen at that time;
    ** Since the number_of_motor_injured and num_of_pedestrain_injured are highly correlated with the total number of injury, we delete these columns. In other words, we expect the mining techniques to help us find relations aside from obvious ones. Similar application has been applied to zip code and borough. 
  % We implemented the cleaning and mapping of data using Pandas. We can provide it upon request.

(c) 
    The NYPD Motor Vehicle Collisions include a very detailed information about all the collisions in NYC during the past 3 years. Studying the time/location/responsibilities/consequences these huge dataset help us to understand more about where does collisions happen mostly in time and in certain spot. e.g. Brooklyn is having car collisions in the morning most possibly at the Wilson Ave. 
    High-confidence association rules is also very helpful in the study of this case. e.g. Given a collision report at certain time and place, what is the confidence that certain kind of vehicle can be responsible.(This can be used to deduct the CONTRIBUTING FACTOR VEHICLE for hit and run) 
    Getting the information of "frequent items", we can increase the awareness of passengers and drivers in certain district. In addition, we can increase the number of police staffs at "frequent collision spot" or establish more signs and logos at these places. 
    Getting the information of "High-confidence association rules", we can infer a contributing factor vehicle for hit and run, or use it as a reference when handling arguments and inconsistency between drivers.

 How to run:
    
    python main.py inputfile min_sup min_conf
    e.g. python main.py data.csv 0.1 0.9
    data.csv is the input file
    0.1 is the minimum support
    0.9 is minimum confidence

 The main.py has the following functions:
    contains_in(a, b)
        check whether tuple a is in tuple b
    gen_candidate_itemsets_for_group(group)
        generate candidate itemsets for a group of itemsets whose items only differ in the last item
    gen_candidate_itemsets(itemsets)
        generate candidate itemsets, this function actually do the "SELECT" in the paper 2.1.1
    main(csv_file_name, min_sup, min_conf):
        the main function for a-priori algorithm

 The main process:
        1. Read the transitions from input file and make sure each transitions are sorted
        2. Find the frequent items and use them to build the initial frequent itemsets
        3. Generate candidate itemsets from previous frequent itemsets:
            3.1 Sort all previous frequent itemsets based on their items
            3.2 Group all the previous frequent itemsets whose items only differ in the last item
            3.3 For each group, generate candidate itemsets.
            3.4 Pruned out the candidate itemsets that has a k - 1 subset not in the k - 1 frequent itemsets.
        4. Counting the frequency of each candidate itemsets
        5. Find all the candidate itemsets that are frequent
        6. If there is no new frequent itemsets, then goto 7, else goto 3
        7. Sort and output all the frequent itemsets.
        8. For each frequent itemset, generate all possible association rules that have only one right hand side item.
            Check whether the confidence of the rule is higher than the min_conf, if true, store it.
        9. Output all stored association rules.

The list is long and here are several few interesting findings:
   1) Frequent Items:
     1. Among all the traffic accidents, passenger vehicle has been a major involver, followed by sport utility/station wagon.
     [PASSENGER VEHICLE], 87%
     [SPORT UTILITY / STATION WAGON], 53%

     2. More traffic collisions happen in afternooon, followed by that in the morning.
     [Afternoon], 54%
     [Morning], 45%

     3. Brooklyn has more traffic collisions than Queens, followed by Brnox.
     [BROOKLYN], 42%
     [QUEENS], 29%
     [BRONX], 14%

   2) High-Confidence Associations:
    0. It is trivial that whenever there is a collision, it is very likely that passenger vehicle was involved.
      [MANHATTAN] => [PASSENGER VEHICLE] (Conf: 86.8%, Supp: 8%)
      [Afternoon] => [PASSENGER VEHICLE] (Conf: 86.8%, Supp: 47%)
      [Afternoon,Num_injur=1] => [PASSENGER VEHICLE] (Conf: 91.9%, Supp: 12%)

    1. Whenever there is an accident caused by driver inexperience, alcohol involvement, Driver Inattention, etc, it is most likely to be a passenger vehicle. We shall pay more attention on the education and training of passenger vehicle drivers. Meanwhile, Sport Utility/Station Wagon tends to fail to keep right during the driving or disregard the traffic control. 
     [Driver Inexperience] => [PASSENGER VEHICLE] (Conf: 96.9%, Supp: 2%)
     [Alcohol Involvement,QUEENS] => [PASSENGER VEHICLE] (Conf: 95.5%, Supp: 3%)
     [Aggressive Driving/Road Rage] => [PASSENGER VEHICLE] (Conf: 90.5%, Supp: 1%)
     [Driver Inattention/Distraction,Num_injur=1] => [PASSENGER VEHICLE] (Conf: 100.0%, Supp: 1%)
     [Pavement Slippery] => [PASSENGER VEHICLE] (Conf: 88.9%, Supp: 1%)
     [Failure to Keep Right] => [SPORT UTILITY / STATION WAGON] (Conf: 77.8%, Supp: 1%)
     [Failure to Keep Right] => [SPORT UTILITY / STATION WAGON] (Conf: 77.8%, Supp: 1%)


    2. If a van is involved in a vehicle collision in Queens, it is more likely to be in the afternoon and with collision between passenger vehicle or sport utility/station wag. We can set up bigger signs during the afternoon in Queens to aware people of driving safety.
     [QUEENS,VAN] => [Afternoon] (Conf: 77.8%, Supp: 1%)
     [QUEENS,VAN] => [PASSENGER VEHICLE] (Conf: 77.8%, Supp: 1%)
     [QUEENS,VAN] => [SPORT UTILITY / STATION WAGON] (Conf: 77.8%, Supp: 1%)

    3. Drivers tend to fail to disoeby the traffic rules more in the afternoon. While Small Com Veh tend to be more likely to involve in a collision in the morning.
     [Driver Inattention/Distraction] => [Afternoon] (Conf: 63.9%, Supp: 5%)
     [Failure to Yield Right-of-Way] => [Afternoon] (Conf: 73.9%, Supp: 2%)
     [Traffic Control Disregarded] => [Afternoon] (Conf: 63.2%, Supp: 4%)
