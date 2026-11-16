@isTest
private class CaseTriggerHandlerTest {
    @isTest
    static void insertEnqueuesCallout() {
        Test.setMock(HttpCalloutMock.class, new SnowCalloutMock());
        Test.startTest();
        insert new Case(Subject = 'Escalate me', Origin = 'Phone', Priority = 'Medium');
        Test.stopTest();
        Case stored = [SELECT Snow_Sys_Id__c, Snow_Number__c FROM Case WHERE Subject = 'Escalate me' LIMIT 1];
        System.assertEquals('a9e30c7dc61122760116894de7bcc7bd', stored.Snow_Sys_Id__c);
        System.assertEquals('INC0010001', stored.Snow_Number__c);
    }

    @isTest
    static void servicenowSourceDoesNotCallOut() {
        Test.startTest();
        insert new Case(Subject = 'Inbound', Origin = 'Phone', Snow_Sync_Source__c = 'servicenow');
        Test.stopTest();
        Case stored = [SELECT Snow_Sys_Id__c FROM Case WHERE Subject = 'Inbound' LIMIT 1];
        System.assertEquals(null, stored.Snow_Sys_Id__c);
    }
}
