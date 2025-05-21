pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'ljm-app'
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
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                script {
                    sh '''
                        docker stop ljm || true
                        docker rm ljm || true
                    '''
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh 'docker run -d -p 8501:8501 --name ljm --restart always $DOCKER_IMAGE'
                }
            }
        }
    }
}

