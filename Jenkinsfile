pipeline {
    agent any
    
    parameters {
        string(name: 'instance_type', defaultValue: 't2.micro', description: 'EC2 instance type')
        string(name: 'ami_id', defaultValue: 'your_ami_id', description: 'AMI ID for EC2 instance')
        string(name: 'security_group_id', defaultValue: 'your_security_group_id', description: 'Security group ID for EC2 instance')
        string(name: 'subnet_id', defaultValue: 'your_subnet_id', description: 'Subnet ID for EC2 instance')
        string(name: 's3_bucket', defaultValue: 'your_s3_bucket', description: 'Name of S3 bucket containing image file')
        string(name: 's3_key', defaultValue: 'your_s3_key', description: 'S3 key of image file')
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
                sh "aws ec2 run-instances --image-id ${params.ami_id} --instance-type ${params.instance_type} --subnet-id ${params.subnet_id} --security-group-ids ${params.security_group_id} --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=hello-instance}]'"
            }
        }
        
        stage('Deploy') {
            environment {
                AWS_DEFAULT_REGION = 'your_aws_region'
                AWS_ACCESS_KEY_ID = credentials('aws-access-key')
                AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
            }
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
        
        stage('Cleanup') {
            steps {
                sh 'aws ec2 terminate-instances --instance-ids "$(cat instance-id.txt)"'
            }
        }
    }
}
