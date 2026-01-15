pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t product-scanner-app .'
            }
        }

        stage('Stop Old Container (if any)') {
            steps {
                bat '''
                docker stop product-scanner-container || exit 0
                docker rm product-scanner-container || exit 0
                '''
            }
        }

        stage('Run Application in Docker') {
            steps {
                bat 'docker run -d -p 5000:5000 --name product-scanner-container product-scanner-app'
            }
        }
    }
}
