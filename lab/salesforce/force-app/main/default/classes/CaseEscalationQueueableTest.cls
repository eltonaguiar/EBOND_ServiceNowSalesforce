@isTest
private class CaseEscalationQueueableTest {
    @isTest
    static void executeWritesCorrelation() {
        Case c = new Case(Subject = 'Queue me', Origin = 'Phone', Priority = 'Low');
        insert c;
        Test.setMock(HttpCalloutMock.class, new SnowCalloutMock());
        Test.startTest();
        System.enqueueJob(new CaseEscalationQueueable(c.Id));
        Test.stopTest();
        Case stored = [SELECT Snow_Number__c FROM Case WHERE Id = :c.Id];
        System.assertEquals('INC0010001', stored.Snow_Number__c);
    }
}
