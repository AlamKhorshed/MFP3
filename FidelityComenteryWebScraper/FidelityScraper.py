#!/usr/bin/env python
"""
Fidelity Funds Quarterly Commentary Scraper

NOTE: In order to use this program, be sure to create a directory
called 'Comentery'.
Also, be sure to install Selenium Webdriver and gracodriver.
Please check requirement.txt

"""
##########################################################################
## Imports
##########################################################################

import os
import json
import time
from selenium import webdriver


##########################################################################
## Module Variables/Constants
##########################################################################

FIDELITY_COMMENTARY_BAE_URL = 'https://www.fidelity.com/mutual-funds/information/fidelity-fund-quarterly-commentary'



##########################################################################
## Functions
##########################################################################
def fetch_fund_urls():
    """
    Performs a GET on the Fidelity-Fund-Quarterly-Commentary home and returns
    an array of URIs of the available funds
    """
    url_list = []


    # initialize the webdriver
    driver1 = webdriver.Firefox()
    # execute a GET request
    driver1.get(FIDELITY_COMMENTARY_BAE_URL)
    #css selector for grabbing the individual fund names and hyperlinks
    urls = driver1.find_elements_by_css_selector('div.tabs--content > div > div > div > div > div > ul > li > a')

    #iterate throught the urls and get the name and href
    for url in urls:
        url_list.append(url.get_attribute("href"))

    #close the Firefox driver
    driver1.close()
    # return the 'url_list' array
    return url_list


