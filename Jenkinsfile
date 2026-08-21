pipeline {
    agent any

    parameters {
        string(
            name: 'LOCALES_DIR',
            defaultValue: 'locales',
            description: 'Directory containing en.json and translated locale JSON files.'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate') {
            steps {
                script {
                    int status = sh(
                        script: "bash tools/run_checks.sh '${params.LOCALES_DIR}'",
                        returnStatus: true
                    )

                    if (status != 0) {
                        unstable("Locale validation found issues. See reports/locale-report.txt.")
                    }
                }
            }
        }

        stage('Report') {
            steps {
                archiveArtifacts artifacts: 'reports/locale-report.txt', allowEmptyArchive: false
            }
        }
    }

    post {
        success {
            echo 'Locale validation passed successfully.'
        }
        unstable {
            echo 'Locale validation completed, but issues were found.'
        }
        failure {
            echo 'Locale validation pipeline failed before producing a clean result.'
        }
        always {
            echo "Checked locales directory: ${params.LOCALES_DIR}"
        }
    }
}
