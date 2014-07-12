"""
Main helper methods for accessing OSB API

"""

import sys
import utils

try:
    from urllib2 import urlopen, HTTPError, Request  # Python 2
except:
    from urllib.request import urlopen, HTTPError, Request # Python 3

import base64
import json
import os.path
import subprocess

import Project#from Project import *

USERNAME = None
PASSWORD = None
auth_file = "github.info"

auth_info = "\n-----------------------------------------------------------------\n\n"+\
            "  GitHub limits the number of calls to its API for unauthorised users (~60 per hour).\n"+\
            "  For registered GitHub users, this goes up to ~5000 per hour. To use your GitHub account\n"+\
            "  details, either create a file "+auth_file+" containing the lines:\n\n    username:YOUR_USERNAME\n    password:YOUR_PASSWORD\n\n"+\
            "  or call with commandline arguments, e.g.:\n"+\
            "\n    python curate.py username:YOUR_USERNAME and password:YOUR_PASSWORD\n\n"+\
            "-----------------------------------------------------------------"

for arg in sys.argv[1:]:
    try:
        key,value = arg.split(":")
        if key == "username":            
            USERNAME = value
        if key == "password":
            PASSWORD = value
    except ValueError as e:
        ignored_arg = arg

if os.path.isfile(auth_file):
    for line in open(auth_file, 'r'):
        if line.startswith("username:"):
            USERNAME = line.strip()[9:]
        if line.startswith("password:"):
            PASSWORD = line.strip()[9:]
            
            
        

def get_project_array(min_curation_level, limit=1000):
    url = "http://www.opensourcebrain.org/projects.json"
    page = utils.get_page('%s?limit=%d' % (url,limit))
    json_data = json.loads(page)
    project_list_all = json_data['projects']
    project_list = []
    for project in project_list_all:

        curation_level = int(utils.get_custom_field(project, "Curation level")) if utils.get_custom_field(project, "Curation level") else 0
        
        if (min_curation_level=="None") or \
           (min_curation_level=="Low" and curation_level>=1)  or \
           (min_curation_level=="Medium" and curation_level>=2)  or \
           (min_curation_level=="High" and curation_level>=3):
            project_list.append(project)
            
    return project_list


def get_projects(min_curation_level, limit=1000):
    url = "http://www.opensourcebrain.org/projects.json"
    page = utils.get_page('%s?limit=%d' % (url,limit))
    json_data = json.loads(page)
    project_list_all = json_data['projects']
    projects = []
    for project in project_list_all:
        
        curation_level = int(utils.get_custom_field(project, "Curation level")) if utils.get_custom_field(project, "Curation level") else 0
        
        if (min_curation_level=="None") or \
           (min_curation_level=="Low" and curation_level>=1)  or \
           (min_curation_level=="Medium" and curation_level>=2)  or \
           (min_curation_level=="High" and curation_level>=3):
            projects.append(Project(project))
            
    return projects


def get_project(project_identifier):
    
    url = "http://www.opensourcebrain.org/projects/%s.json"%project_identifier
    page = utils.get_page('%s' % (url))
    json_data = json.loads(page)
    return Project.Project(json_data['project'])
            

def known_external_repo(reponame):
    if "openworm" in reponame or \
       "neuralgorithm" in reponame or \
       "Simon-at-Ely" in reponame:
        return True
    else:
        return False
