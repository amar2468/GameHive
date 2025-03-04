pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/amar2468/GameHive.git'
            }
        }
        
        stage('Setup') {
            steps {
                // Creating a virtual environment
                bat 'python -m venv gamehive-virtual-environment'
            }
        }
        
        stage('Testing') {
            steps {
                // Installing all the required dependencies that are needed in the virtual environment
                bat '.\\gamehive-virtual-environment\\Scripts\\python -m pip install -r requirements.txt'
                
                // Runs all the tests inside this project
                bat '.\\gamehive-virtual-environment\\Scripts\\python manage.py test'
            }
        }
        
    }
}