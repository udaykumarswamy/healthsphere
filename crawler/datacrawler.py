#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 15:27:47 2024

@author: uday_kumar_swamy
"""
import requests 
import warnings
import logging
import logging.config
import os
from bs4 import BeautifulSoup
import configparser
warnings.filterwarnings('ignore')

# Read the properties file
config = configparser.ConfigParser()
config.read('config.properties')

logConf = config.get('LogFile', 'logConfiguration')
downloadPath = config.get('download','downloadPath')
url = config.get('url','sourceUrl')

logging.config.fileConfig(logConf)
logger = logging.getLogger('healthsphere')



def crawlUrls(url):
    """
    Crawls a webpage for URLs containing 'health-topics/'.

    Args:
        url (str): The URL of the webpage to crawl.

    Returns:
        list: A list of URLs containing 'health-topics/'.
    """
    logger.info("crawling started...")
    pdf_urls = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if 'health-topics/' in str(href):
                    pdf_urls.append(href)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    logger.info("crawling is completed...")
    return pdf_urls


def downLoadThePages(pdf_urls,download_dir):
    """
    Downloads PDF files from a list of URLs and saves them to the specified directory.

    Args:
        pdf_urls (list): A list of URLs to download PDF files from.
        download_dir (str): The directory to save the downloaded PDF files.

    Returns:
        None
    """
    logger.info('downloading the each disease details started...')
    for pdf_url in pdf_urls:
        filename = os.path.join(download_dir, pdf_url.split('/')[-1])
        try:
            response = requests.get('https://www.niams.nih.gov'+pdf_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if '/pdf/' in str(href):
                        response = requests.get('https://www.niams.nih.gov'+href)
                        with open(filename+'.pdf', 'wb') as f:
                            f.write(response.content)
        except Exception as e:
            logger.info('ignore certification')
    logger.info('downloading the each disease details completed...')
 

download_dir = downloadPath
pdf_urls = crawlUrls(url)
downLoadThePages(pdf_urls, download_dir)