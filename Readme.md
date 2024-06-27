pip install flask

vim app.py
...............................
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello From D!nesh'

app.run(host='0.0.0.0',port=80)
...............................

python3 app.py

--------------------------------

single bundle it using pyinstaller

pip install pyinstaller

pyinstaller app.py

cd dist/

cd app

ls

./app -->to execute it 



---------------------------------

To automate it Application
Folder structure
code/app
	-app.py
	-requirement.txt
		-flask=2.2.2
python.yml
---------------------------------------
stages:
  - build
  - push-to-google-cloud

build-job:
  stage: build
  image: python:3.11.2-slim-buster
  before_script:
    - apt-get update && apt-get install -y binutils zip
  script:
    - mkdir artifacts
    - ls -al
    - cd code/app
    - pip install -r requirements.txt
    - pip install pyinstaller
    - pyinstaller --onefile app.py
    - ls -al dist
    - cd dist
    - zip -r app.zip app
    - ls -al
    - cp app.zip ../../../artifacts
  artifacts:
    paths:
      - artifacts
  when: manual

push-job:
  stage: push-to-google-cloud
  script:
    - /google-cloud-sdk/bin/gsutil cp artifacts/app.zip gs://your-bucket-name/
  when: manual


---------------------------------------
pipeline {
    agent {
        docker {
            image 'python:3.11.2-slim-buster'
        }
    }
    environment {
        GCS_BUCKET = 'gs://your-bucket-name/'
        GCS_CREDENTIALS = 'gcs-credentials-id' // Make sure this credential ID matches the one in Jenkins
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-github-repo.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                apt-get update && apt-get install -y binutils zip
                pip install -r code/app/requirements.txt
                pip install pyinstaller
                '''
            }
        }
        
        stage('Build Application') {
            steps {
                sh '''
                mkdir artifacts
                cd code/app
                pyinstaller --onefile app.py
                cd dist
                zip -r app.zip app
                cp app.zip ../../../artifacts
                '''
            }
        }
        
        stage('Upload to Google Cloud Storage') {
            steps {
                withCredentials([file(credentialsId: "${GCS_CREDENTIALS}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                    /google-cloud-sdk/bin/gsutil cp artifacts/app.zip ${GCS_BUCKET}
                    '''
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'artifacts/app.zip'
        }
    }
}
---------------------------------------------------------------




