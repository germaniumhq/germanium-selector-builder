
stage('Build EXE File') {
    node {
        deleteDir()

        checkout scm

        dockerRun image: 'cdrx/pyinstaller-windows:python2',
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

