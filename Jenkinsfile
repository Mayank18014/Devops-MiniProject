pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "devops-mini-project"
        CONTAINER_NAME = "flask-prod-app"
    }

    stages {
        stage('Checkout') {
            steps {
                // Clones from your specific repo
                git branch: 'main', url: 'https://github.com/Mayank18014/Devops-MiniProject.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Deploy (CD)') {
            steps {
                // Remove old container if running to avoid port conflicts
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                // Run the new container
                sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Selenium Testing') {
            steps {
                // Assumes you have a 'tests' folder with your selenium script
                // We use 'container-ip' or 'localhost' depending on Jenkins setup
                sh "python3 tests/selenium_tests.py"
            }
        }
    }

    post {
        success {
            echo "Deployment and Selenium tests passed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs for Docker or Selenium errors."
        }
    }
}
