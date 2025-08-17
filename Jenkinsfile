pipeline {
    agent {label "ec2"}
    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '391974145213'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        ECR_REPO = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/bullbeario"
        FULL_IMAGE = "${ECR_REPO}:${IMAGE_TAG}"
    }
    stages {

        stage('Clone Application Repo') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github')]) {
                    script {
                        if (fileExists('BullBearIO')) {
                            dir('BullBearIO') {
                                sh '''
                                    git checkout main || git checkout -b master origin/main
                                    git pull origin main
                                '''
                            }
                        } else {
                            sh 'git clone https://github.com/Gmaze99/BullBearIO.git'
                        }
                    }
                }
            }
        }
        
        stage('Clean old Docker image') {
            steps {
                sh 'docker rmi -f bullbeario-frontend:latest || true'
                sh 'docker rmi -f bullbeario-backend:latest || true'
            }
        }

        stage('Build Docker image') {
            steps {
                dir('BullBearIO/frontend') {
                    sh 'docker build -t bullbeario-frontend:${IMAGE_TAG} .'
                }
                dir('BullBearIO/backend'){
                    sh 'docker build -t bullbeario-backend:${IMAGE_TAG} .'
                }
            }
        }

       stage('Push Docker Image To ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
        
                    # Push frontend
                    docker tag bullbeario-frontend:${IMAGE_TAG} ${ECR_REPO}/bullbeario-frontend:${IMAGE_TAG}
                    docker push ${ECR_REPO}/bullbeario-frontend:${IMAGE_TAG}
        
                    # Push backend
                    docker tag bullbeario-backend:${IMAGE_TAG} ${ECR_REPO}/bullbeario-backend:${IMAGE_TAG}
                    docker push ${ECR_REPO}/bullbeario-backend:${IMAGE_TAG}
                '''
            }
        }
    }
}