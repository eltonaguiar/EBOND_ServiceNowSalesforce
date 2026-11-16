@isTest
private class SnowIncidentRestTest {
    @isTest
    static void patchCreatesCaseByExternalId() {
        RestRequest req = new RestRequest();
        req.requestURI = '/services/apexrest/snow/incident/a9e30c7dc61122760116894de7bcc7bd';
        req.httpMethod = 'PATCH';
        req.requestBody = Blob.valueOf('{"Subject":"From ServiceNow","Snow_Number__c":"INC0010001"}');
        RestContext.request = req;
        RestContext.response = new RestResponse();
        Test.startTest();
        SnowIncidentRest.patchIncident();
        Test.stopTest();
        System.assertEquals(201, RestContext.response.statusCode);
        Case created = [SELECT Subject, Snow_Sync_Source__c FROM Case WHERE Snow_Sys_Id__c = 'a9e30c7dc61122760116894de7bcc7bd' LIMIT 1];
        System.assertEquals('servicenow', created.Snow_Sync_Source__c);
        System.assertEquals('From ServiceNow', created.Subject);
    }
}
