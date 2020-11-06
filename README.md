# Coffee Partner Lottery
A small project from Covid-19 times, for generating random pairings of people who can have a virtual chat and coffee together. The Python script in this repo takes care of the generation, my whole process for the lottery is as follows: 

1. Let interested people sign up. I used MS Forms for the Coffee Partner Lottery at UU's Department of Information and Computing Sciences, but Google Forms or another similar tool will also do. You can download the responses in the form of a CSV file, which is the input for the Python script.  
2. Run the Python script to generate a set of pairs. It will store all pairs ever generated in another CSV file (all_pairs.csv), to keep track of already generated pairs and thus making sure that new people meet each time. The new set of pairs is written to a separate CSV file (new_pairs.csv). 
3. Use Thunderbird's MailMerge plugin to automatically generate e-mails with the information from new_pairs.csv, to inform people that they have been paired. I haven't tried, but probably MS Outlook and other e-mail clients have similar functionality. 
