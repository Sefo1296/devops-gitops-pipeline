pipeline {

    agent {
        kubernetes {
            yamlFile 'pod.yaml'
        }
    }


    environment {
        IMAGE_NAME = "sefo1296/devops-gitops-app"
        IMAGE_TAG = "v${BUILD_NUMBER}"
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
                    sh '''
                    pip install -r app/requirements.txt
                    '''
                }
            }
        }


        stage('Run Tests') {
            steps {
                container('python') {
                    sh '''
                    pytest app/test_app.py
                    '''
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
                    --destination=${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }


        stage('Update Helm Values') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {


                    sh '''
                    
                    echo "Updating Helm image tag..."

                    sed -i "s/tag:.*/tag: \\"${IMAGE_TAG}\\"/" helm/flask-app/values.yaml


                    git config user.email "saifeldinelsalamony@gmail.com"
                    git config user.name "Jenkins"


                    git add helm/flask-app/values.yaml


                    git commit -m "Update image tag to ${IMAGE_TAG}" || echo "No changes"


                    git push https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/Sefo1296/devops-gitops-pipeline.git main

                    '''
                }
            }
        }

    }
}
