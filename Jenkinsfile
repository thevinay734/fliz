pipeline {
    agent any

    environment {
        BASE_URL = 'https://dev.fliz.com.sa/'
        API_BASE_URL = 'https://dev.api.fliz.com.sa/'
        HEADLESS = 'true'
        LOG_LEVEL = 'INFO'
        ENVIRONMENT = 'dev'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python3 -m venv .venv || true'
                    sh '''
                        . .venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                    sh '''
                        . .venv/bin/activate
                        playwright install chromium
                    '''
                }
            }
        }

        stage('Run API Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest tests/api/ -m api -v \
                        --junitxml=reports/junit-api.xml \
                        --html=reports/report-api.html \
                        --self-contained-html || true
                '''
            }
        }

        stage('Run UI Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest tests/ui/ -m ui -v \
                        --junitxml=reports/junit-ui.xml \
                        --html=reports/report-ui.html \
                        --self-contained-html \
                        --browser chromium || true
                '''
            }
        }
    }

    post {
        always {
            // Archive reports
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
        }

        success {
            echo 'Pipeline completed successfully!'
        }

        cleanup {
            sh 'rm -rf .venv || true'
        }
    }
}
