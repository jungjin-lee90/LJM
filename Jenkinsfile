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

        stage('Build Docker Image') {
            steps {
                script {
		    sh """
                        echo "Building Docker image with tag: ${IMAGE_TAG}"
                	docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                	docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    """
                }
            }
        }

	stage('Clean old Docker images') {
            steps {
                sh """
                echo "Cleaning up old Docker images for ${IMAGE_NAME}..."
                docker images --format '{{.Repository}} {{.Tag}} {{.CreatedAt}} {{.ID}}' | \
                  grep '^${IMAGE_NAME} ' | \
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
                docker stop ${IMAGE_NAME} || true
                docker rm ${IMAGE_NAME} || true
                docker run -d --name ${IMAGE_NAME} --restart always -p 8501:8501 ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }
}

