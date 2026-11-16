@RestResource(urlMapping='/snow/incident/*')
global with sharing class SnowIncidentRest {
    @HttpPatch
    global static void patchIncident() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        String sysId = lastSegment(req.requestURI);
        if (String.isBlank(sysId)) {
            res.statusCode = 400;
            res.responseBody = Blob.valueOf('{"error":"sys_id path segment required"}');
            return;
        }
        Map<String, Object> body = (Map<String, Object>) JSON.deserializeUntyped(req.requestBody.toString());
        List<Case> found = [
            SELECT Id
            FROM Case
            WHERE Snow_Sys_Id__c = :sysId
            LIMIT 1
        ];
        Case row = found.isEmpty() ? new Case(Snow_Sys_Id__c = sysId) : found[0];
        if (body.containsKey('Subject')) {
            row.Subject = (String) body.get('Subject');
        }
        if (body.containsKey('Description')) {
            row.Description = (String) body.get('Description');
        }
        if (body.containsKey('Snow_Number__c')) {
            row.Snow_Number__c = (String) body.get('Snow_Number__c');
        }
        row.Snow_Sync_Source__c = 'servicenow';
        upsert row Snow_Sys_Id__c;
        res.statusCode = found.isEmpty() ? 201 : 200;
        res.responseBody = Blob.valueOf('{"id":"' + row.Id + '","created":' + found.isEmpty() + '}');
    }

    private static String lastSegment(String uri) {
        if (String.isBlank(uri)) {
            return null;
        }
        List<String> parts = uri.split('/');
        return parts.isEmpty() ? null : parts[parts.size() - 1];
    }
}
