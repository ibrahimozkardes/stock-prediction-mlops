pipeline {
    agent any

    environment {
        IMAGE_NAME = "stock-predictor"
        REGISTRY = "ibrahimozkardes"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ibrahimozkardes/stock-prediction-mlops.git'
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    bat "docker login -u ibrahimozkardes -p %DOCKERHUB_TOKEN%"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${REGISTRY}/${IMAGE_NAME}:latest ."
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    bat """
                    docker login -u ibrahimozkardes -p %DOCKERHUB_TOKEN%
                    docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat "kubectl apply -f k8s\\deployment.yaml"
                bat "kubectl apply -f k8s\\service.yaml"

            }
        }
    }
}
