pipeline {
    agent any

    environment {
        IMAGE_NAME = 'ljm-app'
    }

    stages {
	stage('Set Version Tag') {
            steps {
                script {
                    env.IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
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

	stage('Release Port 8501 if Used') {
    	    steps {
        	sh '''
        	    echo "🔍 Checking if port 8501 is in use..."
        	    CONFLICT=$(docker ps -q --filter "publish=8501")
        	    if [ ! -z "$CONFLICT" ]; then
          		echo "⚠ Port 8501 is in use. Removing conflicting container(s)..."
          		docker rm -f $CONFLICT
        	    else
          		echo "✅ Port 8501 is free."
        	    fi
        	'''
    	    }
	}	

        stage('Run Container') {
            steps {
                sh """
                docker rm -f ${env.IMAGE_NAME} || true
                docker run -d --name ${env.IMAGE_NAME} --restart always -p 8501:8501 ${env.IMAGE_NAME}:${env.IMAGE_TAG}
                """
            }
        }
    }
}
