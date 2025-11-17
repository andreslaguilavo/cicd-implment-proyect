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
        
        // stage('Test') {
        //     steps {
        //         echo 'Ejecutando tests básicos...'
        //         script {
        //             sh "docker images | grep ${DOCKER_IMAGE}"
        //         }
        //     }
        // }
        
        stage('Deploy with Docker Compose') {
            steps {
                echo 'Desplegando app y base de datos...'
                script {
                    sh '''
                        # Forzar eliminación de contenedores existentes
                        docker stop cicd_app cicd_db 2>/dev/null || true
                        docker rm -f cicd_app cicd_db 2>/dev/null || true
                        
                        # Levantar solo app y db
                        docker compose up -d --build app db
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Verificando que la app responde...'
                script {
                    sleep(time: 15, unit: 'SECONDS')
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
            sh 'docker compose logs app || true'
        }
        always {
            echo 'Limpiando recursos...'
            sh 'docker system prune -f || true'
        }
    }
}