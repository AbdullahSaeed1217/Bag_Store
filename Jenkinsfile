pipeline {
    agent any

    environment {
        KUBE_CONFIG_PATH = "~/.kube/config" // Path to your kubeconfig file
        TF_VAR_kube_config_path = "~/.kube/config" // Path for Terraform to access kubeconfig
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Fetch code from GitHub repository
                git branch: 'main', url: 'https://github.com/AbdullahSaeed1217/Bag_Store.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Set up a Python virtual environment and install dependencies
                    sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image for the Django app
                    sh '''
                    docker build -t django-app:latest .
                    '''
                }
            }
        }

        stage('Load Docker Image to Kind') {
            steps {
                script {
                    // Load the built image into Kind cluster
                    sh '''
                    kind load docker-image django-app:latest --name django-cluster
                    '''
                }
            }
        }

        stage('Terraform Init') {
            steps {
                script {
                    // Initialize Terraform in the 'terraform' directory
                    dir('terraform') {
                        sh 'terraform init'
                    }
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                script {
                    // Generate a Terraform plan
                    dir('terraform') {
                        sh 'terraform plan'
                    }
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                script {
                    // Apply Terraform to provision infrastructure
                    dir('terraform') {
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
        }

        stage('Deploy with Kubernetes') {
            steps {
                script {
                    // Deploy to Kubernetes using kubectl
                    sh '''
                    kubectl apply -f k8s/django-deployment.yml
                    kubectl apply -f k8s/django-service.yml
                    kubectl apply -f k8s/nginx-ingress.yml
                    '''
                }
            }
        }

        stage('Deploy NGINX Ingress with Helm') {
            steps {
                script {
                    // Use Helm to deploy the NGINX Ingress controller
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
                    // Run the Ansible playbook for additional configurations
                    sh '''
                    ansible-playbook -i ansible/inventory/inventory.yml ansible/playbooks/setup-django.yml
                    '''
                }
            }
        }

        stage('Verify Services') {
            steps {
                script {
                    // Verify running services and pods
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
            // Cleanup resources
            steps {
                script {
                    // Delete Kubernetes resources
                    sh '''
                    kubectl delete -f k8s/django-deployment.yml || true
                    kubectl delete -f k8s/django-service.yml || true
                    kubectl delete -f k8s/nginx-ingress.yml || true
                    '''

                    // Stop and remove Docker containers (optional cleanup for local resources)
                    sh '''
                    docker-compose down || true
                    docker system prune -f || true
                    '''
                }
            }
        }
    }
}
