pipeline {
    agent any

    environment {
        VIRTUAL_ENV = 'venv'
        DJANGO_SECRET_KEY = 'django-insecure-_p)jzspqnsu#kq^e$q9g-d_z8sy)s2yf3t_g2j3s@!erc-^3q'
        DOCKER_IMAGE = 'django-app:latest'
        KIND_CLUSTER = 'django-cluster'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout the Django project code from GitHub (public repository)
                git branch: 'main', url: 'https://github.com/AbdullahSaeed1217/Ecommerce_Store.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Set up Python virtual environment and install dependencies
                    sh '''
                    python3 -m venv $VIRTUAL_ENV
                    source $VIRTUAL_ENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Django Migrations') {
            steps {
                script {
                    // Apply migrations to set up the database schema
                    sh '''
                    source $VIRTUAL_ENV/bin/activate
                    python manage.py migrate
                    '''
                }
            }
        }

        stage('Run Django Tests') {
            steps {
                script {
                    // Run Django tests to ensure everything is working
                    sh '''
                    source $VIRTUAL_ENV/bin/activate
                    python manage.py test
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image for the Django application
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Load Docker Image to Kind Cluster') {
            steps {
                script {
                    // Load the Docker image into a Kubernetes cluster managed by Kind
                    sh "kind load docker-image ${DOCKER_IMAGE} --name ${KIND_CLUSTER}"
                }
            }
        }

        stage('Terraform Init and Apply') {
            steps {
                dir('terraform') {
                    script {
                        // Initialize and apply Terraform for infrastructure provisioning
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
                    // Deploy the Django app on Kubernetes
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
                    // Deploy NGINX ingress controller using Helm
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
                    // Run Ansible playbook for any additional setup or configurations
                    sh '''
                    ansible-playbook -i ansible/inventory/inventory.yml ansible/playbooks/setup-django.yml
                    '''
                }
            }
        }

        stage('Verify Services') {
            steps {
                script {
                    // Verify the deployment status of services in the Kubernetes cluster
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
        success {
            echo 'Django application deployed successfully on Kubernetes!'
        }
        failure {
            echo 'Django application deployment failed.'
        }
        always {
            // Clean up resources after the pipeline run
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
