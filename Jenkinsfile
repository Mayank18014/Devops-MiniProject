pipeline {
    agent any

    stages {

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQubeServer') {
                        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                            bat """
                            ${scannerHome}\\bin\\sonar-scanner ^
                            -Dsonar.projectKey=product-scanner ^
                            -Dsonar.projectName=ProductScanner ^
                            -Dsonar.sources=. ^
                            -Dsonar.language=py ^
                            -Dsonar.login=%SONAR_TOKEN%
                            """
                        }
                    }
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
