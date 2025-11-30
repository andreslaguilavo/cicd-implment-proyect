pipeline {
    agent any

    environment {
        // por si quieres usarlo en algún paso
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Clonando repositorio desde GitHub...'
                checkout scm
            }
        }

        stage('Build de la imagen de la app') {
            steps {
                echo 'Construyendo imagen Docker de la aplicación...'
                sh '''
                    docker compose -f ${DOCKER_COMPOSE_FILE} build app
                '''
            }
        }

        stage('Deploy con Docker Compose') {
            steps {
                echo 'Levantando contenedores de DB y App...'
                sh '''
                    docker compose -f ${DOCKER_COMPOSE_FILE} up -d db app
                    echo "Estado de los contenedores:"
                    docker compose -f ${DOCKER_COMPOSE_FILE} ps
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Verificando que la app responde en /health...'
                sh '''
                    echo "Esperando 15 segundos a que la app termine de arrancar..."
                    sleep 15

                    echo "Haciendo curl a http://cicd_app:5000/health"
                    curl -f http://cicd_app:5000/health || (echo "Healthcheck falló" && docker compose -f ${DOCKER_COMPOSE_FILE} logs app && exit 1)
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline ejecutado exitosamente!'
        }
        failure {
            echo '❌ Pipeline falló. Revisa los logs de Docker Compose.'
            // Esto ayuda a ver qué pasó con la app
            sh '''
                docker compose -f ${DOCKER_COMPOSE_FILE} ps || true
                docker compose -f ${DOCKER_COMPOSE_FILE} logs app || true
            '''
        }
        always {
            echo 'Limpieza ligera de recursos (imágenes/contendores colgados)...'
            sh 'docker system prune -f || true'
        }
    }
}
