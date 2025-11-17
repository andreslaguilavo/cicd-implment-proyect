pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'cicd-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Clonando repositorio desde GitHub...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Construyendo imagen Docker...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Ejecutando tests básicos...'
                script {
                    // Verifica que la imagen se construyó correctamente
                    sh "docker images | grep ${DOCKER_IMAGE}"
                }
            }
        }
        
        stage('Deploy with Docker Compose') {
            steps {
                echo 'Desplegando con Docker Compose...'
                script {
                    sh 'docker compose down || true'
                    sh 'docker compose up -d --build'
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Verificando que la app responde...'
                script {
                    sleep(time: 10, unit: 'SECONDS')
                    sh 'curl -f http://localhost:5000/health || exit 1'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline ejecutado exitosamente!'
        }
        failure {
            echo 'Pipeline falló. Revisa los logs.'
            sh 'docker compose logs app'
        }
        always {
            echo 'Limpiando recursos...'
            sh 'docker system prune -f'
        }
    }
}