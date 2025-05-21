pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'ljm-app'
	IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/jungjin-lee90/LJM.git', branch: 'main'
            }
        }
	
	stage('Checkout') {
            steps {
                checkout scm
            }
        }
	
	stage('Build Docker Image') {
            steps {
                sh """
                echo "Building Docker image with tag: ${env.IMAGE_TAG}"
                docker build -t ${env.IMAGE_NAME}:${env.IMAGE_TAG} .
                docker tag ${env.IMAGE_NAME}:${env.IMAGE_TAG} ${env.IMAGE_NAME}:latest
                """
            }
        }

        stage('Clean old Docker images') {
            steps {
                sh """
                echo "Cleaning up old Docker images for ${env.IMAGE_NAME}..."
                docker images --format '{{.Repository}} {{.Tag}} {{.CreatedAt}} {{.ID}}' | \
                  grep '^${env.IMAGE_NAME} ' | \
                  grep -v 'latest' | \
                  sort -rk3 | \
                  tail -n +4 | \
                  awk '{print \$4}' | \
                  xargs -r docker rmi || true
                """
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker stop ${env.IMAGE_NAME} || true
                docker rm ${env.IMAGE_NAME} || true
                docker run -d --name ${env.IMAGE_NAME} --restart always -p 8501:8501 ${env.IMAGE_NAME}:${env.IMAGE_TAG}
                """
            }
        }
    }
}

