pipeline {
    agent any

    environment {
        IMAGE_NAME = "stock-predictor"
        REGISTRY = "ibrahimozkardes"
        MODEL_PATH = "model/model.pkl"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ibrahimozkardes/stock-prediction-mlops.git'
            }
        }

        stage('Train Model') {
            steps {
                sh """
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                mkdir -p model
                python train_model.py --output ${MODEL_PATH}
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    sh "echo $DOCKERHUB_TOKEN | docker login -u ${REGISTRY} --password-stdin"
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:latest ."
                sh "docker push ${REGISTRY}/${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl apply -f service.yaml"
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo "🔍 Pod ve API monitoring başlatılıyor..."
                sh "kubectl get pods -l app=stock-predictor"
                sh "kubectl top pods -l app=stock-predictor || echo '⚠️ Metrics server yok'"
                sh "kubectl get svc stock-predictor"
                // Health check (service IP üzerinden)
                sh """
                SERVICE_IP=$(kubectl get svc stock-predictor -o jsonpath='{.spec.clusterIP}')
                curl -s http://$SERVICE_IP:8000/ | grep 'Stock Predictor'
                """
            }
        }
    }
}