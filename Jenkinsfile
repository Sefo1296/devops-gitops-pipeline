pipeline {
    agent {
        kubernetes {
            yamlFile 'pod.yaml'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                container('python') {
                    sh 'pip install -r app/requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                container('python') {
                    sh 'pytest app/test_app.py'
                }
            }
        }

        stage('Build & Push Image') {
            steps {
                container('kaniko') {
                    sh '''
                    /kaniko/executor \
                      --context=$WORKSPACE \
                      --dockerfile=$WORKSPACE/Dockerfile \
                      --destination=sefo1296/devops-gitops-app:v1
                    '''
                }
            }
        }
    }
}
