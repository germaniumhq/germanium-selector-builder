
stage('Build EXE') {
    node {
        deleteDir()
        checkout scm

        dockerBuild file: './jenkins/Dockerfile',
            tags: ['germaniumhq/germanium-selector-builder']
    }
}

stage('Build EXE File') {
    node {
        dockerRun image: 'germaniumhq/germanium-selector-builder',
            remove: true,
            env: [
                'PYPI_URL=http://nexus:8081/repository/pypi-local/pypi',
                'PYPI_INDEX_URL=http://nexus:8081/repository/pypi-local/simple'
            ],
            links: [
                'nexus:nexus'
            ],
            volumes: [
                // Sad panda, I need to specify the absolute path on the docker host
                // while running in a container.
                "/opt/jenkins_home/jobs/germanium-selector-builder/workspace:/src:rw"
            ]

        archiveArtifacts artifacts: 'dist/windows/main.exe', fingerprint: true
    }
}

