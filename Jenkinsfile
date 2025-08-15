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

        stage('Test K8s Connection') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig-file']) {
                    bat 'kubectl get pods -A'
                }
            }
        }

        stage('Train Model') {
            steps {
                bat """
                call "%WORKSPACE%\\venv\\Scripts\\activate.bat"
                python train_model.py
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    bat "docker login -u ibrahimozkardes -p %DOCKERHUB_TOKEN%"
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                bat "docker build -t ${REGISTRY}/${IMAGE_NAME}:latest ."
                bat "docker push ${REGISTRY}/${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                    bat "kubectl apply -f deployment.yaml"
                    bat "kubectl apply -f service.yaml"
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo "🔍 Pod ve API monitoring başlatılıyor..."
                // Pod status kontrolü
                bat "kubectl get pods -l app=stock-predictor"
                // Pod resource usage
                bat "kubectl top pods -l app=stock-predictor"
                // Basit API health check
                bat "curl -s http://localhost:8000/ | findstr /i 'Stock Predictor API çalışıyor'"
            }
        }
    }
}