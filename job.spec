apiVersion: template.openshift.io/v1
kind: Template
labels:
  app: maintence-widower
  template: mainence-widower
metadata:
  annotations:
    openshift.io/display-name: Maintance Widower
  name: mainence-widower

objects:
 -  apiVersion: batch/v1beta1
    kind: CronJob
    metadata:
      name: maintence-window-start
    spec:
      schedule: "${START_CRON}"
      jobTemplate:
        spec:
          template:
            spec:
              containers:
              - name: hello
                image: quay.io/openshift/origin-cli:4.5.0
                imagePullPolicy: IfNotPresent
                args:
                - oc login \${KUBERNETES_SERVICE_HOST}:\${KUBERNETES_SERVICE_PORT} --token=\$(< /var/run/secrets/kubernetes.io/serviceaccount/token) --certificate-authority /var/run/secrets/kubernetes.io/serviceaccount/ca.crt;
                - oc patch --type=merge --patch='{"spec":{"paused":true}}' machineconfigpool/master
                - oc patch --type=merge --patch='{"spec":{"paused":true}}' machineconfigpool/worker
              serviceAccountName: ${SA}
              restartPolicy: Never

 -  apiVersion: batch/v1beta1
    kind: CronJob
    metadata:
      name: maintence-window-end
    spec:
      schedule: "${STOP_CRON}"
      jobTemplate:
        spec:
          template:
            spec:
              containers:
              - name: hello
                image: quay.io/openshift/origin-cli:4.5.0
                imagePullPolicy: IfNotPresent
                args:
                - oc login \${KUBERNETES_SERVICE_HOST}:\${KUBERNETES_SERVICE_PORT} --token=\$(< /var/run/secrets/kubernetes.io/serviceaccount/token) --certificate-authority /var/run/secrets/kubernetes.io/serviceaccount/ca.crt;
                - oc patch --type=merge --patch='{"spec":{"paused":false}}' machineconfigpool/master
                - oc patch --type=merge --patch='{"spec":{"paused":false}}' machineconfigpool/worker
              serviceAccountName: ${SA}
              restartPolicy: Never

parameters:
- description: Service Account with Admin Permissions to the Cluster
  displayName: Service Account
  name: SA

- description: Start Cron Spec
  displayName: Start Cron
  name: START_CRON
  value: "0 0 * * *"

- description: Stop Cron Spec
  displayName: Stop Cron
  name: STOP_CRON
  value: "0 4 * * *"


