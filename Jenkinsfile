pipeline {

    agent {
        kubernetes {
            yamlFile 'pod.yaml'
        }
    }


    stages {

        stage('Checkout') {
            steps {

                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Sefo1296/devops-gitops-pipeline.git',
                        credentialsId: 'github-creds'
                    ]]
                ])

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
                    --destination=sefo1296/devops-gitops-app:v${BUILD_NUMBER}

                    '''

                }

            }

        }


        stage('Update Helm Values') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {


                    sh '''

                    sed -i "s/tag:.*/tag: \"v${BUILD_NUMBER}\"/" helm/flask-app/values.yaml


                    git config user.email "saifeldinelsalamony@gmail.com"
                    git config user.name "Jenkins"


                    git add helm/flask-app/values.yaml


                    git commit -m "Update image tag to v${BUILD_NUMBER}" || true


                    git remote set-url origin https://${GIT_USER}:${GIT_TOKEN}@github.com/Sefo1296/devops-gitops-pipeline.git


                    git push origin HEAD:main


                    '''

                }

            }

        }


    }

}
