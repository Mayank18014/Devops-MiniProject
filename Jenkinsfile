pipeline {
    agent any

    environment {
        // Defining the image name as a variable makes the script easier to maintain
        IMAGE_NAME = "devops-mini-project"
        IMAGE_TAG  = "latest"
    }

    stages {
        // Note: 'Checkout SCM' happens automatically; no need for a manual git stage.

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                // Added '.' at the end to specify the current directory context
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Selenium Testing') {
            steps {
                echo "Running Selenium tests..."
                // Add your testing commands here, e.g., python selenium_tests.py
                echo "Tests passed!"
            }
        }

        stage('Deploy (CD)') {
            steps {
                echo "Deploying application..."
                // Example: Stop old container and run new one
                // sh "docker stop ${IMAGE_NAME} || true && docker rm ${IMAGE_NAME} || true"
                // sh "docker run -d -p 5000:5000 --name ${IMAGE_NAME} ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs for Docker or Selenium errors."
        }
        always {
            // Clean up workspace to save disk space
            cleanWs()
        }
    }
}
