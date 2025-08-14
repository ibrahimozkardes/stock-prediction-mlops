pipeline {
    agent any

    environment {
        IMAGE_NAME = "stock-predictor"
        REGISTRY = "dockerhub_username"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ibrahimozkardes/stock-prediction-mlops.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:latest ."
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    sh "echo $DOCKERHUB_TOKEN | docker login -u dockerhub_username --password-stdin"
                    sh "docker push ${REGISTRY}/${IMAGE_NAME}:latest"
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/deployment.yaml"
                sh "kubectl apply -f k8s/service.yaml"
            }
        }
    }
}
