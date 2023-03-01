pipeline {
    agent any
    
    parameters {
        string(name: 'instance_type', defaultValue: 't2.micro', description: 'EC2 instance type')
        string(name: 'ami_id', defaultValue: 'ami-0dfcb1ef8550277af', description: 'AMI ID for EC2 instance')
        string(name: 'security_group_id', defaultValue: 'sg-06b5ddd3fd4dddeb5', description: 'Security group ID for EC2 instance')
        string(name: 'subnet_id', defaultValue: 'subnet-0080869bb3e15b32b', description: 'Subnet ID for EC2 instance')
        string(name: 'INSTANCE_PROFILE_NAME', defaultValue: 'EC2-SSMCore', description: 'Name of the IAM instance profile to associate with the EC2 instance')
        string(name: 's3_bucket', defaultValue: 'ec2-insta-001', description: 'Name of S3 bucket containing image file')
        string(name: 's3_key', defaultValue: 'coffee.jpg', description: 'S3 key of image file')
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'pip install boto3'
                sh 'pip install flask'
                sh 'python -m compileall app.py'
            }
        }
        
        stage('Create Instance') {
            steps {
                withCredentials([[
	                $class: 'AmazonWebServicesCredentialsBinding',
	                credentialsId: 'aws-cred',
	                accessKeyVariable: 'AWS_ACCESS_KEY_ID',
	                secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
                {
                sh "aws ec2 run-instances --image-id ${params.ami_id} --instance-type ${params.instance_type} --subnet-id ${params.subnet_id} --security-group-ids ${params.security_group_id} --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=hello-instance}]'"
                sh 'sleep 50'
		sh 'pip install awscli'
		sh 'aws ec2 describe-instances --filters "Name=tag:Name,Values=hello-instance" --filters "Name=instance-state-name,Values=running" --query "Reservations[0].Instances[0].InstanceId" --output text > instance_id.txt'
		sh 'aws ec2 associate-iam-instance-profile --instance-id $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --iam-instance-profile Name=$INSTANCE_PROFILE_NAME'
                }
            }
        }
        
        stage('Deploy') {
            steps {
		withCredentials([[
	                $class: 'AmazonWebServicesCredentialsBinding',
	                credentialsId: 'aws-cred',
	                accessKeyVariable: 'AWS_ACCESS_KEY_ID',
	                secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
		{
                sh 'sleep 300'
		sh 'aws ssm send-command --instance-ids $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --document-name "AWS-RunShellScript" --parameters '\''commands=["aws s3 cp s3://${params.s3_bucket}/${params.s3_key} image.jpg"]'\'''
		sh 'aws ssm send-command --instance-ids $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --document-name "AWS-RunShellScript" --parameters '\''commands=["aws s3 cp s3://${params.s3_bucket}/app.py ."]'\'''
		sh 'aws ssm send-command --instance-ids $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --document-name "AWS-RunShellScript" --parameters '\''commands=["aws s3 cp s3://${params.s3_bucket}/template/index.html templates"]'\'''
//                sh "aws s3 cp s3://${params.s3_bucket}/${params.s3_key} image.jpg"
//                sh "aws s3 cp s3://${params.s3_bucket}/app.py ."
//                sh "aws s3 cp s3://${params.s3_bucket}/template/index.html templates/"
		sh 'aws ssm send-command --instance-ids $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --document-name "AWS-RunShellScript" --parameters "commands=[\\"sudo yum install -y python3-pip\\"]"'
		sh 'sleep 30'
		sh 'aws ssm send-command --instance-ids $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --document-name "AWS-RunShellScript" --parameters "commands=[\\"pip3 install flask\\"]"'
		sh 'sleep 30'
                sh 'aws ssm send-command --instance-ids $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --document-name "AWS-RunShellScript" --parameters "commands=[\\"export FLASK_APP=app.py\\"]"'
		sh 'sleep 30'
		sh 'aws ssm send-command --instance-ids $(cat /Users/slver/.jenkins/workspace/ec-aws-s3/instance_id.txt) --document-name "AWS-RunShellScript" --parameters "commands=[\\"flask run --host 0.0.0.0 &\\"]\"'
                sh 'sleep 30'
                sh 'curl -o output.jpg http://localhost:5000/image'
                sh 'curl -o output.html http://localhost:5000/'
		}
            }
        }
        
        //stage('Cleanup') {
        //    steps {
        //        sh 'aws ec2 terminate-instances --instance-ids "$(cat instance-id.txt)"'
        //    }
        //}
    }
}
