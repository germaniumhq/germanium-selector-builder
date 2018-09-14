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
    def parallelBuilds = [:]

    parallelBuilds."Win32 Build" = {
        node {
            deleteDir()
            checkout scm

            dockerBuild file: './gbs/win32/Dockerfile',
                build_args: ['GBS_PREFIX=gbs/win32/'],
                tags: ['germaniumhq/germanium-selector-builder:win32']
        }
    }

    parralelBuilds."Linux Build" = {
        node {
            deleteDir()
            checkout scm

            dockerBuild file: './gbs/lin64/Dockerfile',
                build_args: ['GBS_PREFIX=gbs/lin32/'],
                tags: ['germaniumhq/germanium-selector-builder:lin64']
    }

    parallel(parallelBuilds)
}

stage('Extract EXE File') {
    node {
        docker.image('germaniumhq/germanium-selector-builder:win32')
              .inside {
            archiveArtifacts artifacts: '/src/dist/main.exe', fingerprint: true
        }
    }
}

