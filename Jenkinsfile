pipeline {
    agent any

    environment {
        AZURE_RESOURCE_GROUP = 'SWII-CICD'
        AZURE_APP_SERVICE_NAME = 'productosjson'
        AZURE_CREDENTIALS_ID = 'azure-service-principal'
        APP_ZIP_FILE = 'app.zip'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Json-Esutpinan/cicd-implment.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                rm -rf venv
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh '''
                . venv/bin/activate
                export PYTHONPATH=$PYTHONPATH:$(pwd)
                pytest
                '''
            }
        }
        stage('Create Deployment Package') {
            steps {
                sh '''
                # Listar el contenido para depuración (opcional, pero útil)
                echo "Contenido del workspace antes de crear el ZIP:"
                ls -la .

                # Crear el archivo ZIP de la aplicación
                # Asegúrate de que el comando 'zip' esté disponible en tu VM de Jenkins.
                # Si tu código está en un subdirectorio (ej. 'cicd-implment'), ajusta la ruta aquí.
                # Por ejemplo: cd cicd-implment/ && zip -r ${APP_ZIP_FILE} ./*
                zip -r ${APP_ZIP_FILE} ./*

                echo "Archivo ZIP creado:"
                ls -la ${APP_ZIP_FILE}
                '''
            }
        }
        stage('Deploy to Azure App Service') {
            steps {
                withCredentials([azureServicePrincipal(AZURE_CREDENTIALS_ID)]) {
                    sh '''
                        # Autenticarse con el Service Principal usando Azure CLI
                        az login --service-principal -u "$AZURE_CLIENT_ID" -p "$AZURE_CLIENT_SECRET" --tenant "$AZURE_TENANT_ID" --allow-no-subscription

                        # Desplegar el archivo ZIP
                        # El --type zip es crucial para indicar que se está desplegando un archivo ZIP
                        az webapp deploy --resource-group "$AZURE_RESOURCE_GROUP" --name "$AZURE_APP_SERVICE_NAME" --src-path "${APP_ZIP_FILE}" --type zip

                        # Opcional: Cerrar sesión de Azure CLI después del despliegue
                        az logout
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
