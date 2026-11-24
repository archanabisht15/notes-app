pipeline {
  agent any
  environment {
    IMAGE = "archanabisht/notes-app"
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t $IMAGE:$BUILD_NUMBER .'
      }
    }
    stage('Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
          usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'echo $PASS | docker login -u $USER --password-stdin'
          sh 'docker push $IMAGE:$BUILD_NUMBER'
        }
      }
    }
  }
}
