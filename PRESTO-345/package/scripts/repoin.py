import os
import re
import commands

#list all repofiles
def ListFiles(dirPath):  
 fileList = []
 for root, dirs, files in os.walk(dirPath):         
  for fileObj in files:  
   fileList.append(os.path.join(root, fileObj))  
 return fileList  

#search repofile
def FindString(filePath, regex): 
 fileObj = open(filePath, 'r')  
 for eachLine in fileObj:   
  if re.search(regex, eachLine, re.I):  
    return fileObj.name
    break
    os.system("pause")

try:
 finalRepofile = ''
 mycommand_repo = "yum --disablerepo '*' --enablerepo  'HD*' info zookeeper | grep 'Repo'"
 repo = commands.getoutput(mycommand_repo)
 repo_tmp = repo.split('Repo        :')[1]
 repo_id = repo_tmp.strip() 
 fileList = ListFiles('/etc/yum.repos.d/') 
 regex = "name="+repo_id
 repoFile = ''
 for fileObj in fileList: 
  repoFile = FindString(fileObj, regex)
  if repoFile is not None:
   finalRepofile = repoFile
except:
 baseurl=''
 print "Repoin Error: No matching Repofiles to list"
else:
 mycommand_url = "cat " + finalRepofile + "| grep 'baseurl'| head -n 1"
 (n,url)=commands.getstatusoutput(mycommand_url)
 baseurl=url.split("=")[1]
 print "Repoin INFO:baseurl="+baseurl
