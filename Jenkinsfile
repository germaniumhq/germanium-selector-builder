stage('Python Tooling') {
    node {
        deleteDir()
        checkout scm

        docker.build("mypy_${env.BUILD_ID}",
                     '-f Dockerfile.py.build .')
              .inside("-v ${pwd()}:/src")
        {
            sh """
                cd /src
                mypy application.py
            """
        }
    }
}

stage('Build EXE') {
    node {
        deleteDir()
        checkout scm

        dockerBuild file: './Dockerfile',
            tags: ['germaniumhq/germanium-selector-builder']
    }
}

stage('Extract EXE File') {
    node {
        docker.image('germaniumhq/germanium-selector-builder')
              .inside {
            archiveArtifacts artifacts: '/src/dist/main.exe', fingerprint: true
        }
    }
}

