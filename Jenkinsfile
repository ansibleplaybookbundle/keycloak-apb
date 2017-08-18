#!groovy

// https://github.com/feedhenry/fh-pipeline-library
@Library('fh-pipeline-library') _

def repositoryName = "keycloak-apb"
def projectName = "test-${repositoryName}-${currentBuild.number}-${currentBuild.startTimeInMillis}"

stage('Trust') {
    enforceTrustedApproval('aerogear')
}

node ('apb-test') {

    stage ('Checkout') {
        checkout scm
    }
    openshift.withCluster() {

        try {
            openshift.newProject(projectName)

            openshift.withProject(projectName) {

                stage ('Build') {
                    def nb = openshift.newBuild("--name=${repositoryName}", "--binary")
                    openshift.startBuild("${repositoryName}", "--from-dir=.")
                    def buildSelector = nb.narrow("bc").related("builds")

                    try {
                        timeout(15) {
                            buildSelector.untilEach(1) {
                                buildPhase = it.object().status.phase
                                println("Build phase:" + buildPhase)
                                return (it.object().status.phase == "Complete")
                            }
                        }
                    } catch (Exception e) {
                        buildSelector.logs()
                        error "Build timed out"
                    }
                }

                stage ('Test') {
                    // Add admin role to default service account within the project
                    openshift.policy("add-role-to-user", "admin", "--serviceaccount=default")
                    // Create a new pod for running the test.yml playbook
                    openshift.run(
                        "testing-pod",
                        "--image=docker-registry.default.svc:5000/${projectName}/${repositoryName}",
                        "--restart=Never",
                        "--env POD_NAME=testing-pod",
                        "--env POD_NAMESPACE=${projectName}",
                        "--command", "--",
                        "entrypoint.sh test --extra-vars '{\"namespace\": \"${projectName}\"}'"
                    )
                    podSelector = openshift.selector("pod", "testing-pod")

                    try {
                        timeout(15) {
                            podSelector.untilEach(1) {
                                podPhase = it.object().status.phase
                                println("Pod status:" + podPhase)
                                return (it.object().status.phase == "Succeeded")
                            }
                        }
                    } catch (Exception e) {
                        podSelector.logs()
                        error "Pod didn't finish in time."
                    }
                    // Print out log from the testing pod
                    podSelector.logs()
                }

                stage ('Cleanup') {
                    openshift.delete("project", projectName)
                }
            }
        } catch (Exception e) {
            try {
                timeout(15) {
                    input message: 'The test failed. Click on "Approve" to delete the project. Otherwise it will be deleted after 15 minutes'
                }
            } catch (Exception e2) {
                println("Waiting for a user input exceeded its time limit. Deleting the project now.")
            }

            openshift.delete("project", projectName)
            error "Error when running the test: ${e}"
        }
    }
}
