pipeline {
    agent any

    environment {
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

     stage('Tests & Coverage') {
    steps {
        echo '🧪 Ejecutando tests dentro de la imagen de la app y subiendo cobertura a Codecov...'
        withCredentials([string(credentialsId: 'CODECOV_TOKEN', variable: 'CODECOV_TOKEN')]) {
            sh '''
                echo "GIT_COMMIT: $GIT_COMMIT"
                echo "GIT_BRANCH: $GIT_BRANCH"

                docker run --rm \
                    -e CODECOV_TOKEN=$CODECOV_TOKEN \
                    -e GIT_COMMIT=$GIT_COMMIT \
                    -e GIT_BRANCH=$GIT_BRANCH \
                    integracion-continua-app sh -c "
                        pytest --cov=. --cov-report=xml:coverage.xml &&
                        curl -s https://uploader.codecov.io/latest/linux/codecov -o codecov &&
                        chmod +x codecov &&
                        ./codecov \
                            -t $CODECOV_TOKEN \
                            -f coverage.xml \
                            -R /app \
                            -C $GIT_COMMIT \
                            -B $GIT_BRANCH \
                            -r andreslaguilavo/cicd-implment-proyect
                    "
            '''
        }
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


    }

    post {
        success {
            echo '✅ Pipeline ejecutado exitosamente!'
        }
        failure {
            echo '❌ Pipeline falló. Revisa los logs de Docker Compose.'
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
