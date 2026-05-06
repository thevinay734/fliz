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
                    // Create virtual environment
                    sh 'python3 -m venv .venv || true'

                    // Install Python dependencies
                    sh '''
                        . .venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''

                    // Install Playwright browsers (for UI tests)
                    sh '''
                        . .venv/bin/activate
                        playwright install chromium
                    '''
                }
            }
        }

        stage('Run API Tests') {
            steps {
                script {
                    sh '''
                        . .venv/bin/activate
                        pytest tests/api/ -m api -v \
                            --junitxml=reports/junit-api.xml \
                            --html=reports/report-api.html \
                            --self-contained-html
                    '''
                }
            }
        }

        stage('Run UI Tests') {
            steps {
                script {
                    sh '''
                        . .venv/bin/activate
                        pytest tests/ui/ -m ui -v \
                            --junitxml=reports/junit-ui.xml \
                            --html=reports/report-ui.html \
                            --self-contained-html \
                            --browser chromium
                    '''
                }
            }
        }
    }

    post {
        always {
            // Publish JUnit XML results
            junit 'reports/junit-*.xml'

            // Archive HTML reports
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report-api.html,report-ui.html',
                reportName: 'Test Reports'
            ])
        }

        success {
            echo 'All tests passed!'
        }

        failure {
            echo 'Some tests failed. Check Console Output and HTML reports.'
        }

        cleanup {
            // Cleanup virtual environment
            sh 'rm -rf .venv || true'
        }
    }
}
