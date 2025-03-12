pipeline {
    agent any
    
    environment {
        SUPER_ADMIN_USERNAME = credentials('SUPER_ADMIN_USERNAME')
        SUPER_ADMIN_PASSWORD = credentials('SUPER_ADMIN_PASSWORD')
        SUPER_ADMIN_EMAIL = credentials('SUPER_ADMIN_EMAIL')
        JENKINS_ENV="true"
    }
    
    stages {
        // Stage 1: Checkout Source Code
        stage('Checkout Source Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/amar2468/GameHive.git'
            }
        }
        
        // Stage 2: Set Up Python Virtual Environment
        stage('Set Up Python Virtual Environment') {
            steps {
                bat 'python -m venv gamehive-virtual-environment'
            }
        }
        
        // Stage 3: Install Python Dependencies
        stage('Install Python Dependencies') {
            steps {
                bat '.\\gamehive-virtual-environment\\Scripts\\python -m pip install --upgrade pip'
                bat '.\\gamehive-virtual-environment\\Scripts\\python -m pip install -r requirements.txt'
            }
        }
        
        // Stage 4: Apply Migrations
        stage('Apply Migrations') {
            steps {
                bat '.\\gamehive-virtual-environment\\Scripts\\python manage.py migrate'
            }
        }

        // Stage 5: Run Tests
        stage('Run Tests') {
            steps {
                bat '.\\gamehive-virtual-environment\\Scripts\\python manage.py test gamehive'
            }
        }
    }
}