def fetch_fund_details(url):
    """
    Performs a GET on the individual Fidelity fund, scraps data and returns
    a list of those elemenents. CSS selector is used to navigate through the html
    """
    fund_details = {}


    # initialize the webdriver
    driver2 = webdriver.Firefox()
    # execute a GET request
    driver2.get(url)
    driver2.implicitly_wait(15)

    fund_details['url'] = url

    #css selector for grabbing the symbol
    symbol = driver2.find_element_by_css_selector('li.hide-in-980:nth-child(3) > a:nth-child(1)')
    fund_details['symbol'] = symbol.get_attribute("href").split("=")[-1]

    #css selector for grabbing the title
    title = driver2.find_element_by_css_selector('h1.header-container--heading')
    fund_details['title'] = title.text


    #########################################
    ### MorningStar info#####################
    #########################################

    morningStartRatingInfo = {}

    #OverallRating
    overallRating = driver2.find_elements_by_css_selector('div.ratingImg-container:nth-child(2) > img:nth-child(1)')
    morningStartRatingInfo['OverallRating'] = overallRating[0].get_attribute("title")

    #Returns
    returns = driver2.find_elements_by_css_selector('#morning-rating-2 > div:nth-child(2) > div:nth-child(1) > img:nth-child(1)')
    morningStartRatingInfo['Returns'] = returns[0].get_attribute("alt")

    #Expenses
    expenses = driver2.find_elements_by_css_selector('#morning-rating-3 > div:nth-child(2) > div:nth-child(1) > img:nth-child(1)')
    morningStartRatingInfo['Expenses'] = expenses[0].get_attribute("alt")

    #Risks
    risks = driver2.find_elements_by_css_selector('#morning-rating-4 > div:nth-child(2) > div:nth-child(1) > img:nth-child(1)')
    morningStartRatingInfo['Risks'] = expenses[0].get_attribute("alt")

    fund_details['MorningStartRatingInfo'] = morningStartRatingInfo

    ##########################################################
    ### Performance info: Average Annual Return (AAR)#########
    ##########################################################

    performanceInfo = {}

    # YTD
    aarYTD = driver2.find_element_by_css_selector('.mfl-performance-table--data-left-container > p:nth-child(2)')
    #positiveNegativeIndicator = driver2.find_element_by_css_selector('.mfl-performance-table--data-left-container > p:nth-child(2) > span:nth-child(1)')
    performanceInfo['AverageAnnualReturnYTD'] = aarYTD.text

    # 1 Year
    oneYTD = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(2) > p:nth-child(2)')
    #positiveNegativeIndicator = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(2) > p:nth-child(2) > span:nth-child(1)')
    performanceInfo['AverageAnnualReturn1Y'] = oneYTD.text

    # 3 Years
    threeYTD = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(3) > p:nth-child(2)')
    #positiveNegativeIndicator = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(3) > p:nth-child(2) > span:nth-child(1)')
    performanceInfo['AverageAnnualReturn3Y'] = threeYTD.text

    # 5 Years
    fiveYTD = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(4) > p:nth-child(2)')
    #positiveNegativeIndicator = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(4) > p:nth-child(2) > span:nth-child(1)')
    performanceInfo['AverageAnnualReturn5Y'] = fiveYTD.text

    #10 Years
    tenYTD = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(5) > p:nth-child(2)')
    #positiveNegativeIndicator = driver2.find_element_by_css_selector('div.mfl-performance-table--data-right-ind:nth-child(5) > p:nth-child(2) > span:nth-child(1)')
    performanceInfo['AverageAnnualReturn10Y'] = tenYTD.text

    fund_details['PerformanceInfo'] = performanceInfo

    ##########################################################
    ### Quarterly Fund Review#################################
    ##########################################################
    quarterlyFundReview = {}

    #PerformanceReviewDate
    performanceReviewDate = driver2.find_element_by_css_selector('#shcomm-QuarterlyFundReviewDate')
    quarterlyFundReview['PerformanceReviewDate'] = performanceReviewDate.text

    #PerformanceReview
    paragraphs = driver2.find_elements_by_css_selector('#shcomm-QuarterlyFundReviewTopContent > p')
    quarterlyFundReview['PerformanceReview'] = ''.join (str(paragraph.text) for paragraph in paragraphs)

    #OutlookAndPositioning
    outlooks = driver2.find_elements_by_css_selector('#shcomm-QuarterlyFundReviewBottomContent1 > p')
    quarterlyFundReview['OutlookAndPositioning'] = ''.join (str(outlook.text) for outlook in outlooks)

    fund_details['QuarterlyFundReview'] = quarterlyFundReview

    ##########################################################
    ### Portfolio Managers Q&A################################
    ##########################################################
    portfolioManagerQA = {}

    driver2.get(url+'?documentType=QAA')
    driver2.implicitly_wait(15)

    #PortfolioManagersReviewDate
    try:
        portfolioManagersReviewDate = driver2.find_element_by_css_selector('#shcomm-PortfolioManagersQuestionAnswerDate')
        portfolioManagerQA['PortfolioManagersReviewDate'] = portfolioManagersReviewDate.text
    except:
        pass

    #KeyTakeaway
    try:
        takeaways = driver2.find_elements_by_css_selector('#shcomm-PortfolioManagersQuestionAnswerKeyContentBody > ul:nth-child(1) > li')
        portfolioManagerQA['KeyTakeaway'] = ''.join (str(takeaway.text) for takeaway in takeaways)
    except:
        pass

    #PortfolioManagersPlan
    try:
        portfolioManagersPlans = driver2.find_elements_by_css_selector('#shcomm-PortfolioManagersQuestionAnswerInvestmentsContentBody > p')
        portfolioManagerQA['PortfolioManagersPlan'] = ''.join (str(portfolioManagersPlan.text) for portfolioManagersPlan in portfolioManagersPlans)
    except:
        pass

    fund_details['PortfolioManagerQA'] = portfolioManagerQA


    #close the Firefox driver
    driver2.close()

    # return the 'results' array of press releases
    return fund_details


def main():
    """
    Main execution function to perform required actions
    """
    # fetch array of fund urls
    fund_urls = fetch_fund_urls()

    # iterate funds and save in the json file under FidelityFundCommentary direcory
    for url in fund_urls:
        print(url)
        #print(fetch_fund_details(url))
        commentery = fetch_fund_details(url)
        #break

        path = 'Comentery/%s.json' % commentery['symbol']
        content = json.dumps(commentery, indent=4, sort_keys=True)

        f = open(path, 'wb')
        f.write(content.encode('utf-8'))
        f.close()
        time.sleep(10)


##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()
