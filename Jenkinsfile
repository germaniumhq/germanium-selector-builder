germaniumPyExePipeline(
    name: "germanium-selector-builder",
    runFlake8: false,

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

    postBuild: {
        stage('Integration') {
            docker.image('germaniumhq/germanium-selector-builder:lin64')
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
    },

    publishAnsiblePlay: "bin/publish.yml",
)
