from diagrams import Cluster, Diagram
from diagrams.onprem.cd import Tekton
from diagrams.onprem.gitops import Argocd
from diagrams.onprem.iac import Terraform
from diagrams.programming.flowchart import Action

with Diagram("Lorem Ipsum Cloud Native CI/CD", show=True, filename='lorem_ipsum_cloud_native_cidcd'):
    with Cluster('CI/CD - Kube'):
        cd = Tekton('cd')
        iac = Terraform('iac')
        gitops = Argocd('gitops')
        with Cluster('Pipeline'):
            build = Action('build')
            unit_test = Action('unit test')
            deploy_test = Action('deploy test')
            e2e_test = Action('integration/e2e test')
            deploy_prod = Action('deploy prod')
            build >> unit_test >> deploy_test >> e2e_test >> deploy_prod
        gitops << [deploy_test, deploy_prod]
        iac >> [deploy_test, deploy_prod]
