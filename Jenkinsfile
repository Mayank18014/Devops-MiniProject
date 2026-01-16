pipeline {
    agent any

    tools {
        sonarScanner 'SonarScanner'
    }

    stages {

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat '''
                    sonar-scanner ^
                      -Dsonar.projectKey=product-scanner ^
                      -Dsonar.projectName=Product-Scanner ^
                      -Dsonar.sources=. ^
                      -Dsonar.language=py ^
                      -Dsonar.python.version=3 ^
                      -Dsonar.sourceEncoding=UTF-8
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t product-scanner-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat '''
                docker stop product-scanner-container || exit 0
                docker rm product-scanner-container || exit 0
                '''
            }
        }

        stage('Run Application') {
            steps {
                bat 'docker run -d -p 5000:5000 --name product-scanner-container product-scanner-app'
            }
        }

        stage('Wait for App') {
            steps {
                sleep 10
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'docker exec product-scanner-container python -m xmlrunner test_ui.py'
            }
        }

        stage('Copy Test Reports') {
            steps {
                bat 'docker cp product-scanner-container:/app . || exit 0'
            }
        }

        stage('Publish Test Report') {
            steps {
                junit 'app/TEST*.xml'
            }
        }

        stage('Copy Screenshots') {
            steps {
                bat 'docker cp product-scanner-container:/app/screenshots . || exit 0'
            }
        }
    }
}
