germaniumPyExePipeline(
    name: "germanium-selector-builder",
    runFlake8: false,

    preBuild: {
        stage('Container Tests') {
            node {
                deleteDir()
                checkout scm

                gbsBuild([
                    gbs: '/_gbs/lin64/Dockerfile.gbs.test',
                    dockerTag: 'germaniumhq/germanium-selector-builder:lin64-test'
                ])

                docker.image('germaniumhq/germanium-selector-builder:lin64-test')
                    .inside('--link vnc-server:vnc-server --privileged --shm-size 2G') {
                        junitReports("/src/reports") {
                            sh """
                                cd /src
                                export DISPLAY="\$VNC_SERVER_PORT_6000_TCP_ADDR:0"
                                behave --junit
                            """
                        }
                    }
            }
        }
    },

    binaries: [
        "Win 32": [
            gbs: "/_gbs/win32/",
            exe: "/src/dist/germaniumsb.exe",
            dockerTag: "germaniumhq/germanium-selector-builder:win32",
            extraSteps: {
                dockerRun image: 'bmst/chm-generator',
                    remove: true,
                    volumes: [
                        "${pwd()}/germaniumsb/doc/:/src",
                        "${pwd()}/germaniumsb/doc/:/out"
                    ]
            }
        ],

        "Lin 64": [
            gbs: "/_gbs/lin64/",
            exe: "/src/dist/germaniumsb",
            dockerTag: "germaniumhq/germanium-selector-builder:lin64",
            extraSteps: {
                dockerRun image: 'bmst/docker-asciidoctor',
                    remove: true,
                    volumes: [
                        "${pwd()}/germaniumsb/doc/:/documents:rw"
                    ],
                    command: 'asciidoctor index.adoc'
            }
        ]
    ],

    publishAnsiblePlay: "bin/publish.yml",
)
