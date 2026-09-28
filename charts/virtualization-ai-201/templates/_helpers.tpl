{{- define "virtualization-ai-201.labels" -}}
app.kubernetes.io/part-of: virtualization-ai-201
app.kubernetes.io/managed-by: {{ .Release.Service }}
demo.redhat-intel.com/cleanup-owner: launchpad-workshop-reclaim
{{- end }}

{{- define "virtualization-ai-201.image" -}}
{{- $image := . -}}
{{- if $image.digest -}}
{{ printf "%s@%s" $image.repository $image.digest }}
{{- else -}}
{{ printf "%s:%s" $image.repository $image.tag }}
{{- end -}}
{{- end }}
