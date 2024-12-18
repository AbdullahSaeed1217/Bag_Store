pipeline {
    agent any

    environment {
        PYTHON_ENV = 'venv'
        DOCKER_IMAGE = 'django-app:latest'
        KIND_CLUSTER = 'django-cluster'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/AbdullahSaeed1217/Bag_Store.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    sh '''
                    python3 -m venv venv
                    source venv/bin/activate"
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Load Docker Image to Kind') {
            steps {
                script {
                    sh "kind load docker-image ${DOCKER_IMAGE} --name ${KIND_CLUSTER}"
                }
            }
        }

        stage('Terraform Init and Apply') {
            steps {
                dir('terraform') {
                    script {
                        sh '''
                        terraform init
                        terraform apply -auto-approve
                        '''
                    }
                }
            }
        }

        stage('Deploy with Kubernetes') {
            steps {
                script {
                    sh '''
                    kubectl apply -f k8s/django-deployment.yml
                    kubectl apply -f k8s/django-service.yml
                    '''
                }
            }
        }

        stage('Deploy NGINX Ingress with Helm') {
            steps {
                script {
                    sh '''
                    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
                    helm repo update
                    helm install nginx-ingress ingress-nginx/ingress-nginx
                    '''
                }
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                script {
                    sh '''
                    ansible-playbook -i ansible/inventory/inventory.yml ansible/playbooks/setup-django.yml
                    '''
                }
            }
        }

        stage('Verify Services') {
            steps {
                script {
                    sh '''
                    kubectl get pods
                    kubectl get svc
                    kubectl get ingress
                    '''
                }
            }
        }
    }

    post {
        always {
            steps {
                script {
                    sh '''
                    kubectl delete -f k8s/django-deployment.yml || true
                    kubectl delete -f k8s/django-service.yml || true
                    helm uninstall nginx-ingress || true
                    docker system prune -f || true
                    '''
                }
            }
        }
    }
}
