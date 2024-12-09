// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // Fetch code from Git repository
                git branch: 'main', url: 'https://github.com/AbdullahSaeed1217/Sham_E_Store.git'
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Use Python virtual environment
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
                    // Build the Docker image for Django
                    sh '''
                    docker build -t django-app:latest .
                    '''
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    // Deploy the Docker container using Docker Compose
                    sh '''
                    docker-compose up -d
                    '''
                }
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                script {
                    // Run the Ansible playbook for configuration
                    sh '''
                    ansible-playbook -i ansible/inventory/inventory.yml ansible/playbooks/setup-django.yml
                    '''
                }
            }
        }

        stage('Verify Services') {
            steps {
                script {
                    // Verify Docker containers are running
                    sh "docker ps"

                    // Optionally, check other services or configurations
                    // like checking Jenkins status, database connections, etc.
                }
            }
        }
    }

    post {
        always {
            // Cleanup resources after the pipeline
            script {
                // Stop and remove Docker containers
                sh '''
                docker stop django-app || true
                docker rm django-app || true
                docker system prune -f || true
                '''
            }
        }
    }
}