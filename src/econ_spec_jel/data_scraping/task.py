""" Task functions for data scraping. """
# write a loop over the two tasks and pass the number to each of them?
# how else could I achieve parallelization/be sure not to need to re-run them all?

def task_scrape_metadata():
    # base url: https://www.iza.org/publications/dp/[number]
    # numbers range from 1 to 17,628 (as of 21.01.2025)
    # there only 17,622 papers though
    # for each scrape, author(s), month, year, title, abstract, keywords, jel codes
    return None

def task_scrape_paper():
    # base url: https://docs.iza.org/dp[number].pdf
    # download the pdf file
    return None