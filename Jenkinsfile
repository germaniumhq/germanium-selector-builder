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

stage('Build Standalone Binary') {
    def parallelBuilds = [:]

    parallelBuilds."Win32 Build" = {
        node {
            deleteDir()
            checkout scm

            dockerBuild file: './_gbs/win32/Dockerfile',
                build_args: ['GBS_PREFIX=/_gbs/win32/'],
                tags: ['germaniumhq/germanium-selector-builder:win32']
        }
    }

    parallelBuilds."Linux Build" = {
        node {
            deleteDir()
            checkout scm

            dockerBuild file: './_gbs/lin64/Dockerfile',
                build_args: ['GBS_PREFIX=/_gbs/lin64/'],
                tags: ['germaniumhq/germanium-selector-builder:lin64']
        }
    }

    parallel(parallelBuilds)
}

stage('Archive Binaries') {
    node {
        docker.image('germaniumhq/germanium-selector-builder:win32')
              .inside {
            archiveArtifacts artifacts: '/src/dist/main.exe', fingerprint: true
        }

        docker.image('germaniumhq/germanium-selector-builder:lin64')
              .inside {
            archiveArtifacts artifacts: '/src/dist/main', fingerprint: true
        }
    }
}

