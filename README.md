# Jenkins-EC2
## Requirment: To deploy a python flask web application to a EC2 instance  
## 

## Pre-requiste  
(1) Install Jenkins and install below plugins in jenkins  
* AWS Steps Plugin - provides pipeline steps for interacting with Amazon Web Services (AWS).  
* Pipeline AWS Plugin - provides a pipeline step to create and manage AWS CloudFormation stacks.  
* Jenkins Credentials Plugin - provides a way to securely store credentials (e.g., AWS access keys) that can be used by Jenkins jobs.  
* Pipeline Utility Steps Plugin - provides various utility steps for pipelines.  
* Pipeline Stage View Plugin - provides a graphical view of pipeline stages.  

## Steps  
(1) Create a pipeline in Jenkins and pprovide the SCM details to capture Jenkinfile from this git to Jenkins  
(2) Pass the neccessary details such as AMI ID, Security Group, Instance Type and other details  
(3) Create S3 bucket and upload 'app.py' and 'index.html'
(4) Build the Jenkins pipeline jobs  

## Note
* Create user in AWS and create Access Key, create new credentials in jenkins and provide the Access Key and Secret Key.  
* Make sure to create role and attach it to the jenkins user to run SSM commands from Jenkins Script.  
* Create role for 'SSM Managed Core' and attach it to the EC2 instance (Pass it via Parameters)
* Sleep is added so that the instance to be added as part of SSM managed instance, only then instance can execute shell commands from Jenkins.
