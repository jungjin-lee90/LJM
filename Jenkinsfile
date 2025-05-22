pipeline {
    agent any
	
    options {
        disableConcurrentBuilds()  // 동시 실행 방지
	ansiColor('xterm')
        timestamps()
    }

    parameters {
        string(name: 'PORT', defaultValue: '8501', description: 'Host port to expose')
        string(name: 'IMAGE_NAME', defaultValue: 'ljm-app', description: 'Docker image and container name')
    }

//    environment {
     //    IMAGE_NAME = 'ljm-app'
//    }

    stages {
//	stage('Set Version Tag') {
//            steps {
//                script {
//                    env.IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
//                }
//            }
//    	}
	stage('Set Version Tag') {
            steps {
                script {
                    env.IMAGE_TAG = sh(
                        script: "date +%Y%m%d-%H%M%S",
                        returnStdout: true
                    ).trim()
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
                docker build -t ${params.IMAGE_NAME}:${env.IMAGE_TAG} .
                docker tag ${params.IMAGE_NAME}:${env.IMAGE_TAG} ${params.IMAGE_NAME}:latest
                """
            }
        }

        stage('Clean old Docker images') {
            steps {
                sh """
                echo "Cleaning up old Docker images for ${params.IMAGE_NAME}..."
		docker images ${params.IMAGE_NAME} --format '{{.ID}}' | \
  		    tail -n +4 | \
  		    xargs -r docker rmi
                """
            }
        }

	stage('Release Port 8501 if Used') {
    	    steps {
        	sh '''
        	    echo " Checking if port ${params.PORT} is in use..."
        	    CONFLICT=$(docker ps -q --filter "publish=${params.PORT}")
        	    if [ ! -z "$CONFLICT" ]; then
          		echo " Port ${params.PORT} is in use. Removing conflicting container(s)..."
          		docker rm -f $CONFLICT
        	    else
          		echo "Port ${params.PORT} is free."
        	    fi
        	'''
    	    }
	}	

        stage('Run Container') {
            steps {
                sh """
                docker rm -f ${params.IMAGE_NAME} || true
                docker run -d --name ${params.IMAGE_NAME} --restart always -p ${params.PORT}:8501 ${params.IMAGE_NAME}:${env.IMAGE_TAG}
                """
            }
        }
    }

    post {
        success {
            echo "Build and deployment completed: ${params.IMAGE_NAME}:${env.IMAGE_TAG}"
        }
        failure {
            echo "Build failed."
        }
    }
}
