
properties([
    parameters([
        string(name: 'LOCAL_PROXY', defaultValue: '172.17.0.1:3128',
                description: 'Squid proxy to use for fetching resources')
    ])
])

stage('Build Docker EXE Creator') {
    node {
        deleteDir()

        checkout scm

        dockerBuild file: './jenkins/Dockerfile',
            build_args: [
                "http_proxy=http://${LOCAL_PROXY}",
                "https_proxy=http://${LOCAL_PROXY}",
                "ftp_proxy=http://${LOCAL_PROXY}"
            ],
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

