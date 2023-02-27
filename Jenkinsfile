pipeline {
    agent any
    
    parameters {
        string(name: 'instance_type', defaultValue: 't2.micro', description: 'EC2 instance type')
        string(name: 'ami_id', defaultValue: 'ami-0dfcb1ef8550277af', description: 'AMI ID for EC2 instance')
        string(name: 'security_group_id', defaultValue: 'sg-0ce11929837aacbe3', description: 'Security group ID for EC2 instance')
        string(name: 'subnet_id', defaultValue: 'subnet-0bd9344715e3897c0', description: 'Subnet ID for EC2 instance')
        string(name: 's3_bucket', defaultValue: 'ec2-jenkins-001', description: 'Name of S3 bucket containing image file')
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
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'pip install awscli'
                sh 'aws ec2 describe-instances --filters "Name=tag:Name,Values=hello-instance" --query "Reservations[0].Instances[0].InstanceId" --output text > instance-id.txt'
                sh 'aws s3 cp s3://${params.s3_bucket}/${params.s3_key} image.jpg'
                sh 'aws s3 cp app.py .'
                sh 'aws s3 cp templates/index.html templates/'
                sh 'aws ec2 run-command --instance-ids "$(cat instance-id.txt)" --document-name "AWS-RunShellScript" --parameters "commands=[\\"pip install flask\\"]"'
                sh 'aws ec2 run-command --instance-ids "$(cat instance-id.txt)" --document-name "AWS-RunShellScript" --parameters "commands=[\\"FLASK_APP=app.py flask run --host 0.0.0.0 &\\"]"'
                sh 'sleep 10'
                sh 'curl -o output.jpg http://localhost:5000/image'
                sh 'curl -o output.html http://localhost:5000/'
            }
        }
        
        //stage('Cleanup') {
        //    steps {
        //        sh 'aws ec2 terminate-instances --instance-ids "$(cat instance-id.txt)"'
        //    }
        //}
    }
}
