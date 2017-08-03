
stage('Build Docker EXE Creator') {
    node {
        deleteDir()

        checkout scm

        dockerBuild file: './jenkins/Dockerfile',
            tags: ['bmst/pyinstaller-windows-py27']
    }
}

stage('Build EXE File') {
    node {
        dockerRun image: 'bmst/pyinstaller-windows-py27',
            remove: true,
            env: [
                'PYPI_URL=http://nexus:8081/repository/pypi-local/pypi',
                'PYPI_INDEX_URL=http://nexus:8081/repository/pypi-local/simple'
            ],
            links: [
                'nexus:nexus'
            ],
            volumes: [
                "${WORKSPACE}:/src:rw"
            ]
    }
}

