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
warnings.filterwarnings('ignore')




logging.config.fileConfig('temp.conf')
logger = logging.getLogger('healthsphere')
os.mkdir('/Users/uday_kumar_swamy/Documents/work/spring-2024/IR/IR_project/HealthSphere/healthdata')


def crawlUrls(url):
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
            #print(f"Failed to download {pdf_url}: {e}")
            logger.info('ignore certification')
    logger.info('downloading the each disease details completed...')
 
url = "https://www.niams.nih.gov/health-topics/all-diseases"
download_dir = "/Users/uday_kumar_swamy/Documents/work/spring-2024/IR/IR_project/HealthSphere/healthdata"
pdf_urls = crawlUrls(url)
downLoadThePages(pdf_urls, download_dir)