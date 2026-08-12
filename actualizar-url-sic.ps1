$ErrorActionPreference = "Stop"

$OM_BASE_URL = "http://localhost:8585"
$COLLECTION_FQN = "SIC API.Backup como Servicio"
$NEW_URL = "https://sic.cedia.edu.ec/backup-como-servicios"

if ([string]::IsNullOrWhiteSpace($OM_TOKEN)) {
    $OM_TOKEN = "eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImFkbWluIiwicm9sZXMiOlsiQWRtaW4iXSwiZW1haWwiOiJhZG1pbkBvcGVuLW1ldGFkYXRhLm9yZyIsImlzQm90IjpmYWxzZSwidG9rZW5UeXBlIjoiUEVSU09OQUxfQUNDRVNTIiwidXNlcm5hbWUiOiJhZG1pbiIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNzg0NzMwMjAxLCJleHAiOjE3OTI1MDYyMDF9.oZWGYzutWG_ldXzkaUZzso9-W5zlMLyaSkByOMwrjrM8WHgvBVvYhFjqAxjXcUgtHc1Glh0PlqRD_g0u6FZMv8JzJSspunSrgwOefoGwgIwECybHLmG-CYXgu7fXo-Wf6-mFMimiPZ0VUY_2nEs9nvGKJofHVkXhU2vujjiECGCg0nN1-rESkz-cBCyu83G_No9YBC6IaqPoXqsoW0OC42RBvHGy0sfILmge2EWoXNtkDUCpg5xGIxWBgRb1VHiGt5DjZLiW5EWysXsIXGxbR1UnpCzaFGuOGXWavH5XpKgpr4O5o_4EgipdJnG2XO_fI-_CEEJ-AhRfYr8-PpX1ng"
}

if (
    $OM_TOKEN.Length -lt 100 -or
    $OM_TOKEN.Split(".").Count -ne 3
) {
    throw "No se encontró un JWT válido de OpenMetadata."
}

$HEADERS = @{
    Authorization = "Bearer $OM_TOKEN"
    Accept        = "application/json"
}

$ENCODED_FQN = [System.Uri]::EscapeDataString(
    $COLLECTION_FQN
)

$COLLECTION = Invoke-RestMethod `
    -Method Get `
    -Uri "$OM_BASE_URL/api/v1/apiCollections/name/$ENCODED_FQN" `
    -Headers $HEADERS

$OLD_VERSION = $COLLECTION.version
$OLD_URL = $COLLECTION.endpointURL

Write-Host "Colección: $($COLLECTION.fullyQualifiedName)"
Write-Host "Versión anterior: $OLD_VERSION"
Write-Host "URL anterior: $OLD_URL"

$NEW_DESCRIPTION = @"
Estado del servicio de Backup obtenido desde SIC.

Fuente oficial: $NEW_URL
"@

$PATCH_BODY = @(
    @{
        op    = "replace"
        path  = "/endpointURL"
        value = $NEW_URL
    },
    @{
        op    = "replace"
        path  = "/description"
        value = $NEW_DESCRIPTION
    }
) | ConvertTo-Json -Depth 10

Invoke-RestMethod `
    -Method Patch `
    -Uri "$OM_BASE_URL/api/v1/apiCollections/$($COLLECTION.id)" `
    -Headers $HEADERS `
    -ContentType "application/json-patch+json" `
    -Body $PATCH_BODY |
    Out-Null

$VERIFY = Invoke-RestMethod `
    -Method Get `
    -Uri "$OM_BASE_URL/api/v1/apiCollections/$($COLLECTION.id)" `
    -Headers $HEADERS

Write-Host ""
Write-Host "Versión actual: $($VERIFY.version)"
Write-Host "URL actual: $($VERIFY.endpointURL)"

if ($VERIFY.endpointURL -ne $NEW_URL) {
    throw "OpenMetadata no persistió endpointURL."
}

if ($VERIFY.version -eq $OLD_VERSION) {
    Write-Warning "La URL cambió, pero la versión no aumentó."
}

Write-Host "Actualización completada correctamente."