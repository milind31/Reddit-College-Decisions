# -*- coding: utf-8 -*-
#Last edited on 9/17/2019, Milind Rajavasireddy
#necessary libraries
import urllib.request
from bs4 import BeautifulSoup
import re
import numpy as np
import matplotlib.pyplot as plt

#scrape reddit page
ucd_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/aync6m/official_2019_university_of_california_davis/?limit=500", "https://old.reddit.com/r/ApplyingToCollege/comments/83b3cn/uc_davis_stats_thread/?limit=500", "https://old.reddit.com/r/ApplyingToCollege/comments/835n7c/uc_davis_decision_megathread/"]
#ucla_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b3tyrj/official_2019_university_of_california_los/?limit=500"]
#usc_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b3eemc/official_2019_university_of_southern_california/?limit=500"]
#mit_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/84gzgb/mit_statsdecisions_separate_megathread/?limit=500"]
#caltech_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/ayztkb/official_2019_california_institute_of_technology/?sort=new"]
#ucb_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b5mcup/official_2019_university_of_california_berkeley/?limit=500"]
#brown_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b5uqbs/official_2019_brown_university_megathread/?sort=new"]
#upenn_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b5uqki/official_2019_university_of_pennsylvania/?sort=new"]
#columbia_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b5uq26/official_2019_columbia_university_megathread/?sort=new"]
#cornell_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b5ur0q/official_2019_cornell_university_megathread/?sort=new"]
#yale_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b5up4c/official_2019_yale_university_megathread/?sort=new"]
#harvard_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b5uovg/official_2019_harvard_university_megathread/?sort=new"]
#uchicago_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b09yc2/official_2019_university_of_chicago_megathread/?sort=new"]
#stanford_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b6dkt0/official_2019_stanford_university_megathread/?sort=new"]
#georgiatech_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/ayzu23/offical_2019_georgia_institute_of_technology/?sort=new"]
#jhu_urls = ["https://old.reddit.com/r/ApplyingToCollege/comments/b0fp4u/official_2019_johns_hopkins_university_megathread/?sort=new"]
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
extracted_comments = []
def scrape():
    #replace with respective college_urls
    for url in ucd_urls:
        request = urllib.request.Request(url,headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(request).read()           
        soup = BeautifulSoup(html,'html.parser')
        comment_area = soup.find('div',attrs={'class':'commentarea'})
        comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})
        for comment in comments: 
            if comment.find('form'):
                comment_text = comment.find('div',attrs={'class':'md'}).text
                extracted_comments.append(comment_text)

#initialize arrays
satscores = []
statsdupe = []
stats = []
inputsdupe = []
inputs = []
outputsdupe = []
outputs = []
acceptedtestscores = []
accepteduwgpa = []
rejectedtestscores = []
rejecteduwgpa = []
waitlistedtestscores = []
waitlisteduwgpa = []

#define simple for loop with custom start, end, and step
def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

#go through each comment and find keywords/all numbers
def cleanData():
    for item in extracted_comments:
        numberset = re.findall('\d*\.?\d+',item)
        #determine whether the user was admitted, denied, or waitlisted. The use of statusarray is in the case the user mentioning multiple keywords in the same comment. We want to take the first keyword mentioned as that is almost always the actual result.
        statusarray = []
        status = 100
        accepted_cap = re.search("Accepted", item)
        accepted = re.search("accepted", item)
        accepted_allcaps = re.search("ACCEPTED", item)
        if accepted or accepted_cap or accepted_allcaps:
            status = 1
            statusarray.append(status)
        rejected_cap = re.search("Rejected", item)
        rejected = re.search("rejected", item)
        denied_cap = re.search("Denied", item)
        denied = re.search("denied", item)
        if rejected or denied or rejected_cap or denied_cap:
            status = 0
            statusarray.append(status)
        waitlisted_cap = re.search("Waitlisted", item)
        waitlisted = re.search("waitlisted", item)
        if waitlisted or waitlisted_cap:
            status = 2
            statusarray.append(status)
        if len(statusarray) >= 1:
                status = statusarray[0]
        #find and separate test scores/gpas. similar to with the status, we want to find the first number that has a decimal and is in the range of possible gpas as that is usually the correct gpa (users often write their gpas in the format of "gpa/max possible gpa". This is not necessary for test scores because users rarely include multiple numbers in test score range in their comments.
        potential_uwgpas = []
        uwgpa = 100
        sat = 7
        for number in numberset:
            for potentialact in my_range(21, 36, 1):
                if float(number) == potentialact:
                    act = potentialact
                    #act scores are converted to sat using the official 2018 act/sat concordance table
                    sat_conversion_array = [1080, 1110, 1140, 1180, 1210, 1240, 1280, 1310, 1340, 1370, 1400, 1430, 1460, 1500, 1540, 1590]
                    sat = sat_conversion_array[act - 21]
            #sat scores are found after act scores because we would prefer actual sat scores to converted act scores
            for potentialsat in my_range(1100, 1600, 10):
                if float(number) == potentialsat:
                    sat = potentialsat
            if float(number) > 3 and float(number) <= 4:
                if '.' in str(number):
                    potential_uwgpas.append(float(number))
                if len(potential_uwgpas) >= 1:
                    uwgpa = potential_uwgpas[0]
        if float(uwgpa) != 100 and status != 100 and sat > 1100:
            statsdupe.append([sat, uwgpa, status])   
    #remove all duplicates
    for j in statsdupe:
      if j not in stats:
         stats.append(j)


def prepareForPlotting():
    #separate stats into categories for plotting
    for stat in stats:
        if stat[2] == 1:
            acceptedtestscores.append(stat[0])
            accepteduwgpa.append(float(stat[1]))
        if stat[2] == 0:
            rejectedtestscores.append(stat[0])
            rejecteduwgpa.append(float(stat[1]))
        if stat[2] == 2:
            waitlistedtestscores.append(stat[0])
            waitlisteduwgpa.append(float(stat[1]))
    p = 0
    while p < len(stats):
        array = []
        array = np.asarray(stats[p])
        sat = array[0]
        gpa = array[1]
        status = array[2]
        if status !=2:
            inputs.append([int(sat), gpa])
            outputs.append(int(status))
        p = p + 1

def plot():
    plt.scatter(accepteduwgpa, acceptedtestscores, color='g')
    plt.scatter(rejecteduwgpa, rejectedtestscores, color='r')
    #plt.scatter(waitlisteduwgpa, waitlistedtestscores, color='b')
    plt.xlabel('Unweighted GPA')
    plt.ylabel('SAT Score')
    plt.show()

scrape()
cleanData()
prepareForPlotting()
plot()
